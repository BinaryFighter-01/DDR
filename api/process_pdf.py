"""
DiagnoReport API Endpoint for PDF Processing
Handles file uploads and generates comprehensive DDR reports with images
"""

import os
import json
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename

# Backend imports
from backend.pdf_processor import PDFDocumentProcessor, load_documents
from backend.gemini_processor import GeminiProcessor
from backend.enhanced_ddr_generator import EnhancedDDRGenerator, create_ddr_output

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'json'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_pdf_files(inspection_file, thermal_file, api_key=None):
    """
    Process inspection and thermal PDF files
    
    Args:
        inspection_file: Inspection report file (PDF or JSON)
        thermal_file: Thermal report file (PDF or JSON)
        api_key: Gemini API key for enhanced analysis
        
    Returns:
        Complete DDR report with extracted images
    """
    result = {
        'status': 'error',
        'message': '',
        'ddr': None,
        'metadata': {}
    }
    
    try:
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save uploaded files
        if hasattr(inspection_file, 'filename'):
            inspection_path = os.path.join(temp_dir, secure_filename(inspection_file.filename))
            inspection_file.save(inspection_path)
        else:
            inspection_path = inspection_file
        
        if hasattr(thermal_file, 'filename'):
            thermal_path = os.path.join(temp_dir, secure_filename(thermal_file.filename))
            thermal_file.save(thermal_path)
        else:
            thermal_path = thermal_file
        
        # Process files based on type
        processor = PDFDocumentProcessor()
        
        # Load inspection data
        if inspection_path.lower().endswith('.pdf'):
            inspection_data = processor.process_inspection_report(inspection_path)
        else:
            with open(inspection_path, 'r') as f:
                inspection_data = json.load(f)
                inspection_data['source_file'] = Path(inspection_path).name
        
        # Load thermal data
        if thermal_path.lower().endswith('.pdf'):
            thermal_data = processor.process_thermal_report(thermal_path)
        else:
            with open(thermal_path, 'r') as f:
                thermal_data = json.load(f)
                thermal_data['source_file'] = Path(thermal_path).name
        
        # Check for processing errors
        if not inspection_data.get('success', True) or not thermal_data.get('success', True):
            result['message'] = 'Error processing input files'
            result['metadata'] = {
                'inspection_error': inspection_data.get('error'),
                'thermal_error': thermal_data.get('error')
            }
            return result
        
        # Generate DDR report
        gemini_processor = None
        if api_key:
            try:
                gemini_processor = GeminiProcessor(api_key)
            except:
                pass  # Continue without AI enhancement
        
        ddr_generator = EnhancedDDRGenerator(gemini_processor)
        ddr_report = ddr_generator.generate_complete_ddr(
            inspection_data,
            thermal_data,
            include_images=True
        )
        
        result['status'] = 'success'
        result['message'] = 'DDR report generated successfully'
        result['ddr'] = ddr_report
        result['metadata'] = {
            'property': ddr_report['metadata'].get('property_address'),
            'inspection_date': ddr_report['metadata'].get('inspection_date'),
            'total_images': ddr_report['metadata'].get('total_images_extracted'),
            'areas_analyzed': ddr_report['metadata'].get('total_areas_analyzed'),
            'total_issues': ddr_report['property_issue_summary'].get('total_issues_found')
        }
        
        # Cleanup
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass
        
    except FileNotFoundError as e:
        result['message'] = f'File not found: {str(e)}'
    except Exception as e:
        result['message'] = f'Error processing files: {str(e)}'
        import traceback
        result['error_details'] = traceback.format_exc()
    
    return result


def process_sample_pdfs():
    """
    Process sample PDFs from sample_documents folder
    
    Returns:
        Complete DDR report
    """
    sample_dir = Path(__file__).parent.parent / 'sample_documents'
    inspection_pdf = sample_dir / 'Sample Report.pdf'
    thermal_pdf = sample_dir / 'Thermal Images.pdf'
    
    if not (inspection_pdf.exists() and thermal_pdf.exists()):
        return {
            'status': 'error',
            'message': f'Sample PDFs not found in {sample_dir}',
            'ddr': None
        }
    
    return process_pdf_files(
        str(inspection_pdf),
        str(thermal_pdf),
        api_key=os.getenv('GEMINI_API_KEY')
    )


def get_ddr_json(ddr_report):
    """Get DDR as JSON"""
    return json.dumps(ddr_report, indent=2, default=str)


def get_ddr_html(ddr_report):
    """Get DDR as HTML"""
    return create_html_report(ddr_report)


def create_html_report(ddr):
    """Create HTML formatted DDR report with images"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DiagnoReport - Detailed Diagnostic Report</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            header {{
                border-bottom: 3px solid #007bff;
                margin-bottom: 30px;
                padding-bottom: 20px;
            }}
            h1 {{
                color: #007bff;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .metadata {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                background: #f0f8ff;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 30px;
            }}
            .metadata-item {{
                border-left: 4px solid #007bff;
                padding-left: 15px;
            }}
            .metadata-label {{
                font-weight: bold;
                color: #555;
                font-size: 0.9em;
                text-transform: uppercase;
            }}
            .metadata-value {{
                font-size: 1.1em;
                color: #222;
                margin-top: 5px;
            }}
            section {{
                margin: 40px 0;
            }}
            h2 {{
                font-size: 1.8em;
                color: #007bff;
                border-left: 5px solid #007bff;
                padding-left: 15px;
                margin-bottom: 20px;
                margin-top: 30px;
            }}
            .section-content {{
                background: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
            }}
            .issue-card {{
                background: white;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 10px 0;
                border-radius: 3px;
            }}
            .issue-card.critical {{
                border-left-color: #dc3545;
                background: #fff5f5;
            }}
            .issue-card.high {{
                border-left-color: #fd7e14;
                background: #fff8f0;
            }}
            .issue-card.medium {{
                border-left-color: #ffc107;
            }}
            .issue-card.low {{
                border-left-color: #28a745;
                background: #f5fff5;
            }}
            .severity-badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.85em;
                margin-right: 10px;
            }}
            .severity-badge.critical {{ background: #dc3545; color: white; }}
            .severity-badge.high {{ background: #fd7e14; color: white; }}
            .severity-badge.medium {{ background: #ffc107; color: #333; }}
            .severity-badge.low {{ background: #28a745; color: white; }}
            
            .area-section {{
                margin: 20px 0;
                padding: 20px;
                background: white;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .area-title {{
                font-size: 1.3em;
                color: #333;
                margin-bottom: 15px;
                font-weight: bold;
            }}
            .observations {{
                background: #f0f8ff;
                padding: 15px;
                border-radius: 3px;
                margin: 10px 0;
            }}
            .observation-item {{
                margin: 8px 0;
                padding-left: 20px;
                position: relative;
            }}
            .observation-item:before {{
                content: "▸";
                position: absolute;
                left: 0;
                color: #007bff;
                font-weight: bold;
            }}
            .image-container {{
                margin: 20px 0;
                text-align: center;
            }}
            .image-container img {{
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }}
            .image-label {{
                font-size: 0.9em;
                color: #666;
                margin-top: 5px;
            }}
            .recommendation {{
                background: #e8f5e9;
                border-left: 4px solid #28a745;
                padding: 15px;
                margin: 10px 0;
                border-radius: 3px;
            }}
            .recommendation-action {{
                font-weight: bold;
                color: #1b5e20;
                margin-bottom: 5px;
            }}
            .recommendation-meta {{
                font-size: 0.9em;
                color: #558b2f;
            }}
            .summary-stats {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin: 20px 0;
            }}
            .stat-card {{
                background: #f0f8ff;
                border: 2px solid #007bff;
                border-radius: 5px;
                padding: 20px;
                text-align: center;
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
            }}
            .stat-label {{
                font-size: 0.9em;
                color: #666;
                text-transform: uppercase;
                margin-top: 10px;
            }}
            .missing-info {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 10px 0;
                border-radius: 3px;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #999;
                font-size: 0.9em;
            }}
            @media print {{
                body {{ background: white; }}
                .container {{ box-shadow: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📋 Detailed Diagnostic Report (DDR)</h1>
                <p style="color: #666;">DiagnoReport v{ddr.get('version', '2.0')}</p>
            </header>
            
            <div class="metadata">
                <div class="metadata-item">
                    <div class="metadata-label">Property Address</div>
                    <div class="metadata-value">{ddr['metadata'].get('property_address', 'Not Available')}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Inspection Date</div>
                    <div class="metadata-value">{ddr['metadata'].get('inspection_date', 'Not Available')}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Inspector</div>
                    <div class="metadata-value">{ddr['metadata'].get('inspector_name', 'Not Available')}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Report Generated</div>
                    <div class="metadata-value">{ddr.get('generated_at', 'N/A')[:10]}</div>
                </div>
            </div>
            
            <section>
                <h2>📊 Property Issue Summary</h2>
                <div class="section-content">
    """
    
    summary = ddr.get('property_issue_summary', {})
    html += f"""
                    <div class="summary-stats">
                        <div class="stat-card">
                            <div class="stat-number">{summary.get('total_issues_found', 0)}</div>
                            <div class="stat-label">Total Issues</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{ddr['metadata'].get('total_images_extracted', 0)}</div>
                            <div class="stat-label">Images Extracted</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{ddr['metadata'].get('total_areas_analyzed', 0)}</div>
                            <div class="stat-label">Areas Analyzed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{len(ddr.get('recommended_actions', []))}</div>
                            <div class="stat-label">Recommendations</div>
                        </div>
                    </div>
                    <p style="font-size: 1.1em; line-height: 1.8; margin-top: 20px;">
                        <strong>Summary:</strong> {summary.get('client_summary', 'N/A')}
                    </p>
                </div>
            </section>
            
            <section>
                <h2>🔍 Area-wise Observations</h2>
    """
    
    for area in ddr.get('area_wise_observations', []):
        html += f"""
                <div class="area-section">
                    <div class="area-title">🏗️ {area.get('area_name', 'Unknown Area')}</div>
        """
        
        # Observations
        if area.get('observations'):
            html += '<div class="observations"><strong>Observations:</strong>'
            for obs in area.get('observations', [])[:5]:
                html += f'<div class="observation-item">{obs}</div>'
            html += '</div>'
        
        # Issues
        if area.get('inspection_issues'):
            html += '<div class="observations" style="background: #fff5f5;"><strong>Issues Found:</strong>'
            for issue in area.get('inspection_issues', [])[:5]:
                html += f'<div class="observation-item">{issue}</div>'
            html += '</div>'
        
        # Images
        if area.get('images'):
            html += '<div class="image-container">'
            for img in area.get('images', [])[:2]:
                if img.get('data'):
                    html += f'''
                    <img src="data:image/{img.get('format', 'png')};base64,{img.get('data')[:100]}..." 
                         alt="Area image" style="max-width: 300px;">
                    <div class="image-label">Image from page {img.get('page', 'unknown')}</div>
                    '''
            html += '</div>'
        
        html += '</div>'
    
    html += """
            </section>
            
            <section>
                <h2>⚠️ Severity Assessment</h2>
                <div class="section-content">
    """
    
    severity = ddr.get('severity_assessment', {})
    html += f"<p><strong>Overall Severity:</strong> {severity.get('overall_severity', 'Not Available')}</p>"
    
    if severity.get('critical_issues', {}).get('items'):
        html += '<h3 style="color: #dc3545; margin-top: 20px;">Critical Issues</h3>'
        for issue in severity['critical_issues']['items'][:5]:
            html += f'<div class="issue-card critical"><span class="severity-badge critical">CRITICAL</span> {issue}</div>'
    
    if severity.get('high_priority_issues', {}).get('items'):
        html += '<h3 style="color: #fd7e14; margin-top: 20px;">High Priority Issues</h3>'
        for issue in severity['high_priority_issues']['items'][:5]:
            html += f'<div class="issue-card high"><span class="severity-badge high">HIGH</span> {issue}</div>'
    
    html += """
                </div>
            </section>
            
            <section>
                <h2>✅ Recommended Actions</h2>
                <div class="section-content">
    """
    
    for i, rec in enumerate(ddr.get('recommended_actions', [])[:10], 1):
        priority = rec.get('priority', 'medium').lower()
        html += f"""
                <div class="recommendation">
                    <div class="recommendation-action">{i}. {rec.get('action', 'N/A')}</div>
                    <div class="recommendation-meta">
                        <span class="severity-badge {priority}">{priority.upper()}</span>
                        Timeline: {rec.get('recommended_timeline', 'N/A')} | 
                        Cost: {rec.get('estimated_cost', 'N/A')}
                    </div>
                </div>
        """
    
    html += """
                </div>
            </section>
            
            <section>
                <h2>📝 Missing or Unclear Information</h2>
                <div class="section-content">
    """
    
    missing = ddr.get('missing_information', {})
    if missing.get('data_gaps'):
        for gap in missing['data_gaps']:
            html += f'<div class="missing-info">ℹ️ {gap}</div>'
    
    img_status = missing.get('image_status', {})
    html += f"""
                    <div style="margin-top: 20px; padding: 15px; background: #f0f8ff; border-radius: 3px;">
                        <strong>Image Extraction Status:</strong><br>
                        • Inspection Report: {img_status.get('inspection_report_images', 0)} images<br>
                        • Thermal Report: {img_status.get('thermal_report_images', 0)} images<br>
                        • Status: {img_status.get('status', 'Unknown')}
                    </div>
    """
    
    html += """
                </div>
            </section>
            
            <div class="footer">
                <p>This report was generated by DiagnoReport - An AI-Powered Diagnostic Report Generator</p>
                <p>For questions or clarifications, please contact the property inspector or facility manager.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == '__main__':
    import sys
    
    # Test with sample PDFs
    result = process_sample_pdfs()
    
    if result['status'] == 'success':
        print("✅ DDR Report Generated Successfully")
        print(f"\nMetadata: {result['metadata']}")
        print(f"\nProperty: {result['ddr']['metadata'].get('property_address')}")
        print(f"Total Issues: {result['ddr']['property_issue_summary'].get('total_issues_found')}")
        print(f"Areas Analyzed: {result['ddr']['metadata'].get('total_areas_analyzed')}")
        print(f"Images Extracted: {result['ddr']['metadata'].get('total_images_extracted')}")
    else:
        print(f"❌ Error: {result['message']}")
