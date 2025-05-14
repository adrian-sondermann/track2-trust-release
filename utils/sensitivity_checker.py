import json

from config import SENSITIVITY_RULES
import re
from typing import Any

class SensitivityChecker:
    @staticmethod
    def check_document(text_content: list[str], ai_processor) -> list[dict[str, Any]]:
        """
        Check document content for sensitive information.
        Returns list of sensitive sections with their categories and locations.
        """
        sensitive_sections = []
        
        # Process each page
        for page_num, page_text in enumerate(text_content):
            analysis = ai_processor.analyze_text(page_text)

            try:
                results = SensitivityChecker.extract_json_from_response(analysis)
                for section in results.get('sensitive_sections', []):
                    sensitive_sections.append({
                        'page_num': page_num,
                        'text': section['text'],
                        'category': section['category'],
                        'reason': section['reason'],
                        'accepted': True  # Can be updated by user
                    })
            except json.JSONDecodeError:
                print(f"Error parsing AI response for page {page_num}")
            except ValueError as e:
                print(f"Error extracting JSON from response. Eror: {e} for response: {analysis}")
        
        return sensitive_sections 
    
    @staticmethod
    def extract_json_from_response(raw_response: str) -> dict:
        """
        Extract JSON from the raw response string, e.g. for markdown-formatted 
        strings. This is a utility function to clean up the response.
        
        Args:
            raw_response (str): The raw response string from the AI model.
        Returns:
            dict: A dictionary containing the extracted JSON data.
        """
        # Use regex to greedily match from the first '{' to the last '}' in the string
        pattern = re.search(r'\{.*\}', raw_response, re.DOTALL)

        if pattern:
            # Extract the JSON string and load it
            json_response = pattern.group(0)
            json_data = json.loads(json_response)
            return json_data
        else:
            raise ValueError("No JSON found in the response string.")

def find_sensitive_info(text):
    sensitive_ranges = []
    
    # Patterns for sensitive information
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
    }
    
    for sensitivity_type, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            sensitive_ranges.append({
                'start': match.start(),
                'end': match.end(),
                'type': sensitivity_type,
                'text': match.group()
            })
    
    return sensitive_ranges 