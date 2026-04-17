# DiagnoReport Testing Quick Start

## Get Started in 30 Seconds

### 1. Set Your API Key
```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows Command Prompt
set GEMINI_API_KEY=your-api-key-here
```

### 2. Run Tests

**Linux/Mac:**
```bash
bash tests/run_tests.sh
```

**Windows:**
```bash
tests\run_tests.bat
```

**Or directly with Python:**
```bash
python tests/test_runner.py
```

## What Gets Tested

✅ **Residential Property** (Good Condition)
- Modern home in excellent condition
- Validates report generation for well-maintained property

✅ **Commercial Property** (Needs Maintenance)
- Office building with multiple issues
- Validates detailed analysis and prioritized recommendations

## Test Outputs

After running tests, you'll find:

- `tests/output_*.json` - Generated diagnostic reports
- `tests/test_summary.json` - Test execution summary with pass/fail status

## What's Being Validated

Each test validates:
- ✓ All 7 required report sections
- ✓ Proper data structure and formatting
- ✓ Logical analysis and recommendations
- ✓ API integration and response handling

## Example Output

```json
{
  "executive_summary": "Property inspection...",
  "property_details": { ... },
  "inspection_findings": { ... },
  "thermal_analysis": { ... },
  "integrated_analysis": { ... },
  "recommendations": [ ... ],
  "conclusion": "..."
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GEMINI_API_KEY not set" | Set environment variable first |
| API timeout errors | Check internet connection, retry |
| Missing sections | Verify Gemini API is responding |
| Permission denied (Mac/Linux) | Run: `chmod +x tests/run_tests.sh` |

## Learn More

See `tests/README.md` for:
- Detailed test documentation
- Adding custom test cases
- CI/CD integration
- Performance benchmarks

---

**Next Steps:**
1. Run tests to validate setup
2. Review generated reports in `tests/` folder
3. Check `tests/test_summary.json` for detailed results
