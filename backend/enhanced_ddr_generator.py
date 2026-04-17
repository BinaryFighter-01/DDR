"""
Enhanced DiagnoReport DDR Generator with Image Support
Generates comprehensive diagnostic reports with embedded images
"""

import json
import base64
from typing import Dict, List, Optional, Any
from datetime import datetime


class ImageHandler:
    """Handle image embedding and placement in reports"""

    @staticmethod
    def encode_image(image_data: Dict) -> Dict:
        """
        Prepare image data for embedding
        
        Args:
            image_data: Dictionary with image information
            
        Returns:
            Image data ready for embedding
        """
        return {
            'data': image_data.get('base64', ''),
            'format': image_data.get('format', 'png'),
            'page': image_data.get('page'),
            'source': image_data.get('source', 'document'),
            'index': image_data.get('index')
        }

    @staticmethod
    def get_images_for_section(section_name: str, images_by_page: Dict) -> List[Dict]:
        """
        Retrieve relevant images for a report section
        
        Args:
            section_name: Name of the section
            images_by_page: Dictionary of images organized by page
            
        Returns:
            List of relevant images
        """
        relevant_images = []
        
        section_keywords = {
            'roof': ['roof', 'shingle', 'flashing', 'gutter'],
            'walls': ['wall', 'exterior', 'siding', 'brick', 'mortar'],
            'hvac': ['hvac', 'furnace', 'ac', 'duct', 'unit'],
            'plumbing': ['plumbing', 'pipe', 'water', 'heater', 'drain'],
            'electrical': ['electrical', 'panel', 'wire', 'outlet'],
            'foundation': ['foundation', 'basement', 'concrete', 'crack'],
            'attic': ['attic', 'insulation', 'vent']
        }
        
        keywords = section_keywords.get(section_name.lower(), [section_name.lower()])
        
        for page_num, page_images in images_by_page.items():
            for img in page_images:
                # For now, include all images (could be enhanced with OCR/vision analysis)
                relevant_images.append(img)
        
        return relevant_images[:3]  # Limit to 3 images per section


class EnhancedDDRGenerator:
    """Generate comprehensive DDR reports with image support"""

    def __init__(self, gemini_processor=None):
        """
        Initialize DDR generator
        
        Args:
            gemini_processor: Gemini API processor for AI analysis
        """
        self.gemini_processor = gemini_processor
        self.image_handler = ImageHandler()

    def generate_complete_ddr(
        self,
        inspection_data: Dict,
        thermal_data: Dict,
        include_images: bool = True
    ) -> Dict:
        """
        Generate complete DDR with all sections and images
        
        Args:
            inspection_data: Inspection report data with text and images
            thermal_data: Thermal report data with text and images
            include_images: Whether to include extracted images
            
        Returns:
            Complete DDR report
        """
        # Combine images from both reports
        all_images = {}
        inspection_images = inspection_data.get('images', {})
        thermal_images = thermal_data.get('images', {})
        all_images.update(inspection_images)
        all_images.update(thermal_images)
        
        # Generate report sections
        ddr = {
            'generated_at': datetime.now().isoformat(),
            'report_type': 'Detailed Diagnostic Report (DDR)',
            'version': '2.0',
            
            # 1. Property Issue Summary
            'property_issue_summary': self._generate_property_summary(
                inspection_data, thermal_data
            ),
            
            # 2. Area-wise Observations
            'area_wise_observations': self._generate_area_observations(
                inspection_data, thermal_data, all_images, include_images
            ),
            
            # 3. Probable Root Causes
            'probable_root_causes': self._generate_root_causes(
                inspection_data, thermal_data
            ),
            
            # 4. Severity Assessment
            'severity_assessment': self._generate_severity_assessment(
                inspection_data, thermal_data
            ),
            
            # 5. Recommended Actions
            'recommended_actions': self._generate_recommendations(
                inspection_data, thermal_data
            ),
            
            # 6. Additional Notes
            'additional_notes': self._generate_additional_notes(
                inspection_data, thermal_data
            ),
            
            # 7. Missing or Unclear Information
            'missing_information': self._generate_missing_info(
                inspection_data, thermal_data
            ),
            
            # Metadata
            'metadata': {
                'property_address': inspection_data.get('property_address', 'Not Available'),
                'inspection_date': inspection_data.get('inspection_date', 'Not Available'),
                'inspector_name': inspection_data.get('inspector_name', 'Not Available'),
                'source_documents': [
                    inspection_data.get('source_file', 'Unknown'),
                    thermal_data.get('source_file', 'Unknown')
                ],
                'total_images_extracted': len(all_images),
                'total_areas_analyzed': len(inspection_data.get('areas', []))
            }
        }
        
        return ddr

    def _generate_property_summary(self, inspection: Dict, thermal: Dict) -> Dict:
        """Generate property issue summary"""
        inspection_issues = []
        for area in inspection.get('areas', []):
            inspection_issues.extend(area.get('issues', []))
        
        thermal_findings = thermal.get('findings', [])
        
        summary = {
            'total_issues_found': len(inspection_issues) + len(thermal_findings),
            'inspection_issues_count': len(inspection_issues),
            'thermal_anomalies_count': len(thermal_findings),
            'primary_concerns': [],
            'overall_assessment': 'Not Available',
            'client_summary': ''
        }
        
        # Identify primary concerns
        if inspection_issues:
            summary['primary_concerns'].extend(inspection_issues[:3])
        
        if thermal_findings:
            for finding in thermal_findings[:3]:
                summary['primary_concerns'].append(
                    f"{finding.get('area', 'Unknown')}: {finding.get('severity', 'UNKNOWN')}"
                )
        
        # Generate AI-powered summary if available
        if self.gemini_processor:
            try:
                prompt = f"""
                Based on these inspection findings:
                {json.dumps(inspection_issues[:5], indent=2)}
                
                And thermal analysis:
                {json.dumps([f["area"] for f in thermal_findings[:3]], indent=2)}
                
                Provide a brief 2-3 sentence client-friendly summary of the main issues.
                Use simple language, avoid jargon.
                """
                summary['client_summary'] = self.gemini_processor.analyze(prompt)
            except:
                summary['client_summary'] = f"Found {summary['total_issues_found']} issues requiring attention."
        else:
            summary['client_summary'] = f"Found {summary['total_issues_found']} issues requiring attention."
        
        return summary

    def _generate_area_observations(
        self,
        inspection: Dict,
        thermal: Dict,
        all_images: Dict,
        include_images: bool = True
    ) -> List[Dict]:
        """Generate area-wise observations with images"""
        observations = []
        
        for area in inspection.get('areas', []):
            area_name = area.get('name', 'Unknown')
            
            # Find corresponding thermal findings
            thermal_findings = []
            for finding in thermal.get('findings', []):
                if area_name.lower() in finding.get('area', '').lower():
                    thermal_findings.append(finding)
            
            # Get relevant images
            section_images = []
            if include_images:
                for page_num, page_images in all_images.items():
                    section_images.extend([
                        self.image_handler.encode_image(img)
                        for img in page_images[:2]
                    ])
            
            observation = {
                'area_name': area_name,
                'description': area.get('description', 'Not Available'),
                'observations': area.get('observations', []),
                'inspection_issues': area.get('issues', []),
                'thermal_data': thermal_findings,
                'combined_analysis': self._combine_findings(area, thermal_findings),
                'images': section_images if include_images else []
            }
            
            observations.append(observation)
        
        return observations

    def _combine_findings(self, inspection_area: Dict, thermal_findings: List) -> str:
        """Combine inspection and thermal findings"""
        issues = inspection_area.get('issues', [])
        
        if not issues and not thermal_findings:
            return "No significant issues identified in this area."
        
        combined = []
        if issues:
            combined.append(f"Inspection findings: {', '.join(issues[:2])}")
        
        if thermal_findings:
            for finding in thermal_findings[:1]:
                combined.append(f"Thermal analysis: {finding.get('area')} - {finding.get('severity', 'MEDIUM')}")
        
        return ' | '.join(combined) if combined else "Not Available"

    def _generate_root_causes(self, inspection: Dict, thermal: Dict) -> List[Dict]:
        """Generate probable root causes"""
        causes = []
        
        # Analyze patterns
        all_issues = []
        for area in inspection.get('areas', []):
            all_issues.extend(area.get('issues', []))
        
        # Common root cause patterns
        issue_cause_map = {
            'missing': 'Poor maintenance or weather damage',
            'leak': 'Seal failure or drainage issues',
            'corrosion': 'Age-related degradation or moisture exposure',
            'crack': 'Settlement, thermal stress, or structural movement',
            'mold': 'Moisture accumulation and inadequate ventilation',
            'efficiency': 'Aging systems or inadequate insulation',
            'thermal': 'Insulation deficiency or air infiltration'
        }
        
        identified_causes = set()
        
        for issue in all_issues:
            for keyword, cause in issue_cause_map.items():
                if keyword.lower() in issue.lower():
                    identified_causes.add(cause)
        
        for cause in identified_causes:
            causes.append({
                'root_cause': cause,
                'affected_areas': self._find_affected_areas(all_issues, cause),
                'evidence': 'Based on inspection and thermal analysis',
                'confidence': 'HIGH'
            })
        
        if not causes:
            causes.append({
                'root_cause': 'Age-related wear and tear',
                'affected_areas': [],
                'evidence': 'Property shows signs of general aging',
                'confidence': 'MEDIUM'
            })
        
        return causes

    def _find_affected_areas(self, issues: List[str], cause_keyword: str) -> List[str]:
        """Find areas affected by a particular cause"""
        affected = []
        area_keywords = {
            'maintenance': ['roof', 'gutters', 'exterior'],
            'moisture': ['walls', 'basement', 'attic'],
            'insulation': ['attic', 'walls', 'hvac'],
            'age': ['electrical', 'plumbing', 'hvac']
        }
        
        return area_keywords.get(cause_keyword.lower(), [])

    def _generate_severity_assessment(self, inspection: Dict, thermal: Dict) -> Dict:
        """Generate severity assessment with reasoning"""
        critical_issues = []
        high_issues = []
        medium_issues = []
        low_issues = []
        
        # Categorize issues by severity
        for area in inspection.get('areas', []):
            for issue in area.get('issues', []):
                if any(word in issue.lower() for word in ['critical', 'severe', 'safety', 'hazard']):
                    critical_issues.append(issue)
                elif any(word in issue.lower() for word in ['major', 'significant', 'extensive']):
                    high_issues.append(issue)
                elif any(word in issue.lower() for word in ['minor', 'small', 'slight']):
                    low_issues.append(issue)
                else:
                    medium_issues.append(issue)
        
        # Check thermal anomalies
        for finding in thermal.get('findings', []):
            severity = finding.get('severity', 'MEDIUM')
            if severity == 'HIGH':
                high_issues.append(f"Thermal: {finding.get('area')}")
            elif severity == 'MEDIUM':
                medium_issues.append(f"Thermal: {finding.get('area')}")
        
        assessment = {
            'overall_severity': self._determine_overall_severity(critical_issues, high_issues),
            'critical_issues': {
                'count': len(critical_issues),
                'items': critical_issues[:5],
                'reasoning': 'Requires immediate attention to prevent safety hazards or property damage'
            },
            'high_priority_issues': {
                'count': len(high_issues),
                'items': high_issues[:5],
                'reasoning': 'Should be addressed within 1-3 months to prevent escalation'
            },
            'medium_priority_issues': {
                'count': len(medium_issues),
                'items': medium_issues[:5],
                'reasoning': 'Can be scheduled for maintenance within 3-12 months'
            },
            'low_priority_issues': {
                'count': len(low_issues),
                'items': low_issues[:5],
                'reasoning': 'Cosmetic or minor issues, address as part of routine maintenance'
            }
        }
        
        return assessment

    def _determine_overall_severity(self, critical: List, high: List) -> str:
        """Determine overall severity level"""
        if critical:
            return 'CRITICAL - Immediate Action Required'
        elif high:
            return 'HIGH - Priority Attention Needed'
        else:
            return 'MEDIUM - Routine Maintenance Recommended'

    def _generate_recommendations(self, inspection: Dict, thermal: Dict) -> List[Dict]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        priority_order = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4
        }
        
        # Extract recommendations from issues
        issue_recommendations = {
            'missing shingles': {
                'action': 'Replace missing roof shingles',
                'priority': 'critical',
                'estimated_cost': 'Moderate',
                'timeline': 'Within 2 weeks'
            },
            'leak': {
                'action': 'Locate and repair leak source',
                'priority': 'high',
                'estimated_cost': 'Moderate',
                'timeline': 'Within 1 month'
            },
            'corrosion': {
                'action': 'Clean and apply protective coating',
                'priority': 'medium',
                'estimated_cost': 'Low to Moderate',
                'timeline': 'Within 3 months'
            },
            'crack': {
                'action': 'Evaluate and seal cracks',
                'priority': 'medium',
                'estimated_cost': 'Low',
                'timeline': 'Within 3 months'
            },
            'insulation': {
                'action': 'Increase insulation to R-38 minimum',
                'priority': 'high',
                'estimated_cost': 'High',
                'timeline': 'Within 6 months'
            }
        }
        
        # Collect unique recommendations
        added_recommendations = set()
        
        for area in inspection.get('areas', []):
            for issue in area.get('issues', []):
                for keyword, rec in issue_recommendations.items():
                    if keyword.lower() in issue.lower() and rec['action'] not in added_recommendations:
                        recommendations.append({
                            'action': rec['action'],
                            'priority': rec['priority'],
                            'priority_order': priority_order.get(rec['priority'], 5),
                            'area_affected': area.get('name'),
                            'estimated_cost': rec['estimated_cost'],
                            'recommended_timeline': rec['timeline'],
                            'reasoning': f"Identified in {area.get('name')}: {issue[:50]}..."
                        })
                        added_recommendations.add(rec['action'])
                        break
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority_order'])
        
        if not recommendations:
            recommendations.append({
                'action': 'Schedule routine maintenance inspection',
                'priority': 'medium',
                'priority_order': 3,
                'area_affected': 'General',
                'estimated_cost': 'Low',
                'recommended_timeline': 'Annually',
                'reasoning': 'Regular maintenance helps prevent future issues'
            })
        
        return recommendations[:10]  # Limit to top 10 recommendations

    def _generate_additional_notes(self, inspection: Dict, thermal: Dict) -> Dict:
        """Generate additional notes and observations"""
        return {
            'inspection_quality': 'Comprehensive visual and thermal inspection performed',
            'data_reliability': 'Based on actual site observations and thermal imaging',
            'limitations': [
                'Some areas may not be fully accessible',
                'Interior components not evaluated',
                'Long-term performance cannot be predicted'
            ],
            'suggestions': [
                'Consider professional assessment for critical items',
                'Plan preventive maintenance schedule',
                'Monitor thermal patterns seasonally'
            ],
            'general_observations': 'Property shows typical wear patterns for its age'
        }

    def _generate_missing_info(self, inspection: Dict, thermal: Dict) -> Dict:
        """Document missing or unclear information"""
        missing = {
            'data_gaps': [],
            'clarifications_needed': [],
            'image_status': {}
        }
        
        # Check for missing inspection data
        required_fields = ['property_address', 'inspection_date', 'inspector_name']
        for field in required_fields:
            if not inspection.get(field) or inspection.get(field) == 'Not Available':
                missing['data_gaps'].append(f"Inspection report missing: {field}")
        
        # Check thermal data
        if not thermal.get('findings'):
            missing['data_gaps'].append('Limited thermal imaging data available')
        
        # Image status
        inspection_images = inspection.get('images', {})
        thermal_images = thermal.get('images', {})
        
        missing['image_status'] = {
            'inspection_report_images': len(inspection_images),
            'thermal_report_images': len(thermal_images),
            'status': 'Images extracted successfully' if (inspection_images or thermal_images) else 'No images found'
        }
        
        if not missing['data_gaps']:
            missing['data_gaps'] = ['All required data available']
        
        return missing


def create_ddr_output(ddr: Dict, output_format: str = 'json') -> str:
    """
    Create final DDR output
    
    Args:
        ddr: Complete DDR dictionary
        output_format: Output format ('json' or 'html')
        
    Returns:
        Formatted DDR output
    """
    if output_format == 'json':
        return json.dumps(ddr, indent=2, default=str)
    elif output_format == 'html':
        return _generate_html_report(ddr)
    else:
        return json.dumps(ddr, indent=2, default=str)


def _generate_html_report(ddr: Dict) -> str:
    """Generate HTML formatted report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Diagnostic Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; border-bottom: 2px solid #007bff; }}
            h2 {{ color: #555; margin-top: 30px; }}
            .section {{ margin: 20px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #007bff; }}
            .critical {{ border-left-color: #dc3545; }}
            .high {{ border-left-color: #fd7e14; }}
            .medium {{ border-left-color: #ffc107; }}
            .low {{ border-left-color: #28a745; }}
            .metadata {{ background: #e7f3ff; padding: 10px; margin: 10px 0; }}
            img {{ max-width: 100%; height: auto; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>Detailed Diagnostic Report (DDR)</h1>
        
        <div class="metadata">
            <p><strong>Property:</strong> {ddr['metadata'].get('property_address', 'N/A')}</p>
            <p><strong>Inspection Date:</strong> {ddr['metadata'].get('inspection_date', 'N/A')}</p>
            <p><strong>Generated:</strong> {ddr.get('generated_at', 'N/A')}</p>
        </div>
        
        <div class="section">
            <h2>Property Issue Summary</h2>
            <p>{ddr['property_issue_summary'].get('client_summary', 'N/A')}</p>
            <p>Total Issues Found: {ddr['property_issue_summary'].get('total_issues_found', 0)}</p>
        </div>
        
        <div class="section">
            <h2>Recommendations</h2>
            <ol>
    """
    
    for rec in ddr.get('recommended_actions', [])[:5]:
        html += f"<li>{rec.get('action', 'N/A')} - {rec.get('estimated_timeline', 'N/A')}</li>"
    
    html += """
            </ol>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == '__main__':
    # Test the enhanced generator
    generator = EnhancedDDRGenerator()
    
    sample_inspection = {
        'property_address': '123 Main St, City, State',
        'inspection_date': '2026-04-15',
        'inspector_name': 'John Doe',
        'source_file': 'Sample Report.pdf',
        'areas': [
            {
                'name': 'Roof',
                'description': 'Roof System',
                'observations': ['Roof appears aged'],
                'issues': ['Missing shingles', 'Flashing deterioration']
            }
        ],
        'images': {1: [], 2: []}
    }
    
    sample_thermal = {
        'property_address': '123 Main St, City, State',
        'inspection_date': '2026-04-15',
        'source_file': 'Thermal Images.pdf',
        'findings': [
            {
                'area': 'Roof',
                'temperature_range': '35-42°C',
                'severity': 'HIGH',
                'analysis': 'Significant thermal variations'
            }
        ],
        'images': {3: []}
    }
    
    ddr = generator.generate_complete_ddr(sample_inspection, sample_thermal)
    print(json.dumps(ddr, indent=2, default=str))
