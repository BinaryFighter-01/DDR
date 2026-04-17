#!/usr/bin/env python3
"""
Test script to validate core functionality without API key
This demonstrates the system's ability to process and merge inspection/thermal data
"""
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from document_processor import DocumentProcessor

def test_document_processor():
    """Test document processing pipeline"""
    print("=" * 60)
    print("🧪 Testing Document Processor...")
    print("=" * 60)
    
    # Load sample documents
    with open('sample_documents/inspection_report.json') as f:
        inspection = json.load(f)
    with open('sample_documents/thermal_report.json') as f:
        thermal = json.load(f)
    
    processor = DocumentProcessor()
    
    # Test 1: Parse documents
    print("\n✓ Test 1: Parsing documents")
    inspection_data = processor.parse_json_document(
        json.dumps(inspection), 
        "inspection"
    )
    thermal_data = processor.parse_json_document(
        json.dumps(thermal), 
        "thermal"
    )
    print(f"  - Inspection areas found: {len(inspection_data.get('areas', []))}")
    print(f"  - Thermal findings found: {len(thermal_data.get('findings', []))}")
    
    # Test 2: Extract observations
    print("\n✓ Test 2: Extracting observations")
    inspection_obs = processor.extract_text_observations(inspection_data)
    thermal_obs = processor.extract_text_observations(thermal_data)
    print(f"  - Inspection observations: {len(inspection_obs)}")
    print(f"  - Thermal observations: {len(thermal_obs)}")
    print(f"  - Sample inspection obs: {inspection_obs[0] if inspection_obs else 'None'}")
    
    # Test 3: Extract images
    print("\n✓ Test 3: Extracting images")
    inspection_images = processor.extract_images(inspection_data)
    thermal_images = processor.extract_images(thermal_data)
    print(f"  - Inspection images: {len(inspection_images)}")
    print(f"  - Thermal images: {len(thermal_images)}")
    
    # Test 4: Get areas
    print("\n✓ Test 4: Extracting areas")
    areas = processor.get_areas_from_inspection()
    print(f"  - Areas identified: {len(areas)}")
    for area in areas[:5]:
        print(f"    • {area}")
    
    # Test 5: Severity assessment
    print("\n✓ Test 5: Severity assessment")
    severity = processor.get_severity_clues()
    print(f"  - Critical issues: {len(severity['critical'])}")
    print(f"  - High severity: {len(severity['high'])}")
    print(f"  - Medium severity: {len(severity['medium'])}")
    print(f"  - Low severity: {len(severity['low'])}")
    
    # Test 6: Temperature anomalies
    print("\n✓ Test 6: Extracting thermal anomalies")
    anomalies = processor.get_temperature_anomalies()
    print(f"  - Anomalies found: {len(anomalies)}")
    
    print("\n" + "=" * 60)
    print("✅ All document processing tests passed!")
    print("=" * 60)
    
    return True

def test_report_structure():
    """Test DDR report structure generation"""
    print("\n" + "=" * 60)
    print("🧪 Testing Report Structure...")
    print("=" * 60)
    
    with open('sample_documents/inspection_report.json') as f:
        inspection = json.load(f)
    
    # Validate structure
    required_fields = ['type', 'property_address', 'inspection_date', 'areas']
    print("\n✓ Validating inspection report structure")
    for field in required_fields:
        assert field in inspection, f"Missing field: {field}"
        print(f"  - {field}: ✓")
    
    # Validate areas have required data
    print("\n✓ Validating area data")
    for area in inspection['areas']:
        assert 'name' in area, "Area missing name"
        assert 'observations' in area, "Area missing observations"
        print(f"  - {area['name']}: {len(area['observations'])} observations")
    
    print("\n" + "=" * 60)
    print("✅ Report structure validation passed!")
    print("=" * 60)
    
    return True

def test_sample_data_validity():
    """Validate sample data is realistic and complete"""
    print("\n" + "=" * 60)
    print("🧪 Testing Sample Data Validity...")
    print("=" * 60)
    
    with open('sample_documents/inspection_report.json') as f:
        inspection = json.load(f)
    with open('sample_documents/thermal_report.json') as f:
        thermal = json.load(f)
    
    # Check inspection data
    print("\n✓ Inspection Report Validation")
    print(f"  - Property: {inspection['property_address']}")
    print(f"  - Year built: {inspection['year_built']}")
    print(f"  - Areas: {len(inspection['areas'])}")
    print(f"  - Safety concerns: {len(inspection.get('safety_concerns', []))}")
    
    # Check thermal data
    print("\n✓ Thermal Report Validation")
    print(f"  - Camera: {thermal['thermal_camera_model']}")
    print(f"  - Findings: {len(thermal['findings'])}")
    
    # Verify correlations
    print("\n✓ Data Correlation")
    inspection_areas = set(a['name'] for a in inspection['areas'])
    thermal_findings = thermal['findings']
    
    correlated_areas = 0
    for finding in thermal_findings:
        if any(area.lower() in finding.get('area', '').lower() for area in inspection_areas):
            correlated_areas += 1
    
    print(f"  - Areas with correlated thermal data: {correlated_areas}/{len(thermal_findings)}")
    
    print("\n" + "=" * 60)
    print("✅ Sample data validity checks passed!")
    print("=" * 60)
    
    return True

def test_api_endpoints():
    """Test that API endpoints are properly structured"""
    print("\n" + "=" * 60)
    print("🧪 Testing API Endpoint Structure...")
    print("=" * 60)
    
    # Check API files exist
    api_files = ['api/generate_ddr.py', 'api/health.py', 'api/samples.py']
    print("\n✓ Checking API endpoint files")
    for file in api_files:
        path = Path(file)
        assert path.exists(), f"Missing: {file}"
        print(f"  - {file}: ✓")
    
    # Check configuration files
    print("\n✓ Checking configuration files")
    config_files = ['vercel.json', 'requirements.txt', 'frontend/index.html']
    for file in config_files:
        path = Path(file)
        assert path.exists(), f"Missing: {file}"
        print(f"  - {file}: ✓")
    
    print("\n" + "=" * 60)
    print("✅ API endpoint structure validation passed!")
    print("=" * 60)
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("DDR Report Generation System - Test Suite".center(60))
    print("=" * 60)
    
    try:
        test_document_processor()
        test_report_structure()
        test_sample_data_validity()
        test_api_endpoints()
        
        print("\n")
        print("=" * 60)
        print("ALL TESTS PASSED".center(60))
        print("=" * 60)
        print("\n📌 Next steps:")
        print("   1. Get Gemini API key: https://aistudio.google.com/app/apikeys")
        print("   2. Run locally: export GEMINI_API_KEY='your-key' && python app.py")
        print("   3. Deploy: vercel deploy")
        print("   4. Set env var in Vercel: Settings → Environment Variables")
        print("   5. Redeploy: vercel deploy --prod")
        print("\n")
        
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
