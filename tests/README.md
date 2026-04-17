# DiagnoReport Testing Guide

This folder contains comprehensive test cases and utilities for validating the DiagnoReport system.

## Test Cases

### 1. Residential Property - Good Condition
**File**: `test_case_residential.json`

A modern residential property in good condition with:
- Well-maintained roof and exterior
- Modern HVAC and plumbing systems
- Proper electrical setup with 200-amp service
- Good insulation and ventilation
- No significant issues

**Expected Output**: Clean report with minimal recommendations

### 2. Commercial Property - Needs Maintenance
**File**: `test_case_commercial.json`

A commercial building with multiple maintenance issues including:
- Aging flat roof membrane
- Corroded metal facade
- Mixed-age HVAC systems
- Water heater and pipe corrosion
- Parking lot settling and cracking
- Outdated electrical systems

**Expected Output**: Report highlighting significant thermal losses and maintenance needs

## Test Structure

Each test case JSON file contains:

```json
{
  "inspection_report": {
    "type": "inspection_report",
    "property_address": "...",
    "inspection_date": "...",
    "inspector_name": "...",
    "areas": [
      {
        "name": "Area name",
        "description": "...",
        "observations": ["..."],
        "issues": ["..."]
      }
    ]
  },
  "thermal_report": {
    "type": "thermal_report",
    "property_address": "...",
    "findings": [
      {
        "area": "...",
        "temperature_range": "...",
        "analysis": "...",
        "anomalies": ["..."],
        "severity": "..."
      }
    ]
  }
}
```

## Running Tests

### Prerequisites
```bash
# Set Gemini API key
export GEMINI_API_KEY="your-api-key-here"  # Linux/Mac
set GEMINI_API_KEY=your-api-key-here       # Windows

# Install dependencies (if not already done)
pip install -r requirements.txt
```

### Run Test Suite
```bash
# From project root
python tests/test_runner.py
```

### Run Individual Test
```bash
# From project root
python -c "
from tests.test_runner import DiagnoReportTestRunner
runner = DiagnoReportTestRunner()
runner.run_test('Residential', 'test_case_residential.json')
runner.print_summary()
"
```

## Test Outputs

Generated files after running tests:

- `output_Residential_Property_Good_Condition.json` - Generated DDR report
- `output_Commercial_Property_Needs_Maintenance.json` - Generated DDR report
- `test_summary.json` - Test execution summary

## Expected Test Behavior

### Successful Test ✓
- All 7 required DDR sections generated
- Report contains executive summary, analysis, and recommendations
- Output saved to JSON file
- Status: PASSED

### Failed Test ✗
- Missing required sections in report
- Report structure invalid
- Status: FAILED

### Error Test ✗
- API call failed
- Missing dependencies
- Configuration issues
- Status: ERROR

## Test Validation

Each test validates:

1. **Structure**: All required DDR sections present
   - executive_summary
   - property_details
   - inspection_findings
   - thermal_analysis
   - integrated_analysis
   - recommendations
   - conclusion

2. **Content**: 
   - Proper text generation from inspection/thermal data
   - Logical analysis and recommendations
   - Accurate cross-referencing between reports

3. **Output Format**:
   - Valid JSON structure
   - Proper field types and values
   - No malformed data

## Adding New Test Cases

To add a new test case:

1. Create a new JSON file: `test_case_<name>.json`
2. Follow the structure in existing test cases
3. Include both inspection and thermal report data
4. Update `test_runner.py` to include your test in the `run_all_tests()` method

Example:
```python
def run_all_tests(self):
    tests = [
        ('Residential Property - Good Condition', 'test_case_residential.json'),
        ('Commercial Property - Needs Maintenance', 'test_case_commercial.json'),
        ('Your New Test', 'test_case_newtest.json'),  # Add here
    ]
```

## Troubleshooting

### "GEMINI_API_KEY not set"
- Ensure API key is exported: `export GEMINI_API_KEY=your-key`
- Check key is valid from https://aistudio.google.com/app/apikeys

### "Test failed with ERROR"
- Check internet connection for API calls
- Verify API key quota not exceeded
- Check Python dependencies: `pip install -r requirements.txt`

### "Missing sections in report"
- Check backend processor implementations
- Verify Gemini API is responding correctly
- Review API response in error logs

## Performance Baseline

Expected performance for test suite:

- **Runtime**: 30-60 seconds per test (depends on API response time)
- **API Calls**: 1 per test case
- **Output Size**: 10-50 KB per report
- **Memory Usage**: ~100 MB

## CI/CD Integration

To integrate with GitHub Actions or other CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run DiagnoReport Tests
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  run: |
    python tests/test_runner.py
```

## Manual Testing UI

For manual testing with the web interface:

1. Start local server: `python app.py`
2. Open: `http://localhost:5000`
3. Use sample files from `sample_documents/` folder
4. Test with different report types and formats

## Support

For issues or questions about tests:
- Check test output files for error details
- Review `test_summary.json` for execution details
- Verify sample data in test case JSON files
