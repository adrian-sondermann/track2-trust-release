"""Home"""

import streamlit as st
import tempfile
import os
from utils.pdf_processor import PDFProcessor
from utils.azure_ai import AzureAIProcessor
from utils.sensitivity_checker import SensitivityChecker
from utils.pdf_redactor import PDFRedactor
from sidebar import render_sidebar_logo
from utils.common import initialize_page
from PIL import Image
from utils.cleanup import cleanup_temp_pdfs

# Get the absolute path to the image
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "static", "images", "logo.png")

# Load and convert the image
icon_image = Image.open(logo_path)

st.set_page_config(
    page_title="TrustRelease",
    page_icon=icon_image,
    layout="wide"
)

# Add custom CSS to adjust the sidebar navigation and logo positioning
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            margin-top: 0px !important;
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 0rem;
        }
        .logo-container {
            position: fixed !important;
            top: 240px !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999 !important;
        }
        .nav-links {
            position: relative !important;
            margin-top: 0px !important;
            z-index: 998 !important;
        }
        /* Additional selectors to ensure proper stacking */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0px !important;
        }
        div[data-testid="stSidebarNav"] {
            padding-top: 0px !important;
            z-index: 997 !important;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # 🧹 Temp-Ordner aufräumen
    cleanup_temp_pdfs() 

    # Initialize common elements
    lang = initialize_page()
    
    # Translated texts for each language
    translations = {
        "English": {
            "title": "Welcome to TrustRelease",
            "subtitle": "Your Tool for GDPR and IFG Compliance",
            "about": """
#### About this Application
The PDF Sensitivity Checker helps you identify and manage sensitive information in your PDF documents 
according to GDPR (General Data Protection Regulation) and IFG (Freedom of Information Act) requirements.
""",
            "features": """
#### Key Features:
- **Automated Detection:** Upload PDFs and automatically detect sensitive information
- **Smart Analysis:** Uses AI to identify potential sensitive content
- **Interactive Review:** Review and confirm detected sensitive sections
- **GDPR & IFG Compliance:** Focuses on relevant sensitivity categories
""",
            "how_to": """
#### How to Use:
1. Navigate to the "PDF Checker" page using the sidebar
2. Upload one or more PDF documents
3. Review the detected sensitive information
4. Confirm or dismiss the findings
""",
            "get_started": """
#### Get Started
Click on "PDF Checker" in the sidebar to begin analyzing your documents.
"""
        },
        "Deutsch": {
            "title": "Willkommen beim PDF Sensitivity Checker",
            "subtitle": "Ihr Werkzeug zur Einhaltung der DSGVO und IFG",
            "about": """
#### Über diese Anwendung
Der PDF Sensitivity Checker hilft Ihnen dabei, sensible Informationen in Ihren PDF-Dokumenten zu identifizieren 
und zu verwalten, um den Anforderungen der DSGVO (Datenschutz-Grundverordnung) und des IFG (Informationsfreiheitsgesetz) gerecht zu werden.
""",
            "features": """
#### Hauptfunktionen:
- **Automatische Erkennung:** Laden Sie PDFs hoch und erkennen Sie automatisch sensible Informationen
- **Intelligente Analyse:** Nutzt KI, um potenziell sensible Inhalte zu identifizieren
- **Interaktive Überprüfung:** Überprüfen und bestätigen Sie erkannte sensible Abschnitte
- **DSGVO- & IFG-Konformität:** Konzentriert sich auf relevante Kategorien
""",
            "how_to": """
#### Anleitung:
1. Navigieren Sie über die Seitenleiste zur Seite "PDF Checker"
2. Laden Sie ein oder mehrere PDF-Dokumente hoch
3. Überprüfen Sie die erkannten sensiblen Informationen
4. Bestätigen oder verwerfen Sie die Ergebnisse
""",
            "get_started": """
#### Loslegen
Klicken Sie in der Seitenleiste auf "PDF Checker", um mit der Analyse Ihrer Dokumente zu beginnen.
"""
        },
        "Français": {
            "title": "Bienvenue sur le PDF Sensitivity Checker",
            "subtitle": "Votre outil pour la conformité au RGPD et à la loi sur l'accès à l'information",
            "about": """
#### À propos de cette application
Le PDF Sensitivity Checker vous aide à identifier et à gérer les informations sensibles dans vos documents PDF 
conformément aux exigences du RGPD (Règlement général sur la protection des données) et de la loi sur l'accès à l'information.
""",
            "features": """
#### Caractéristiques principales:
- **Détection automatisée:** Téléchargez des PDFs et détectez automatiquement les informations sensibles
- **Analyse intelligente:** Utilise l'IA pour identifier les contenus potentiellement sensibles
- **Révision interactive:** Examinez et confirmez les sections sensibles identifiées
- **Conformité RGPD & IFG:** Se concentre sur les catégories sensibles pertinentes
""",
            "how_to": """
#### Comment l'utiliser:
1. Naviguez vers la page "PDF Checker" dans la barre latérale
2. Téléchargez un ou plusieurs documents PDF
3. Passez en revue les informations sensibles détectées
4. Confirmez ou rejetez les résultats
""",
            "get_started": """
#### Commencez
Cliquez sur "PDF Checker" dans la barre latérale pour commencer l'analyse de vos documents.
"""
        }
    }

    # Choose the appropriate translation based on the selected language
    t = translations[lang]

    st.title(t["title"])
    st.write("### " + t["subtitle"])
    st.markdown(t["about"])
    st.markdown(t["features"])
    st.markdown(t["how_to"])

    # Initialize session state
    if 'processed_docs' not in st.session_state:
        st.session_state.processed_docs = {}

if __name__ == "__main__":
    main() 