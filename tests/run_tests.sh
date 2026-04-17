#!/bin/bash
# DiagnoReport Test Runner Script
# Quick start for running the test suite

echo "======================================================"
echo "DiagnoReport - Test Suite Execution"
echo "======================================================"
echo ""

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY environment variable not set"
    echo ""
    echo "Please set your Gemini API key:"
    echo "  export GEMINI_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your free API key from:"
    echo "  https://aistudio.google.com/app/apikeys"
    exit 1
fi

echo "✓ GEMINI_API_KEY is set"
echo ""

# Check if running from correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "✓ Project structure verified"
echo ""

# Install/update dependencies
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run tests
echo "🚀 Running DiagnoReport Test Suite..."
echo "======================================================"
echo ""

python tests/test_runner.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================"
    echo "✓ Test suite completed successfully"
    echo ""
    echo "📊 Test Results Summary:"
    if [ -f "tests/test_summary.json" ]; then
        echo "  See: tests/test_summary.json"
    fi
    echo ""
    echo "📄 Generated Reports:"
    ls -lh tests/output_*.json 2>/dev/null | awk '{print "  " $9}'
    echo ""
else
    echo ""
    echo "======================================================"
    echo "❌ Test suite failed"
    exit 1
fi

echo "======================================================"
