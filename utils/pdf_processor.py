import PyPDF2
try:
    from pdf2image import convert_from_path
except ImportError:
    raise ImportError("pdf2image is required. Please install it using: pip install pdf2image")
from PIL import Image, ImageDraw
import io
import tempfile
from utils.sensitivity_checker import find_sensitive_info
#import fitz  # PyMuPDF for PDF manipulation

class PDFProcessor:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

    @staticmethod
    def extract_text(pdf_file) -> list[str]:
        """Extract text from PDF with size validation."""
        # Check file size
        pdf_file.seek(0, 2)  # Go to end of file
        file_size = pdf_file.tell()  # Get current position (file size)
        pdf_file.seek(0)  # Go back to start
        
        if file_size > PDFProcessor.MAX_FILE_SIZE:
            raise ValueError(f"File too large. Maximum size is {PDFProcessor.MAX_FILE_SIZE/1024/1024}MB")
            
        reader = PyPDF2.PdfReader(pdf_file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return text

    @staticmethod
    def redact_pdf(pdf_path, sensitive_areas):
        """
        Redact sensitive areas in the PDF.
        sensitive_areas: list of dicts with page_num, coordinates (x1,y1,x2,y2)
        """
        # Convert PDF to images
        images = PDFProcessor.convert_pdf_to_images(pdf_path)
        
        # Redact each page
        redacted_images = []
        for i, image in enumerate(images):
            draw = ImageDraw.Draw(image)
            page_areas = [area for area in sensitive_areas if area['page_num'] == i]
            
            for area in page_areas:
                draw.rectangle(
                    [area['x1'], area['y1'], area['x2'], area['y2']], 
                    fill='black'
                )
            redacted_images.append(image)
        
        # Convert back to PDF
        output_pdf = io.BytesIO()
        redacted_images[0].save(
            output_pdf, 
            'PDF', 
            save_all=True, 
            append_images=redacted_images[1:]
        )
        return output_pdf 

    @staticmethod
    def convert_pdf_to_images(pdf_path):
        try:
            return convert_from_path(pdf_path)
        except Exception as e:
            if "poppler" in str(e).lower():
                raise Exception(
                    "Poppler is not installed or not in PATH.\n"
                    "Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/ "
                    "and add bin directory to PATH\n"
                    "Linux: sudo apt-get install poppler-utils\n"
                    "MacOS: brew install poppler"
                )
            raise e 



def process_pdf(file_path):
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        full_text = ""
        page_offsets = [0]  # Track the starting position of each page
        
        # Extract text while keeping track of character positions
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            full_text += page_text
            page_offsets.append(len(full_text))
            
        # Get sensitive information with positions
        sensitive_ranges = find_sensitive_info(full_text)
        
        return {
            'text': full_text,
            'sensitive_ranges': sensitive_ranges,
            'success': True
        }
    except Exception as e:
        return {
            'text': '',
            'sensitive_ranges': [],
            'success': False,
            'error': str(e)
        } 