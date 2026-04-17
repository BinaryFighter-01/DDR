"""
Document Processing Module
Extracts text, metadata, and images from inspection and thermal reports
"""
import json
import re
from typing import Dict, List, Tuple, Optional
import base64
from io import BytesIO


class DocumentProcessor:
    """Processes inspection and thermal reports"""
    
    def __init__(self):
        self.inspection_data = {}
        self.thermal_data = {}
        
    def parse_json_document(self, document_str: str, doc_type: str) -> Dict:
        """Parse JSON-formatted document (inspection or thermal report)"""
        try:
            data = json.loads(document_str)
            if doc_type == "inspection":
                self.inspection_data = data
            elif doc_type == "thermal":
                self.thermal_data = data
            return data
        except json.JSONDecodeError:
            return self._parse_text_document(document_str, doc_type)
    
    def _parse_text_document(self, text: str, doc_type: str) -> Dict:
        """Parse plain text document"""
        lines = text.strip().split('\n')
        data = {
            "type": doc_type,
            "sections": [],
            "observations": [],
            "images": []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('##'):
                current_section = line.replace('##', '').strip()
                data["sections"].append({"title": current_section, "content": []})
            elif line.startswith('- ') or line.startswith('* '):
                observation = line[2:].strip()
                data["observations"].append(observation)
                if current_section and data["sections"]:
                    data["sections"][-1]["content"].append(observation)
        
        if doc_type == "inspection":
            self.inspection_data = data
        elif doc_type == "thermal":
            self.thermal_data = data
            
        return data
    
    def extract_text_observations(self, data: Dict) -> List[str]:
        """Extract all text observations from document"""
        observations = []
        
        if "observations" in data:
            observations.extend(data["observations"])
        
        if "sections" in data:
            for section in data["sections"]:
                if isinstance(section.get("content"), list):
                    observations.extend(section["content"])
        
        if "areas" in data:
            for area in data["areas"]:
                if "observations" in area:
                    observations.extend(area["observations"])
                if "issues" in area:
                    observations.extend(area["issues"])
        
        if "findings" in data:
            observations.extend(data["findings"])
        
        return [obs for obs in observations if obs]
    
    def extract_images(self, data: Dict) -> List[Dict]:
        """Extract image references from document"""
        images = []
        
        if "images" in data:
            if isinstance(data["images"], list):
                images.extend(data["images"])
            elif isinstance(data["images"], dict):
                images.append(data["images"])
        
        if "areas" in data:
            for area in data["areas"]:
                if "image" in area:
                    images.append({
                        "area": area.get("name", "Unknown"),
                        "url": area["image"],
                        "description": area.get("description", "")
                    })
        
        if "thermal_images" in data:
            images.extend(data["thermal_images"])
        
        return images
    
    def get_areas_from_inspection(self) -> List[str]:
        """Extract area names from inspection report"""
        areas = set()
        
        if "areas" in self.inspection_data:
            for area in self.inspection_data["areas"]:
                if isinstance(area, dict):
                    areas.add(area.get("name", ""))
                else:
                    areas.add(str(area))
        
        # Extract from text patterns
        text_obs = self.extract_text_observations(self.inspection_data)
        for obs in text_obs:
            match = re.match(r'^(.*?)(?::|,|-)', obs)
            if match:
                potential_area = match.group(1).strip()
                if len(potential_area) < 50:
                    areas.add(potential_area)
        
        return sorted(list(areas))
    
    def get_severity_clues(self) -> Dict[str, List[str]]:
        """Extract severity-related information"""
        severity_info = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        all_obs = self.extract_text_observations(self.inspection_data) + \
                  self.extract_text_observations(self.thermal_data)
        
        critical_keywords = ["urgent", "critical", "failure", "risk", "dangerous", "hazard", "leak", "structural"]
        high_keywords = ["severe", "significant", "major", "damage", "deterioration", "crack"]
        medium_keywords = ["moderate", "issue", "concern", "wear", "aging"]
        
        for obs in all_obs:
            # Ensure obs is a string
            if not isinstance(obs, str):
                obs = str(obs)
            
            obs_lower = obs.lower()
            if any(kw in obs_lower for kw in critical_keywords):
                severity_info["critical"].append(obs)
            elif any(kw in obs_lower for kw in high_keywords):
                severity_info["high"].append(obs)
            elif any(kw in obs_lower for kw in medium_keywords):
                severity_info["medium"].append(obs)
            else:
                severity_info["low"].append(obs)
        
        return severity_info
    
    def get_temperature_anomalies(self) -> List[Dict]:
        """Extract temperature-related findings from thermal report"""
        anomalies = []
        
        if "findings" in self.thermal_data:
            for finding in self.thermal_data["findings"]:
                if isinstance(finding, dict):
                    if any(key in str(finding).lower() for key in ["temp", "heat", "cold", "anomaly"]):
                        anomalies.append(finding)
        
        all_obs = self.extract_text_observations(self.thermal_data)
        for obs in all_obs:
            # Ensure obs is a string
            if not isinstance(obs, str):
                obs = str(obs)
            
            if any(key in obs.lower() for key in ["°c", "°f", "temperature", "thermal", "heat", "anomaly"]):
                anomalies.append({"observation": obs})
        
        return anomalies
