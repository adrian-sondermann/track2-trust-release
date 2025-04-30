import fitz  # PyMuPDF

class PDFRedactor:
    @staticmethod
    def redact_sections(pdf_path, sensitive_sections, output_path=None):
        if output_path is None:
            output_path = "redacted_" + pdf_path.split("/")[-1]

        doc = fitz.open(pdf_path)

        for page in doc:
            for section in sensitive_sections:
                value_to_redact = section.get('sensitive_value') or section['text']
                if not value_to_redact or not value_to_redact.strip():
                    continue 
                matches = page.search_for(value_to_redact)
                for match in matches:
                    page.add_redact_annot(match, fill=(0, 0, 0))  # schwarze Schwärzung
            page.apply_redactions()

        doc.save(output_path)
        doc.close()
