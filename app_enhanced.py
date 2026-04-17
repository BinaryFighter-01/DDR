"""
Enhanced Flask app with PDF support
Run: python app.py
"""
from flask import Flask, request, jsonify, send_from_directory
import json
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from backend.pdf_processor import PDFDocumentProcessor, load_documents
from backend.gemini_processor import GeminiProcessor
from backend.enhanced_ddr_generator import EnhancedDDRGenerator
from api.process_pdf import process_pdf_files, process_sample_pdfs, create_html_report

app = Flask(__name__, static_folder='frontend', static_url_path='')

# CORS helper
def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    return jsonify({
        "status": "healthy",
        "service": "DiagnoReport",
        "version": "2.0",
        "features": [
            "PDF text extraction",
            "PDF image extraction",
            "Intelligent report generation",
            "Severity assessment",
            "Recommendation prioritization"
        ]
    }), 200, cors_headers()

@app.route('/api/process_pdf', methods=['POST', 'OPTIONS'])
def process_pdf():
    """Process PDF files and generate DDR report"""
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        if 'inspection_file' not in request.files or 'thermal_file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Both inspection_file and thermal_file are required'
            }), 400, cors_headers()
        
        inspection_file = request.files['inspection_file']
        thermal_file = request.files['thermal_file']
        include_images = request.form.get('include_images', 'true').lower() == 'true'
        
        result = process_pdf_files(
            inspection_file,
            thermal_file,
            api_key=os.getenv('GEMINI_API_KEY'),
            include_images=include_images
        )
        
        return jsonify(result), 200, cors_headers()
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500, cors_headers()

@app.route('/api/process_samples', methods=['GET', 'OPTIONS'])
def process_samples():
    """Process sample PDF files"""
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        result = process_sample_pdfs()
        return jsonify(result), 200, cors_headers()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500, cors_headers()

@app.route('/api/report_html', methods=['POST', 'OPTIONS'])
def report_html():
    """Convert DDR report to HTML"""
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        ddr = request.get_json()
        html = create_html_report(ddr)
        return html, 200, {'Content-Type': 'text/html', **cors_headers()}
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500, cors_headers()

@app.route('/api/samples', methods=['GET', 'OPTIONS'])
def samples():
    """Get sample data"""
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        sample_dir = Path(__file__).parent / 'sample_documents'
        inspection_json = sample_dir / 'inspection_report.json'
        thermal_json = sample_dir / 'thermal_report.json'
        
        data = {
            'status': 'available',
            'pdf_samples': {
                'inspection': 'Sample Report.pdf',
                'thermal': 'Thermal Images.pdf'
            },
            'json_samples': {
                'inspection': inspection_json.exists(),
                'thermal': thermal_json.exists()
            }
        }
        
        return jsonify(data), 200, cors_headers()
    except Exception as e:
        return jsonify({'error': str(e)}), 500, cors_headers()

if __name__ == '__main__':
    print("🚀 Starting DiagnoReport Server...")
    print("📊 Listening on http://localhost:5000")
    print("📁 Processing PDFs: sample_documents/Sample Report.pdf, sample_documents/Thermal Images.pdf")
    app.run(debug=True, port=5000, host='0.0.0.0')
