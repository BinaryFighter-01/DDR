"""
PDF Document Processor for DiagnoReport
Extracts text and images from inspection and thermal report PDFs
"""

import os
import json
import base64
import io
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from pdf2image import convert_from_path, convert_from_bytes
except ImportError:
    convert_from_path = None

from PIL import Image


class PDFImageExtractor:
    """Extract images from PDF documents"""

    @staticmethod
    def extract_images_from_pdf(pdf_path: str) -> Dict[int, List[Dict]]:
        """
        Extract images from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary mapping page numbers to list of extracted images
        """
        images_by_page = {}
        
        if not fitz:
            raise ImportError("PyMuPDF (fitz) required for PDF processing. Install with: pip install PyMuPDF")
        
        try:
            pdf_document = fitz.open(pdf_path)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                images = []
                
                # Extract images embedded in PDF
                image_list = page.get_images()
                
                for img_index, img_id in enumerate(image_list):
                    try:
                        xref = img_id[0]
                        pix = fitz.Pixmap(pdf_document, xref)
                        
                        # Convert to RGB if needed
                        if pix.n - pix.alpha < 4:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # Save to bytes
                        image_bytes = pix.tobytes("png")
                        
                        # Encode to base64
                        base64_image = base64.b64encode(image_bytes).decode('utf-8')
                        
                        images.append({
                            'index': img_index,
                            'page': page_num + 1,
                            'base64': base64_image,
                            'format': 'png',
                            'source': 'embedded'
                        })
                        
                    except Exception as e:
                        print(f"Error extracting image {img_index} from page {page_num + 1}: {str(e)}")
                        continue
                
                if images:
                    images_by_page[page_num + 1] = images
            
            pdf_document.close()
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
        
        return images_by_page

    @staticmethod
    def extract_images_as_files(pdf_path: str, output_dir: str) -> Dict[int, List[str]]:
        """
        Extract images from PDF and save as files
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save extracted images
            
        Returns:
            Dictionary mapping page numbers to list of image file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        images_by_page = {}
        
        if not fitz:
            raise ImportError("PyMuPDF required for PDF processing")
        
        try:
            pdf_document = fitz.open(pdf_path)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_images = []
                
                image_list = page.get_images()
                
                for img_index, img_id in enumerate(image_list):
                    try:
                        xref = img_id[0]
                        pix = fitz.Pixmap(pdf_document, xref)
                        
                        if pix.n - pix.alpha < 4:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # Save image file
                        image_filename = f"page_{page_num + 1}_image_{img_index}.png"
                        image_path = os.path.join(output_dir, image_filename)
                        pix.save(image_path)
                        
                        page_images.append(image_path)
                        
                    except Exception as e:
                        print(f"Error saving image {img_index} from page {page_num + 1}: {str(e)}")
                        continue
                
                if page_images:
                    images_by_page[page_num + 1] = page_images
            
            pdf_document.close()
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
        
        return images_by_page


class PDFTextExtractor:
    """Extract text from PDF documents"""

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> Dict[str, any]:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not fitz:
            raise ImportError("PyMuPDF required for PDF processing")
        
        extracted_data = {
            'filename': Path(pdf_path).name,
            'total_pages': 0,
            'text_by_page': {},
            'full_text': '',
            'metadata': {}
        }
        
        try:
            pdf_document = fitz.open(pdf_path)
            extracted_data['total_pages'] = len(pdf_document)
            
            # Extract metadata
            if hasattr(pdf_document, 'metadata'):
                extracted_data['metadata'] = pdf_document.metadata
            
            full_text = []
            
            # Extract text from each page
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_text = page.get_text()
                
                extracted_data['text_by_page'][page_num + 1] = page_text
                full_text.append(page_text)
            
            extracted_data['full_text'] = '\n'.join(full_text)
            pdf_document.close()
            
        except Exception as e:
            print(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise
        
        return extracted_data


class PDFDocumentProcessor:
    """Main PDF processor combining text and image extraction"""

    def __init__(self):
        self.text_extractor = PDFTextExtractor()
        self.image_extractor = PDFImageExtractor()

    def process_pdf(self, pdf_path: str, extract_images: bool = True) -> Dict:
        """
        Process PDF file to extract text and images
        
        Args:
            pdf_path: Path to PDF file
            extract_images: Whether to extract images (base64 encoded)
            
        Returns:
            Dictionary with extracted content
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        result = {
            'file': Path(pdf_path).name,
            'path': pdf_path,
            'text_data': {},
            'images': {},
            'success': False
        }
        
        try:
            # Extract text
            result['text_data'] = self.text_extractor.extract_text_from_pdf(pdf_path)
            
            # Extract images if requested
            if extract_images:
                result['images'] = self.image_extractor.extract_images_from_pdf(pdf_path)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            print(f"Error processing PDF {pdf_path}: {str(e)}")
        
        return result

    def process_inspection_report(self, pdf_path: str) -> Dict:
        """
        Process inspection report PDF
        
        Args:
            pdf_path: Path to inspection report PDF
            
        Returns:
            Structured inspection data with extracted text and images
        """
        processed = self.process_pdf(pdf_path)
        
        if not processed['success']:
            return processed
        
        text_data = processed['text_data']['full_text']
        
        # Parse inspection report structure
        inspection_data = {
            'type': 'inspection_report',
            'source_file': Path(pdf_path).name,
            'raw_text': text_data,
            'property_address': self._extract_property_address(text_data),
            'inspection_date': self._extract_inspection_date(text_data),
            'inspector_name': self._extract_inspector_name(text_data),
            'areas': self._extract_areas(text_data),
            'images': processed['images'],
            'text_by_page': processed['text_data']['text_by_page']
        }
        
        return inspection_data

    def process_thermal_report(self, pdf_path: str) -> Dict:
        """
        Process thermal report PDF
        
        Args:
            pdf_path: Path to thermal report PDF
            
        Returns:
            Structured thermal data with extracted text and images
        """
        processed = self.process_pdf(pdf_path)
        
        if not processed['success']:
            return processed
        
        text_data = processed['text_data']['full_text']
        
        # Parse thermal report structure
        thermal_data = {
            'type': 'thermal_report',
            'source_file': Path(pdf_path).name,
            'raw_text': text_data,
            'property_address': self._extract_property_address(text_data),
            'inspection_date': self._extract_inspection_date(text_data),
            'findings': self._extract_thermal_findings(text_data),
            'images': processed['images'],
            'text_by_page': processed['text_data']['text_by_page']
        }
        
        return thermal_data

    @staticmethod
    def _extract_property_address(text: str) -> str:
        """Extract property address from text"""
        # Common patterns for property address
        patterns = [
            r'(?:Address|Property|Location)[:\s]+([^\n]+)',
            r'(\d+\s+[a-zA-Z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[^\n]*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not Available"

    @staticmethod
    def _extract_inspection_date(text: str) -> str:
        """Extract inspection date from text"""
        # Common date patterns
        patterns = [
            r'(?:Inspection\s+)?[Dd]ate[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return "Not Available"

    @staticmethod
    def _extract_inspector_name(text: str) -> str:
        """Extract inspector name from text"""
        patterns = [
            r'(?:Inspector|Inspected\s+by)[:\s]+([A-Za-z\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not Available"

    @staticmethod
    def _extract_areas(text: str) -> List[Dict]:
        """Extract inspection areas/sections from text"""
        areas = []
        
        # Common area patterns
        area_keywords = [
            'roof', 'walls', 'foundation', 'hvac', 'plumbing', 
            'electrical', 'attic', 'basement', 'exterior', 'interior',
            'windows', 'doors', 'flooring', 'kitchen', 'bathroom'
        ]
        
        # Split text into sections
        sections = re.split(r'\n(?=\d+\.|[A-Z][A-Z\s]+)', text)
        
        for section in sections:
            if len(section.strip()) < 20:
                continue
            
            # Check if section contains area keyword
            for keyword in area_keywords:
                if keyword.lower() in section.lower():
                    # Extract observations and issues
                    observations = []
                    issues = []
                    
                    lines = section.split('\n')
                    for line in lines[1:]:  # Skip header
                        line = line.strip()
                        if line and len(line) > 5:
                            if any(word in line.lower() for word in ['issue', 'problem', 'concern', 'damaged', 'defect']):
                                issues.append(line)
                            else:
                                observations.append(line)
                    
                    if observations or issues:
                        areas.append({
                            'name': keyword.title(),
                            'description': keyword.title(),
                            'observations': observations[:5],
                            'issues': issues[:5]
                        })
                    break
        
        return areas if areas else [{'name': 'General', 'description': 'General Observations', 'observations': [], 'issues': []}]

    @staticmethod
    def _extract_thermal_findings(text: str) -> List[Dict]:
        """Extract thermal analysis findings from text"""
        findings = []
        
        # Look for temperature ranges and analysis
        temp_pattern = r'(\d+)\s*°?C.*?(?=\d+\s*°?C|$)'
        matches = re.findall(temp_pattern, text)
        
        if matches:
            findings.append({
                'area': 'General Thermal Analysis',
                'temperature_range': f"{min(matches)}-{max(matches)}°C",
                'analysis': 'Thermal imaging analysis indicates temperature variations across property',
                'anomalies': [],
                'severity': 'MEDIUM'
            })
        
        # Look for specific findings
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in ['finding', 'anomaly', 'hotspot', 'cold spot', 'thermal']):
                findings.append({
                    'area': line.strip(),
                    'temperature_range': 'Not Available',
                    'analysis': lines[i+1].strip() if i+1 < len(lines) else 'Not Available',
                    'anomalies': [],
                    'severity': 'MEDIUM'
                })
        
        return findings if findings else [{'area': 'Thermal Analysis', 'temperature_range': 'Not Available', 'analysis': text[:200], 'anomalies': [], 'severity': 'MEDIUM'}]


def load_documents(inspection_pdf: str, thermal_pdf: str) -> Tuple[Dict, Dict]:
    """
    Load and process both inspection and thermal PDFs
    
    Args:
        inspection_pdf: Path to inspection report PDF
        thermal_pdf: Path to thermal report PDF
        
    Returns:
        Tuple of (inspection_data, thermal_data)
    """
    processor = PDFDocumentProcessor()
    
    inspection_data = processor.process_inspection_report(inspection_pdf)
    thermal_data = processor.process_thermal_report(thermal_pdf)
    
    return inspection_data, thermal_data


if __name__ == '__main__':
    # Test the PDF processor
    import json
    
    processor = PDFDocumentProcessor()
    
    sample_dir = Path(__file__).parent.parent / 'sample_documents'
    inspection_pdf = sample_dir / 'Sample Report.pdf'
    thermal_pdf = sample_dir / 'Thermal Images.pdf'
    
    if inspection_pdf.exists() and thermal_pdf.exists():
        print("Processing sample documents...")
        inspection, thermal = load_documents(str(inspection_pdf), str(thermal_pdf))
        
        print("\n=== Inspection Report ===")
        print(f"Property: {inspection.get('property_address')}")
        print(f"Date: {inspection.get('inspection_date')}")
        print(f"Areas found: {len(inspection.get('areas', []))}")
        print(f"Images extracted: {len(inspection.get('images', {}))}")
        
        print("\n=== Thermal Report ===")
        print(f"Property: {thermal.get('property_address')}")
        print(f"Date: {thermal.get('inspection_date')}")
        print(f"Findings: {len(thermal.get('findings', []))}")
        print(f"Images extracted: {len(thermal.get('images', {}))}")
    else:
        print(f"Sample PDFs not found in {sample_dir}")
