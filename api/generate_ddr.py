"""
Main API handler for Vercel deployment
Endpoint: /api/generate-ddr
"""
import json
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from document_processor import DocumentProcessor
from gemini_processor import GeminiProcessor
from ddr_generator import DDRGenerator


def handler(request):
    """
    Main handler for generating DDR reports
    
    Expected POST body:
    {
        "inspection_report": {...},
        "thermal_report": {...},
        "property_address": "string",
        "inspection_date": "string"
    }
    """
    
    if request.method == 'OPTIONS':
        return cors_response({}, 200)
    
    if request.method != 'POST':
        return cors_response({"error": "Only POST allowed"}, 405)
    
    try:
        # Parse request
        body = json.loads(request.get_data(as_text=True))
        
        inspection_data = body.get('inspection_report')
        thermal_data = body.get('thermal_report')
        property_address = body.get('property_address', '')
        inspection_date = body.get('inspection_date', '')
        output_format = body.get('output_format', 'json')  # json or html
        
        if not inspection_data or not thermal_data:
            return cors_response(
                {"error": "Both inspection_report and thermal_report required"},
                400
            )
        
        # Get Gemini API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return cors_response(
                {"error": "GEMINI_API_KEY not configured on server"},
                500
            )
        
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
            return cors_response(
                {"html": html_content, "status": "success"},
                200
            )
        else:
            return cors_response(
                {"ddr_report": ddr_report, "status": "success"},
                200
            )
    
    except json.JSONDecodeError:
        return cors_response({"error": "Invalid JSON in request body"}, 400)
    except Exception as e:
        return cors_response(
            {"error": f"Processing error: {str(e)}", "type": type(e).__name__},
            500
        )


def cors_response(data, status_code):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }
