"""
Deployment configuration for local testing with Flask
Run: python app.py
"""
from flask import Flask, request, jsonify, send_from_directory
import json
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from backend.document_processor import DocumentProcessor
from backend.gemini_processor import GeminiProcessor
from backend.ddr_generator import DDRGenerator

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
        "version": "1.0.0"
    }), 200, cors_headers()

@app.route('/api/samples', methods=['GET', 'OPTIONS'])
def samples():
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        with open('sample_documents/inspection_report.json') as f:
            inspection = json.load(f)
        with open('sample_documents/thermal_report.json') as f:
            thermal = json.load(f)
        
        return jsonify({
            "inspection_report": inspection,
            "thermal_report": thermal
        }), 200, cors_headers()
    except Exception as e:
        return jsonify({"error": str(e)}), 500, cors_headers()

@app.route('/api/generate_ddr', methods=['POST', 'OPTIONS'])
def generate_ddr():
    if request.method == 'OPTIONS':
        return '', 200, cors_headers()
    
    try:
        data = request.get_json()
        
        inspection_data = data.get('inspection_report')
        thermal_data = data.get('thermal_report')
        property_address = data.get('property_address', '')
        inspection_date = data.get('inspection_date', '')
        output_format = data.get('output_format', 'json')
        
        if not inspection_data or not thermal_data:
            return jsonify({
                "error": "Both inspection_report and thermal_report required"
            }), 400, cors_headers()
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                "error": "GEMINI_API_KEY not configured. Set it with: export GEMINI_API_KEY='your-key'"
            }), 500, cors_headers()
        
        # Initialize processors
        gemini_processor = GeminiProcessor(api_key)
        ddr_gen = DDRGenerator(gemini_processor)
        
        # Generate DDR
        ddr_report = ddr_gen.generate_complete_ddr(
            inspection_data,
            thermal_data,
            property_address,
            inspection_date
        )
        
        if output_format == 'html':
            html_content = ddr_gen.export_to_html(ddr_report)
            return jsonify({
                "status": "success",
                "html": html_content
            }), 200, cors_headers()
        else:
            return jsonify({
                "status": "success",
                "ddr_report": ddr_report
            }), 200, cors_headers()
    
    except Exception as e:
        return jsonify({
            "error": f"Processing error: {str(e)}",
            "type": type(e).__name__
        }), 500, cors_headers()

if __name__ == '__main__':
    print("Starting DiagnoReport...")
    print("Server: http://localhost:5000")
    print("Note: Set GEMINI_API_KEY before running:")
    print("   export GEMINI_API_KEY='your-api-key'")
    print()
    app.run(debug=True, port=5000)
