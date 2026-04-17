"""
Health check endpoint for Vercel
"""
import json


def handler(request):
    """Simple health check"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "status": "healthy",
            "service": "DDR Report Generator",
            "version": "1.0.0"
        })
    }
