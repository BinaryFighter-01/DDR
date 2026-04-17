"""
DiagnoReport Test Utilities
Test runner and validation functions for DiagnoReport system
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.document_processor import DocumentProcessor
from backend.gemini_processor import GeminiProcessor
from backend.ddr_generator import DDRGenerator


class DiagnoReportTestRunner:
    """Test runner for DiagnoReport generation"""

    def __init__(self, api_key=None):
        """
        Initialize test runner
        
        Args:
            api_key: Gemini API key (uses env var if not provided)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        self.test_dir = Path(__file__).parent
        self.results = []

    def load_test_case(self, filename):
        """Load a test case from JSON file"""
        filepath = self.test_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Test case not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)

    def run_test(self, test_name, test_case_file):
        """
        Run a single test case
        
        Args:
            test_name: Display name for test
            test_case_file: Filename of test case
            
        Returns:
            dict: Test result with status and report
        """
        try:
            print(f"\n{'='*60}")
            print(f"Running Test: {test_name}")
            print(f"{'='*60}")
            
            # Load test case
            test_case = self.load_test_case(test_case_file)
            inspection = test_case.get('inspection_report', {})
            thermal = test_case.get('thermal_report', {})
            
            print(f"Property: {inspection.get('property_address', 'Unknown')}")
            print(f"Inspection Date: {inspection.get('inspection_date', 'Unknown')}")
            
            # Generate DDR
            print("\nGenerating Diagnostic Report...")
            gemini = GeminiProcessor(self.api_key)
            ddr_gen = DDRGenerator(gemini)
            ddr = ddr_gen.generate_complete_ddr(inspection, thermal)
            
            # Validate structure
            required_sections = [
                'executive_summary',
                'property_details',
                'inspection_findings',
                'thermal_analysis',
                'integrated_analysis',
                'recommendations',
                'conclusion'
            ]
            
            missing_sections = [s for s in required_sections if s not in ddr]
            
            status = "PASSED" if not missing_sections else "FAILED"
            
            result = {
                'test_name': test_name,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'property': inspection.get('property_address'),
                'missing_sections': missing_sections,
                'report_keys': list(ddr.keys()),
                'report_preview': {
                    'summary': str(ddr.get('executive_summary', ''))[:200] + '...'
                }
            }
            
            print(f"\nResult: {status}")
            if missing_sections:
                print(f"Missing sections: {missing_sections}")
            else:
                print("All required sections present ✓")
            
            # Save report
            output_file = self.test_dir / f"output_{test_name.replace(' ', '_')}.json"
            with open(output_file, 'w') as f:
                json.dump(ddr, f, indent=2)
            print(f"Report saved to: {output_file}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test_name': test_name,
                'status': 'ERROR',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            print(f"\nResult: ERROR")
            print(f"Error: {str(e)}")
            self.results.append(result)
            return result

    def run_all_tests(self):
        """Run all available test cases"""
        tests = [
            ('Residential Property - Good Condition', 'test_case_residential.json'),
            ('Commercial Property - Needs Maintenance', 'test_case_commercial.json'),
        ]
        
        for test_name, test_file in tests:
            self.run_test(test_name, test_file)

    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.results if r['status'] == 'FAILED')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        
        print("\nDetailed Results:")
        for result in self.results:
            status_symbol = "✓" if result['status'] == 'PASSED' else "✗"
            print(f"{status_symbol} {result['test_name']}: {result['status']}")
            if 'error' in result:
                print(f"  Error: {result['error']}")
            if result.get('missing_sections'):
                print(f"  Missing: {result['missing_sections']}")
        
        # Save summary
        summary_file = self.test_dir / 'test_summary.json'
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total': total,
                'passed': passed,
                'failed': failed,
                'errors': errors,
                'results': self.results
            }, f, indent=2)
        print(f"\nSummary saved to: {summary_file}")


def main():
    """Main test execution"""
    print("DiagnoReport Test Suite")
    print("="*60)
    
    try:
        runner = DiagnoReportTestRunner()
        runner.run_all_tests()
        runner.print_summary()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set GEMINI_API_KEY environment variable:")
        print("  Windows: set GEMINI_API_KEY=your-key")
        print("  Linux/Mac: export GEMINI_API_KEY=your-key")
        sys.exit(1)
    except Exception as e:
        print(f"Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
