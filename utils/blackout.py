import fitz  # PyMuPDF

class Blackout:

    @staticmethod
    def redact_sentences(text_array, file_input_path, file_output_path):
        """
        Schwaerzt alle Woerter aus text_array in einem PDF.
        
        :param text_array: Liste mit Saetzen/Woertern, die geschwaerzt werden sollen.
        :param file_input_path: Pfad zur Eingabe-PDF.
        :param file_output_path: Pfad zur Ausgabe-PDF.
        """
        # PDF oeffnen
        doc = fitz.open(file_input_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            words = page.get_text("words")  # Alle Woerter mit Positionen
            blocks = page.get_text("blocks")  # Alle Textbloecke mit Positionen
            full_text = page.get_text("text")  # Gesamter Text der Seite

            for sentence in text_array:
                if sentence in full_text:
                    print(f"Satz gefunden: '{sentence}' auf Seite {page_num+1}")

                    # Satz in Woerter zerlegen
                    sentence_words = sentence.split()

                    # Suche den passenden Textblock
                    for block in blocks:
                        x0, y0, x1, y1, block_text, _, _ = block

                        if sentence in block_text:
                            print(f"Textblock gefunden fuer '{sentence}' auf Seite {page_num+1}")

                            # Schwaerze jedes Wort im Block, wenn es zum Satz geh�rt
                            for word in words:
                                wx0, wy0, wx1, wy1, text, _, _, _ = word

                                # Pruefen, ob das Wort in diesem Satz enthalten ist und im Block liegt
                                if text in sentence_words and (x0 <= wx0 <= x1 and y0 <= wy0 <= y1):
                                    print(f"Schwaerze Wort: {text} auf Seite {page_num+1}")
                                    word_rect = fitz.Rect(wx0, wy0, wx1, wy1)
                                    page.add_redact_annot(word_rect, fill=(0, 0, 0))  # Schwarzer Hintergrund
            page.apply_redactions()  # Anwenden der Schw�rzung

        # Geaendertes PDF speichern
        doc.save(file_output_path)
        doc.close()

