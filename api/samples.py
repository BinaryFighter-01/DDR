"""
Sample data endpoint - returns sample inspection and thermal reports
"""
import json
from pathlib import Path


def handler(request):
    """Return sample reports for testing"""
    
    try:
        # Load sample documents
        samples_dir = Path(__file__).parent.parent / 'sample_documents'
        
        inspection_path = samples_dir / 'inspection_report.json'
        thermal_path = samples_dir / 'thermal_report.json'
        
        with open(inspection_path) as f:
            inspection = json.load(f)
        
        with open(thermal_path) as f:
            thermal = json.load(f)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "inspection_report": inspection,
                "thermal_report": thermal
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": str(e)})
        }
