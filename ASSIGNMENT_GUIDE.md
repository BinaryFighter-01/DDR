# DiagnoReport - Assignment Submission Guide

## Project Overview

**DiagnoReport** is an AI-powered diagnostic report generation system that:
- Extracts text and images from PDF inspection and thermal reports
- Intelligently merges data from multiple sources
- Generates comprehensive, structured Detailed Diagnostic Reports (DDR)
- Places extracted images in appropriate sections
- Handles missing or conflicting data gracefully

## Submission Checklist

### ✅ Working Output
- [x] Live project: http://localhost:5000 (local deployment)
- [x] GitHub Repository: https://github.com/YOUR_USERNAME/diagnoreport
- [x] Docker deployment ready
- [x] Vercel deployment configuration included

### ✅ Technical Requirements

#### 1. Text & Image Extraction ✓
```python
# Extract from PDFs
from backend.pdf_processor import PDFDocumentProcessor
processor = PDFDocumentProcessor()
inspection = processor.process_inspection_report('Sample Report.pdf')
thermal = processor.process_thermal_report('Thermal Images.pdf')
# Result: {text_data, images}
```

#### 2. Data Merging ✓
```python
# Intelligent merging
from backend.enhanced_ddr_generator import EnhancedDDRGenerator
generator = EnhancedDDRGenerator(gemini_processor)
ddr = generator.generate_complete_ddr(inspection, thermal)
# Result: Merged 7-section DDR with images
```

#### 3. DDR Structure (7 Sections) ✓
1. **Property Issue Summary** - Overview with statistics
2. **Area-wise Observations** - Detailed findings with extracted images
3. **Probable Root Causes** - Cause analysis with evidence
4. **Severity Assessment** - Issue prioritization with reasoning
5. **Recommended Actions** - Priority-ordered recommendations
6. **Additional Notes** - Quality and reliability assessment
7. **Missing Information** - Explicit "Not Available" notations

#### 4. Image Placement ✓
- Images extracted from PDFs
- Placed in relevant area sections
- Fallback: "Image Not Available" when missing
- Base64 encoding for web display
- Proper image sourcing documented

#### 5. Error Handling ✓
- Missing data: Marked as "Not Available"
- Conflicting data: Noted with conflict indicator
- Duplicate avoidance: De-duplication logic
- Generalized approach: Pattern-based extraction

## Quick Start (30 seconds)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run System
```bash
# Option A: Web Interface
python app_enhanced.py
# Open: http://localhost:5000

# Option B: Process Samples Directly
python api/process_pdf.py

# Option C: Run Tests
python tests/test_runner.py
```

## System Architecture

```
INPUT (PDFs)
    ↓
[PDF Text Extraction] → Full text content
[PDF Image Extraction] → Base64 images
    ↓
[Data Parsing] → Parse properties, areas, findings
    ↓
[Data Merging] → Combine inspection + thermal
    ↓
[DDR Generation] → Create 7-section report
    ↓
[Image Placement] → Place images in sections
    ↓
OUTPUT (JSON/HTML with images)
```

## File Organization

### Core System
```
backend/
├── pdf_processor.py          # PDF text/image extraction
├── enhanced_ddr_generator.py # DDR report generation
├── document_processor.py     # JSON data processing
└── gemini_processor.py       # AI analysis

api/
├── process_pdf.py            # PDF processing API
├── generate_ddr.py           # Report generation endpoint
└── health.py                 # System health check

frontend/
└── index.html                # Web interface
```

### Sample Data
```
sample_documents/
├── Sample Report.pdf         # Inspection report (text + images)
├── Thermal Images.pdf        # Thermal report (text + images)
├── inspection_report.json    # JSON backup
└── thermal_report.json       # JSON backup
```

### Testing & Documentation
```
tests/
├── test_runner.py            # Test execution
├── test_case_residential.json
├── test_case_commercial.json
└── README.md

docs/
├── PDF_IMAGE_PROCESSING.md   # Technical details
├── QUICKSTART.md             # Quick reference
└── API_EXAMPLES.md           # API usage examples
```

## Key Features Demonstrated

### Feature 1: PDF Processing
```python
# Reads Sample Report.pdf and Thermal Images.pdf
# Extracts:
# - Complete text content
# - All embedded images
# - Page associations
```

### Feature 2: Image Extraction & Embedding
```python
# Extracts images as base64
# Places in relevant sections:
# {
#   "area_name": "Roof",
#   "images": [
#     {
#       "data": "iVBORw0KGgoAAAA...",
#       "format": "png",
#       "page": 1
#     }
#   ]
# }
```

### Feature 3: Intelligent Merging
```python
# Combines data:
inspection_issues + thermal_findings = comprehensive_analysis
# Avoids duplicates
# Identifies conflicts
# Prioritizes findings
```

### Feature 4: Error Handling
```python
# Missing data → "Not Available"
# Conflicts → Documented with reasoning
# Incomplete reports → Flags identified items
# Generic patterns → Works across similar reports
```

## Testing the System

### Test Case 1: Sample PDFs
```bash
python api/process_pdf.py
# Processes: Sample Report.pdf + Thermal Images.pdf
# Output: DDR with extracted images
```

### Test Case 2: JSON Files
```bash
# Use test cases from tests/ folder
python tests/test_runner.py
```

### Test Case 3: Manual Upload
```bash
# Visit http://localhost:5000
# Upload PDF files
# View generated report
```

## Output Examples

### JSON Format
```json
{
  "generated_at": "2026-04-17T15:30:00",
  "property_issue_summary": {
    "total_issues_found": 8,
    "client_summary": "Property shows...",
    "images_extracted": 5
  },
  "area_wise_observations": [
    {
      "area_name": "Roof",
      "issues": ["Missing shingles", "Flashing issues"],
      "images": [{"data": "base64...", "page": 1}]
    }
  ],
  "recommended_actions": [
    {
      "action": "Replace missing roof shingles",
      "priority": "critical",
      "timeline": "Within 2 weeks"
    }
  ]
}
```

### HTML Format
- Professional formatting with CSS
- Embedded images in sections
- Interactive tabs
- Responsive design
- Export capabilities

## Generalization (Works on Similar Reports)

### Pattern-Based Extraction
- Detects areas: roof, walls, HVAC, plumbing, etc.
- Identifies issues via keyword matching
- Extracts dates and addresses via regex
- No hardcoding for specific reports

### Flexible Data Handling
- Handles various PDF formats
- Works with partial data
- Adapts to different report structures
- Scales with document size

## Limitations & Considerations

### Documented Limitations
1. PDF text must be searchable (not scanned images)
2. Layout variations may affect parsing
3. Image extraction dependent on PDF embedding
4. Complex tables may parse imperfectly
5. Multilingual content requires additional setup

### How We Handle Them
- Clear "Not Available" notations
- Conflict detection and reporting
- Fallback mechanisms
- Detailed logging
- Manual review recommendations

## Deployment Options

### Option 1: Local (Testing)
```bash
python app_enhanced.py
```

### Option 2: Docker
```bash
docker build -t diagnoreport .
docker run -p 5000:5000 diagnoreport
```

### Option 3: Vercel
```bash
vercel deploy
# See: vercel.json configuration
```

### Option 4: Cloud Run
```bash
gcloud run deploy diagnoreport --source .
```

## Code Quality

### Modularity
- Separate processors for PDF, text, images
- Independent DDR generation
- Pluggable AI providers
- Clean API interfaces

### Error Handling
- Try-except blocks with specific errors
- Graceful degradation
- Comprehensive logging
- User-friendly error messages

### Documentation
- Inline code comments
- Docstrings on all classes/functions
- README files in each directory
- API documentation
- Assignment guide (this file)

## For Evaluators

### Run the System
1. `pip install -r requirements.txt`
2. `export GEMINI_API_KEY="..."`
3. `python api/process_pdf.py` → See live processing
4. `python app_enhanced.py` → Web interface
5. Visit http://localhost:5000

### Verify Features
- ✓ PDF text extraction: Check console output
- ✓ Image extraction: Check images in JSON
- ✓ Data merging: Compare input/output correlation
- ✓ DDR structure: Review all 7 sections
- ✓ Image placement: View HTML report
- ✓ Error handling: See "Not Available" notations

### View Output
- JSON: `api/process_pdf.py` output
- HTML: Rendered at http://localhost:5000
- Test results: `tests/test_summary.json`

## Key Achievements

✅ **Extracts text from PDFs** - Full implementation with PyMuPDF
✅ **Extracts images from PDFs** - Base64 encoding for web display
✅ **Merges inspection + thermal** - Intelligent data combination
✅ **Avoids duplicates** - De-duplication logic implemented
✅ **Handles conflicts** - Conflict detection documented
✅ **Handles missing data** - "Not Available" markers
✅ **Generates 7-section DDR** - Complete structure
✅ **Places images in sections** - Relevant placement logic
✅ **Client-friendly format** - HTML and JSON outputs
✅ **Generalizes to similar reports** - Pattern-based extraction

## Submission Contents

### GitHub Repository
- ✓ Full source code
- ✓ Sample PDFs
- ✓ Test cases
- ✓ Documentation
- ✓ Configuration files

### Loom Video (3-5 min)
- What was built: DiagnoReport system overview
- How it works: Architecture and data flow
- Limitations: Known constraints and handling
- Improvements: Potential enhancements

### Live Demo / Screenshots
- Web interface screenshot
- PDF upload example
- Generated report example
- HTML/JSON output examples

## Contact & Support

For questions about the implementation:
- Review PDF_IMAGE_PROCESSING.md for technical details
- Check API_EXAMPLES.md for usage examples
- See tests/README.md for testing guide
- Review source code comments for implementation details

---

**Project**: DiagnoReport - AI-Powered Diagnostic Report Generator
**Version**: 2.0 with PDF & Image Processing
**Status**: Production-Ready
**Created**: April 2026
