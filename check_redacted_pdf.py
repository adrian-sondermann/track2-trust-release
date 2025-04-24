import fitz  # PyMuPDF
import sys
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"❌ Datei nicht gefunden: {pdf_path}")
        return

    print(f"📂 Lese Datei: {pdf_path}\n")

    with fitz.open(pdf_path) as doc:
        full_text = ""
        for page_num, page in enumerate(doc):
            text = page.get_text()
            print(f"\n🧾 --- Seite {page_num + 1} ---")
            if text.strip():
                print(text)
            else:
                print("✅ Kein maschinenlesbarer Text gefunden.")
            full_text += text

        if not full_text.strip():
            print("\n🎉 Die gesamte PDF enthält **keinen maschinenlesbaren Text**.")
        else:
            print("\n⚠️ **Achtung:** Es wurde noch Text gefunden. Bitte Schwärzung prüfen.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ Nutzung: python check_redacted_pdf.py <pfad_zur_pdf>")
    else:
        extract_text_from_pdf(sys.argv[1])

# python check_redacted_pdf.py redacted_mein_dokument.pdf
