import os
import tempfile
import time

def cleanup_temp_pdfs(max_age_seconds=3600):
    temp_dir = tempfile.gettempdir()
    now = time.time()

    for filename in os.listdir(temp_dir):
        if filename.endswith(".pdf"):  # alle PDFs erfassen
            file_path = os.path.join(temp_dir, filename)
            try:
                file_mtime = os.path.getmtime(file_path)
                file_age = now - file_mtime

                # Löschen nur, wenn Datei älter als max_age_seconds (z.B. 3600 Sekunden = 1 Stunde)
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    print(f"Deleted old temp file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")


