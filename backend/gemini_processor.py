"""
Gemini AI Integration Module
Uses Google Gemini API to intelligently merge and analyze inspection + thermal data
"""
import os
import json
from typing import Dict, List, Optional
import google.generativeai as genai


class GeminiProcessor:
    """Process and merge inspection + thermal data using Gemini API"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        if not api_key:
            raise ValueError("GEMINI_API_KEY not provided")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def merge_inspection_and_thermal(self, 
                                      inspection_data: Dict, 
                                      thermal_data: Dict) -> str:
        """Merge inspection and thermal data using Gemini"""
        
        prompt = f"""You are an expert building inspector AI. Analyze these two inspection reports and create a unified summary.

INSPECTION REPORT DATA:
{json.dumps(inspection_data, indent=2)}

THERMAL REPORT DATA:
{json.dumps(thermal_data, indent=2)}

Tasks:
1. Extract all key observations and findings
2. Identify correlations between inspection and thermal data
3. Flag any conflicting information
4. Highlight missing information
5. Provide a brief unified summary (max 200 words)

Format your response as JSON with keys: "summary", "correlations", "conflicts", "missing_info", "combined_findings"
"""
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"summary": response.text, "correlations": [], "conflicts": [], "missing_info": []}
    
    def generate_ddr_section(self, 
                            section_name: str, 
                            data: Dict, 
                            context: str = "") -> str:
        """Generate a specific section of the DDR"""
        
        if section_name == "property_issue_summary":
            prompt = self._get_summary_prompt(data, context)
        elif section_name == "area_wise_observations":
            prompt = self._get_area_observations_prompt(data)
        elif section_name == "probable_root_cause":
            prompt = self._get_root_cause_prompt(data)
        elif section_name == "severity_assessment":
            prompt = self._get_severity_prompt(data)
        elif section_name == "recommended_actions":
            prompt = self._get_recommendations_prompt(data)
        else:
            return "Not Available"
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _get_summary_prompt(self, data: Dict, context: str) -> str:
        return f"""Based on this inspection and thermal data, provide a concise property issue summary (2-3 paragraphs, client-friendly language):

Data: {json.dumps(data, indent=2)}
Context: {context}

Write clear, non-technical summary of main issues found."""
    
    def _get_area_observations_prompt(self, data: Dict) -> str:
        return f"""Organize these observations by area/location in a client-friendly format:

Data: {json.dumps(data, indent=2)}

Format each area as:
- AREA NAME: [list of observations specific to this area]

Avoid duplication. Use simple language."""
    
    def _get_root_cause_prompt(self, data: Dict) -> str:
        return f"""Based on the inspection and thermal findings, identify probable root causes:

Data: {json.dumps(data, indent=2)}

For each major issue, provide:
1. Issue
2. Most likely root cause(s)
3. Contributing factors

Use evidence from the data. If unclear, say 'requires further investigation'."""
    
    def _get_severity_prompt(self, data: Dict) -> str:
        return f"""Assess severity of issues found and provide reasoning:

Data: {json.dumps(data, indent=2)}

For each issue, rate as: CRITICAL / HIGH / MEDIUM / LOW
Provide brief reasoning based on the evidence.

CRITICAL = Safety risk or major functionality loss
HIGH = Significant damage/decay, needs urgent attention
MEDIUM = Should be addressed soon
LOW = Cosmetic or minor maintenance"""
    
    def _get_recommendations_prompt(self, data: Dict) -> str:
        return f"""Based on findings, provide recommended actions prioritized by urgency:

Data: {json.dumps(data, indent=2)}

Format:
URGENT (within 1-2 weeks):
- Action 1
- Action 2

SHORT-TERM (1-3 months):
- Action 3

LONG-TERM (3-12 months):
- Action 4

Be specific and actionable. Include rough priority."""
    
    def validate_data_consistency(self, inspection: Dict, thermal: Dict) -> Dict:
        """Check for conflicting or missing information"""
        
        prompt = f"""Compare these two reports for conflicts and gaps:

INSPECTION: {json.dumps(inspection, indent=2)}
THERMAL: {json.dumps(thermal, indent=2)}

Identify:
1. Contradictions (e.g., inspection says OK but thermal shows high temp)
2. Missing data (areas mentioned in one but not other)
3. Unexplained observations

Return as JSON with keys: "contradictions", "gaps", "unexplained_findings", "data_quality_issues"
"""
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"analysis": response.text}
    
    def extract_missing_info(self, merged_data: Dict) -> List[str]:
        """Identify what information is missing or unclear"""
        
        missing = []
        
        indicators = ["not available", "unclear", "missing", "unknown", "not provided", "n/a", "insufficient"]
        
        for key, value in merged_data.items():
            if isinstance(value, str):
                if any(ind in value.lower() for ind in indicators):
                    missing.append(f"{key}: {value}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and any(ind in item.lower() for ind in indicators):
                        missing.append(f"{key}: {item}")
        
        return missing
