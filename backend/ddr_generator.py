"""
DDR (Detailed Diagnostic Report) Generator
Assembles final client-ready report with all sections
"""
import json
from typing import Dict, List
from datetime import datetime
from .document_processor import DocumentProcessor
from .gemini_processor import GeminiProcessor


class DDRGenerator:
    """Generate structured Detailed Diagnostic Reports"""
    
    def __init__(self, gemini_processor: GeminiProcessor):
        self.gemini = gemini_processor
        self.doc_processor = DocumentProcessor()
    
    def generate_complete_ddr(self, 
                             inspection_data: Dict, 
                             thermal_data: Dict,
                             property_address: str = "",
                             inspection_date: str = "") -> Dict:
        """Generate complete DDR report"""
        
        # Merge documents
        merged_analysis = self.gemini.merge_inspection_and_thermal(
            inspection_data, 
            thermal_data
        )
        
        # Validate consistency
        consistency_check = self.gemini.validate_data_consistency(
            inspection_data, 
            thermal_data
        )
        
        # Extract components
        areas = self.doc_processor.get_areas_from_inspection()
        severity_clues = self.doc_processor.get_severity_clues()
        thermal_anomalies = self.doc_processor.get_temperature_anomalies()
        
        # Build DDR sections
        ddr = {
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "property_address": property_address,
                "inspection_date": inspection_date,
                "report_type": "Detailed Diagnostic Report (DDR)"
            },
            "sections": {}
        }
        
        # 1. Property Issue Summary
        ddr["sections"]["property_issue_summary"] = self._generate_property_summary(
            merged_analysis, 
            inspection_data,
            thermal_data
        )
        
        # 2. Area-wise Observations
        ddr["sections"]["area_wise_observations"] = self._generate_area_observations(
            areas,
            inspection_data,
            thermal_data
        )
        
        # 3. Probable Root Cause
        ddr["sections"]["probable_root_cause"] = self._generate_root_causes(
            merged_analysis,
            severity_clues,
            thermal_anomalies
        )
        
        # 4. Severity Assessment
        ddr["sections"]["severity_assessment"] = self._generate_severity_assessment(
            severity_clues,
            merged_analysis
        )
        
        # 5. Recommended Actions
        ddr["sections"]["recommended_actions"] = self._generate_recommendations(
            severity_clues,
            thermal_anomalies,
            merged_analysis
        )
        
        # 6. Additional Notes
        ddr["sections"]["additional_notes"] = self._generate_additional_notes(
            consistency_check,
            merged_analysis
        )
        
        # 7. Missing or Unclear Information
        ddr["sections"]["missing_or_unclear"] = self._generate_missing_info(
            consistency_check,
            inspection_data,
            thermal_data
        )
        
        # Images (if any)
        ddr["images"] = self._collect_images(inspection_data, thermal_data)
        
        # Data Quality Assessment
        ddr["data_quality"] = consistency_check
        
        return ddr
    
    def _generate_property_summary(self, merged: Dict, inspection: Dict, thermal: Dict) -> str:
        """Generate Property Issue Summary"""
        summary = merged.get("summary", "")
        
        if not summary:
            all_findings = (
                self.doc_processor.extract_text_observations(inspection) +
                self.doc_processor.extract_text_observations(thermal)
            )
            summary = f"Property inspection identified {len(all_findings)} key observations requiring analysis."
        
        return f"""
PROPERTY ISSUE SUMMARY
{'='*50}

{summary}

Key Areas Affected: {', '.join(merged.get('combined_findings', ['Multiple areas'])[:5])}

Data Sources:
- Inspection Report: Analyzed
- Thermal Report: Analyzed
"""
    
    def _generate_area_observations(self, areas: List[str], inspection: Dict, thermal: Dict) -> str:
        """Generate Area-wise Observations"""
        
        result = "\nAREA-WISE OBSERVATIONS\n" + "="*50 + "\n"
        
        inspection_obs = self.doc_processor.extract_text_observations(inspection)
        thermal_obs = self.doc_processor.extract_text_observations(thermal)
        
        if areas:
            for area in areas:
                result += f"\n{area.upper()}\n{'-'*40}\n"
                
                area_specific_obs = [o for o in inspection_obs if area.lower() in o.lower()]
                thermal_specific = [o for o in thermal_obs if area.lower() in o.lower()]
                
                if area_specific_obs:
                    result += "Inspection Findings:\n"
                    for obs in area_specific_obs[:3]:
                        result += f"  • {obs}\n"
                
                if thermal_specific:
                    result += "Thermal Findings:\n"
                    for obs in thermal_specific[:3]:
                        result += f"  • {obs}\n"
                
                if not area_specific_obs and not thermal_specific:
                    result += "  • No specific observations\n"
        else:
            result += "General Observations:\n"
            for obs in (inspection_obs + thermal_obs)[:10]:
                result += f"  • {obs}\n"
        
        return result
    
    def _generate_root_causes(self, merged: Dict, severity: Dict, thermal: List) -> str:
        """Generate Probable Root Cause analysis"""
        
        result = "\nPROBABLE ROOT CAUSE\n" + "="*50 + "\n"
        
        critical_issues = severity.get("critical", [])
        if critical_issues:
            result += "CRITICAL ISSUES:\n"
            for issue in critical_issues[:3]:
                result += f"  • {issue}\n"
                result += "    Likely causes: Deterioration, structural issues, or system failure\n"
        
        high_issues = severity.get("high", [])
        if high_issues:
            result += "\nHIGH-SEVERITY ISSUES:\n"
            for issue in high_issues[:3]:
                result += f"  • {issue}\n"
                result += "    Likely causes: Age-related wear, maintenance issues\n"
        
        result += merged.get("analysis", "\nFurther investigation recommended for complete root cause analysis.")
        
        return result
    
    def _generate_severity_assessment(self, severity: Dict, merged: Dict) -> str:
        """Generate Severity Assessment with reasoning"""
        
        result = "\nSEVERITY ASSESSMENT\n" + "="*50 + "\n"
        
        result += "CRITICAL SEVERITY (Immediate Action Required)\n"
        critical = severity.get("critical", [])
        if critical:
            for issue in critical[:5]:
                result += f"  • {issue}\n"
        else:
            result += "  • None identified\n"
        
        result += "\nHIGH SEVERITY (Address within 1-2 weeks)\n"
        high = severity.get("high", [])
        if high:
            for issue in high[:5]:
                result += f"  • {issue}\n"
        else:
            result += "  • None identified\n"
        
        result += "\nMEDIUM SEVERITY (Address within 1-3 months)\n"
        medium = severity.get("medium", [])
        if medium:
            for issue in medium[:5]:
                result += f"  • {issue}\n"
        else:
            result += "  • None identified\n"
        
        result += "\nLOW SEVERITY (Monitor and maintain)\n"
        low = severity.get("low", [])
        if low:
            for issue in low[:5]:
                result += f"  • {issue}\n"
        else:
            result += "  • No issues\n"
        
        return result
    
    def _generate_recommendations(self, severity: Dict, thermal: List, merged: Dict) -> str:
        """Generate Recommended Actions"""
        
        result = "\nRECOMMENDED ACTIONS\n" + "="*50 + "\n"
        
        result += "URGENT (Within 1-2 weeks):\n"
        for i, issue in enumerate(severity.get("critical", [])[:3], 1):
            result += f"  {i}. Address: {issue}\n"
            result += f"     Action: Immediate professional inspection required\n"
        
        result += "\nSHORT-TERM (1-3 months):\n"
        for i, issue in enumerate(severity.get("high", [])[:3], 1):
            result += f"  {i}. Repair/Monitor: {issue}\n"
            result += f"     Action: Schedule professional assessment\n"
        
        result += "\nLONG-TERM (3-12 months):\n"
        for i, issue in enumerate(severity.get("medium", [])[:3], 1):
            result += f"  {i}. Maintenance: {issue}\n"
            result += f"     Action: Plan preventive maintenance\n"
        
        if thermal:
            result += "\nTHERMAL ISSUES:\n"
            for item in thermal[:2]:
                result += f"  • {item}\n"
        
        return result
    
    def _generate_additional_notes(self, consistency: Dict, merged: Dict) -> str:
        """Generate Additional Notes section"""
        
        result = "\nADDITIONAL NOTES\n" + "="*50 + "\n"
        
        if consistency.get("contradictions"):
            result += "Data Conflicts Found:\n"
            for conflict in consistency["contradictions"][:3]:
                result += f"  • {conflict}\n"
        
        result += "\nReport Quality:\n"
        result += "  • Analysis based on provided inspection and thermal data\n"
        result += "  • Professional onsite verification recommended\n"
        result += "  • Report valid for 30 days from inspection date\n"
        
        return result
    
    def _generate_missing_info(self, consistency: Dict, inspection: Dict, thermal: Dict) -> str:
        """Generate Missing or Unclear Information section"""
        
        result = "\nMISSING OR UNCLEAR INFORMATION\n" + "="*50 + "\n"
        
        missing_items = []
        
        # Check common fields
        if not inspection.get("inspector_name"):
            missing_items.append("Inspector Name: Not Available")
        if not inspection.get("inspection_date"):
            missing_items.append("Detailed Inspection Date/Time: Not Available")
        if not thermal.get("calibration_date"):
            missing_items.append("Thermal Camera Calibration Date: Not Available")
        
        gaps = consistency.get("gaps", [])
        if gaps:
            missing_items.extend([f"Data Gap: {gap}" for gap in gaps])
        
        if missing_items:
            for item in missing_items:
                result += f"  • {item}\n"
        else:
            result += "  • All critical information available\n"
        
        return result
    
    def _collect_images(self, inspection: Dict, thermal: Dict) -> List[Dict]:
        """Collect all images from source documents"""
        images = []
        
        inspection_images = self.doc_processor.extract_images(inspection)
        thermal_images = self.doc_processor.extract_images(thermal)
        
        for img in inspection_images:
            images.append({
                "source": "inspection",
                "url": img.get("url", "Image Not Available"),
                "description": img.get("description", "Inspection finding"),
                "area": img.get("area", "Unknown Area")
            })
        
        for img in thermal_images:
            images.append({
                "source": "thermal",
                "url": img.get("url", "Image Not Available"),
                "description": img.get("description", "Thermal finding"),
                "temperature": img.get("temperature", "N/A")
            })
        
        return images
    
    def _generate_images_html(self, images: List[Dict]) -> str:
        """Generate HTML for images section"""
        if not images:
            return ""
        
        html = '<div class="images"><h3>Images</h3>'
        for img in images:
            source = img.get("source", "Unknown")
            description = img.get("description", "No description")
            html += f'<div class="image-item"><p><strong>{source}:</strong> {description}</p></div>'
        html += '</div>'
        return html
    
    def export_to_html(self, ddr: Dict) -> str:
        """Export DDR to HTML format"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Detailed Diagnostic Report (DDR)</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a5490; border-bottom: 3px solid #1a5490; }}
        h2 {{ color: #1a5490; margin-top: 30px; }}
        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .metadata p {{ margin: 5px 0; }}
        .section {{ margin-bottom: 30px; }}
        .content {{ background: white; padding: 15px; border-left: 4px solid #1a5490; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        .warning {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ff6b6b; margin: 15px 0; }}
        .critical {{ background: #f8d7da; }}
        .high {{ background: #f5c2c7; }}
        .medium {{ background: #ffeaa7; }}
        .images {{ margin-top: 20px; }}
        .image-item {{ margin: 15px 0; }}
        img {{ max-width: 100%; height: auto; }}
        footer {{ text-align: center; color: #999; margin-top: 40px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>Detailed Diagnostic Report (DDR)</h1>
    
    <div class="metadata">
        <p><strong>Generated Date:</strong> {ddr['metadata']['generated_date']}</p>
        <p><strong>Property Address:</strong> {ddr['metadata']['property_address'] or 'Not Provided'}</p>
        <p><strong>Inspection Date:</strong> {ddr['metadata']['inspection_date'] or 'Not Provided'}</p>
    </div>
    
    <div class="section">
        <h2>1. Property Issue Summary</h2>
        <div class="content">
            {ddr['sections']['property_issue_summary'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>2. Area-wise Observations</h2>
        <div class="content">
            {ddr['sections']['area_wise_observations'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>3. Probable Root Cause</h2>
        <div class="content">
            {ddr['sections']['probable_root_cause'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>4. Severity Assessment</h2>
        <div class="content warning">
            {ddr['sections']['severity_assessment'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>5. Recommended Actions</h2>
        <div class="content">
            {ddr['sections']['recommended_actions'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>6. Additional Notes</h2>
        <div class="content">
            {ddr['sections']['additional_notes'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <div class="section">
        <h2>7. Missing or Unclear Information</h2>
        <div class="content">
            {ddr['sections']['missing_or_unclear'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    {self._generate_images_html(ddr['images'])}
    
    <footer>
        <p>This report is generated by AI analysis of inspection and thermal data.</p>
        <p>Professional verification recommended for critical issues.</p>
    </footer>
</body>
</html>
"""
        return html
