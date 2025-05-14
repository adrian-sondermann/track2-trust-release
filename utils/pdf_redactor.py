import fitz  # PyMuPDF

class PDFRedactor:
    @staticmethod
    def redact_sections(sensitive_sections: list, pdf_path: str, output_path: str=None) -> None:
        '''
        Schwaerzt alle Woerter aus sensitive_sections in einem PDF.
        Args: 
            sensitive_sections (list): Liste mit Informationen, die geschwaerzt werden sollen.
            pdf_path (str): Pfad zur Eingabe-PDF.
            output_path (str): Pfad zur Ausgabe-PDF.
        
        '''
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
                    page.add_redact_annot(match, fill=(0, 0, 0))  # Schwarzer Hintergrund
            page.apply_redactions() # Anwenden der Schwärzung

        # Geändertes PDF speichern
        doc.save(output_path)
        doc.close()
