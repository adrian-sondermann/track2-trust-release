import streamlit as st
import tempfile
import os
import uuid  # <-- Added to generate new keys for file uploader
from utils.pdf_processor import PDFProcessor
from utils.sensitivity_checker import SensitivityChecker
from utils.common import initialize_page
#from utils.blackout import Blackout
from utils.pdf_redactor import PDFRedactor
from utils.cleanup import cleanup_temp_pdfs

st.set_page_config(
    page_title="PDF Checker",
    page_icon="🔍",
    layout="wide"
)

lang = initialize_page()


def main():
    # Translated texts for each language
    translations = {
        "English": {
            "title": "PDF Sensitivity Checker",
            "subtitle": "Upload PDFs to check for sensitive information according to GDPR and IFG. Please confirm the identified sections and apply the changes to the document.",
            "model_choice": "Select AI Model",
            "model_help": "Select Albert as the more secure model optimized for administrative tasks in french.",
            "upload_label": "Upload PDF documents",
            "processing": "Processing {}...",
            "no_sensitive": "No sensitive information detected",
            "found_sensitive": "Found sensitive information:",
            "review_title": "Review Sensitive Information:",
            "section": "Section",
            "category": "Category",
            "text": "Text",
            "reason": "Reason",
            "confirm": "Confirm",
            "clear_all": "Clear All",
            "apply": "Apply to Document",
            "risk_low": "Overall Assessment: Low Sensitivity",
            "risk_medium": "Overall Assessment: Medium Sensitivity",
            "risk_high": "Overall Assessment: High Sensitivity",
            "applying_redactions": "Applying redactions...",
            "download_redacted": "Download Redacted Document"
        },
        "Deutsch": {
            "title": "PDF Sensitivitätsprüfer",
            "subtitle": "Laden Sie PDFs hoch, um sie auf sensible Informationen gemäß DSGVO und IFG zu prüfen. Bitte bestätigen Sie die identifizierten Abschnitte und wenden Sie die Änderungen auf das Dokument an.",
            "model_choice": "KI-Modell auswählen",
            "model_help": "Wählen Sie Albert als sichereres Modell, das für administrative Aufgaben auf Französisch optimiert ist.",
            "upload_label": "PDF-Dokumente hochladen",
            "processing": "Verarbeite {}...",
            "no_sensitive": "Keine sensiblen Informationen gefunden",
            "found_sensitive": "Gefundene sensible Informationen:",
            "review_title": "Sensible Informationen überprüfen:",
            "section": "Abschnitt",
            "category": "Kategorie",
            "text": "Text",
            "reason": "Grund",
            "confirm": "Bestätigen",
            "clear_all": "Alles löschen",
            "apply": "Auf Dokument anwenden",
            "risk_low": "Gesamtbewertung: Niedriges Risiko",
            "risk_medium": "Gesamtbewertung: Mittleres Risiko",
            "risk_high": "Gesamtbewertung: Hohes Risiko",
            "applying_redactions": "Redaktion anwenden...",
            "download_redacted": "Redigiertes Dokument herunterladen"
        },
        "Français": {
            "title": "Vérificateur de sensibilité PDF",
            "subtitle": "Téléchargez des PDF pour vérifier les informations sensibles selon le RGPD et l'IFG. Veuillez confirmer les sections identifiées et appliquer les modifications au document.",
            "model_choice": "Sélectionner le modèle IA",
            "model_help": "Sélectionnez Albert comme modèle plus sécurisé optimisé pour les tâches administratives en français.",
            "upload_label": "Télécharger des documents PDF",
            "processing": "Traitement de {}...",
            "no_sensitive": "Aucune information sensible détectée",
            "found_sensitive": "Informations sensibles trouvées :",
            "review_title": "Examiner les informations sensibles :",
            "section": "Section",
            "category": "Catégorie",
            "text": "Texte",
            "reason": "Raison",
            "confirm": "Confirmer",
            "clear_all": "Tout effacer",
            "apply": "Appliquer au document",
            "risk_low": "Évaluation globale : Risque faible",
            "risk_medium": "Évaluation globale : Risque moyen",
            "risk_high": "Évaluation globale : Risque élevé",
            "applying_redactions": "Appliquer la rédaction...",
            "download_redacted": "Télécharger le document rédigé"
        }
    }

    # Choose the appropriate translation based on the selected language
    t = translations[lang]

    st.title(t["title"])
    st.write(t["subtitle"])

    # Model selection
    model_options = {
        "Azure Open AI: gpt-4o 2024-11-20": "Azure Open AI", 
        "Portal: microsoft/phi-4": "Portal"
    }
    model_choice_label = st.selectbox(
        t["model_choice"],
        options=list(model_options.keys()),
        index=1,
        # help=t["model_help"]
    )
    model_choice = model_options[model_choice_label]

    # Info-Banner einfügen
    #if model_choice == "Azure Open AI":
    #    st.info("Azure Open AI nutzt derzeit GPT-4o.", icon="ℹ️")
    #elif model_choice == "Portal":
    #    st.warning("Die Modelle im Portal befinden sich derzeit in der Entwicklung. Es kann zu unvollständigen oder fehlerhaften Erkennungen kommen.", icon="⚠️")

    # Initialize session state
    if 'processed_docs' not in st.session_state:
        # 🧹 Temp-Ordner aufräumen
        cleanup_temp_pdfs()
        st.session_state["processed_docs"] = {}
    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = "uploader_initial"

    uploaded_files = st.file_uploader(
        t["upload_label"],
        type="pdf",
        accept_multiple_files=True,
        key=st.session_state['uploader_key']
    )

    if uploaded_files:
        # Conditionally instantiate the AI processor based on selection
        if model_choice == "Azure Open AI":
            from utils.azure_ai import AzureAIProcessor
            ai_processor = AzureAIProcessor()
        elif model_choice == "Portal":
            from utils.portal_ai import PortalAIProcessor
            ai_processor = PortalAIProcessor()
        else:
            from utils.albert_ai import AlbertAIProcessor
            ai_processor = AlbertAIProcessor()

        # Add a simple counter for processed files
        total_files = len(uploaded_files)
        processed_count = 0
        
        placeholder = st.empty()
        placeholder.write(f"Processing {total_files} files...")
        progress_bar = st.progress(0)
        
        for uploaded_file in uploaded_files:
            # Check if the file has already been processed to avoid reprocessing
            # This check is based on the file name, which should be unique. 
            # If the file name is not unique, consider using a hash or a unique identifier.
            if uploaded_file.name not in st.session_state.processed_docs:
                placeholder.write(t["processing"].format(f"{processed_count}/{total_files}: {uploaded_file.name}"))
                try:
                    # Check if the file is empty or too large
                    if uploaded_file.size == 0:
                        st.error(f"The file {uploaded_file.name} is empty. Please upload a valid PDF.")
                        continue

                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir="./data/tmp/") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Debugging: Print path to ensure it's being created
                    st.write(f"Temporary file path for {uploaded_file.name}: {tmp_path}")

                    # Extract text and run sensitivity check
                    text_content = PDFProcessor.extract_text(uploaded_file)
                    sensitive_sections = SensitivityChecker.check_document(
                        text_content, 
                        ai_processor
                    )
                    print(f"{uploaded_file.name}: Found {len(sensitive_sections)} sensitive sections")

                    st.session_state.processed_docs[uploaded_file.name] = {
                        'path': tmp_path,
                        'text_content': text_content,
                        'sensitive_sections': sensitive_sections,
                        'model': model_choice
                    }
                    processed_count += 1

                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")

            progress_bar.progress(processed_count / total_files)
        
        placeholder.success(f"Successfully processed {processed_count}/{total_files} files!")

        # Instead of stacking results vertically, create a tab for each processed document.
        doc_names = list(st.session_state.processed_docs.keys())
        if doc_names:
            tabs = st.tabs(doc_names)
            for idx, doc_name in enumerate(doc_names):
                with tabs[idx]:
                    st.subheader(f"Document: {doc_name}")
                    doc_data = st.session_state.processed_docs[doc_name]
                    
                    # Compute overall risk assessment for this document.
                    overall = "low"
                    if doc_data['sensitive_sections']:
                        for section in doc_data['sensitive_sections']:
                            cat = section['category'].lower()
                            if "secret" in cat or "security" in cat:
                                overall = "high"
                                break
                            elif "personal" in cat:
                                overall = "medium"
                    
                    # Display overall assessment with translated text
                    if overall == "low":
                        st.markdown(f"<span style='font-size: 24px;'>🟢</span> <span style='font-weight:bold;'>{t['risk_low']}</span>", unsafe_allow_html=True)
                    elif overall == "medium":
                        st.markdown(f"<span style='font-size: 24px;'>🟠</span> <span style='font-weight:bold;'>{t['risk_medium']}</span>", unsafe_allow_html=True)
                    elif overall == "high":
                        st.markdown(f"<span style='font-size: 24px;'>🔴</span> <span style='font-weight:bold;'>{t['risk_high']}</span>", unsafe_allow_html=True)
                    
                    # If no sensitive sections were found, display message; otherwise display the review table.
                    if not doc_data['sensitive_sections']:
                        st.success(t["no_sensitive"])
                    else:
                        st.write(t["found_sensitive"])
                        
                        # Get document text and sensitive sections
                        text_content = doc_data['text_content']
                        sensitive_sections = doc_data['sensitive_sections']
                        
                        # If text_content is returned as a list, join it into one string.
                        if isinstance(text_content, list):
                            text_content = ' '.join(text_content)
                        
                        # Display a table with sensitive parts and checkboxes for confirmation
                        st.write(f"### {t['review_title']}")
                        
                        # Create table header columns (adjusted widths)
                        cols_header = st.columns([0.1, 0.15, 0.4, 0.25, 0.1])
                        cols_header[0].write(f"**{t['section']}**")
                        cols_header[1].write(f"**{t['category']}**")
                        cols_header[2].write(f"**{t['text']}**")
                        cols_header[3].write(f"**{t['reason']}**")
                        cols_header[4].write(f"**{t['confirm']}**")
                        
                        # Create a table row for each sensitive section with a checkbox.
                        confirmed_sections = []
                        for i, section in enumerate(sensitive_sections):
                            cols = st.columns([0.1, 0.15, 0.4, 0.25, 0.1])
                            cols[0].write(f"Section {i+1}")
                            cols[1].write(section['category'])
                            cols[2].write(section['text'])
                            cols[3].write(section['reason'])
                            
                            confirmed = cols[4].checkbox(
                                "✓", 
                                key=f"confirm_{doc_name}_{i}", 
                                value=section['accepted']
                            )
                            
                            if confirmed:
                                confirmed_sections.append(section)  # Add confirmed section to the list

                        if st.button(t["apply"], key=f"apply_{doc_name}"):
                            # Bestätigte Schwärzungsstellen sammeln
                            confirmed_sections = []
                            for i, section in enumerate(doc_data['sensitive_sections']):
                                if st.session_state.get(f"confirm_{doc_name}_{i}", False):
                                    confirmed_sections.append(section)

                            if not confirmed_sections:
                                st.warning("No confirmed redactions. Please select sensitive sections to redact.")
                            else:
                                st.write(t["applying_redactions"])
                                tmp_path = doc_data.get('path')
                                if tmp_path and os.path.exists(tmp_path):
                                    redacted_path = f"redacted_{doc_name}"
                                    
                                    # Schwärzung anwenden
                                    #text_values = [s.get('sensitive_value') or s['text'] for s in confirmed_sections]
                                    #Blackout.redact_sentences(text_values, tmp_path, redacted_path)
                                    PDFRedactor.redact_sections(confirmed_sections, tmp_path, redacted_path)

                                    # Datei als Download anbieten
                                    with open(redacted_path, "rb") as file:
                                        st.download_button(
                                            label=t["download_redacted"],
                                            data=file,
                                            file_name=os.path.basename(redacted_path),
                                            mime="application/pdf"
                                        )
                                else:
                                    st.error("Originaldatei nicht mehr vorhanden.")


    # Option to clear all processed data and temporary files
    if st.session_state.processed_docs:
        if st.button(t["clear_all"]):
            for doc_data in st.session_state.processed_docs.values():
                if os.path.exists(doc_data['path']):
                    os.unlink(doc_data['path'])
            # Remove any confirmation keys associated with documents
            for key in list(st.session_state.keys()):
                if key.startswith("confirmed_sections_"):
                    del st.session_state[key]
            st.session_state.processed_docs = {}
            # Reset the file uploader's key to clear the uploaded files selection
            st.session_state['uploader_key'] = str(uuid.uuid4())
            st.rerun()
            
if __name__ == "__main__":
    main()
