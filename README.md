<p align="center">
  <img src="static/images/logo.png" alt="PDF Sensitivity Checker Logo" width="200"/>
</p>

# Trust Release

A Streamlit application that checks PDF documents for sensitive information according to GDPR and German Informationsfreiheitsgesetz (IFG) or French loi sur l'accès à l'information using Azure OpenAI or Albert [Albert AI](https://github.com/etalab-ia/albert-api?tab=readme-ov-file).

## Features

- Upload multiple PDF documents
- Analyze documents for sensitive information using Azure OpenAI or [Albert AI](https://github.com/etalab-ia/albert-api?tab=readme-ov-file)
- Identify sensitive content based on GDPR and IFG criteria

- Review and approve/dismiss detected sensitive sections
- Generate redacted PDFs with approved sensitive content blackened out
- Download redacted documents

## Setup

1. Create a `.env` file with your Azure OpenAI and Portal credentials:
   ```
   AZURE_OPENAI_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```
   streamlit run Home.py
   ```

## Additional Information

This project is designed to tackle a prominent challenge in the public sector by leveraging state-of-the-art AI to detect sensitive information in PDFs. Below is an explanation of how the application delivers value based on key evaluation criteria – integrating additional benefits such as boosting confidence in data-driven decision-making through open data practices and its applicability across various governmental contexts:

### English
**Relevance:** This app directly addresses a critical need in public service institutions by automating the detection of sensitive data in compliance with GDPR and IFG regulations. It enhances trust in decision-making by promoting open data practices across public institutions.
**Impact:** By harnessing robust AI engines such as Azure OpenAI (and alternatives), the application enables organizations to quantitatively assess risks, leading to measurable improvements in data protection. This not only improves data security but also supports transparent, evidence-based decision-making in government operations.
**Feasibility:** Developed as an MVP using Streamlit and a modular design, the solution incorporates established APIs and clear workflows, ensuring a realistic and deployable implementation. Its straightforward design also facilitates the integration of open data practices into governmental workflows.
**Scalability:** With built-in multi-language support and a modular architecture, the app can be effortlessly extended and adapted as a digital commons for broader public sector applications. Its versatile design ensures seamless scalability across various governmental contexts, further advancing open data initiatives.

### Français
**Pertinence :** Cette application répond à un besoin crucial dans le secteur public en automatisant la détection des données sensibles conformément aux réglementations RGPD et la loi sur l'accès à l'information. Elle renforce la confiance dans la prise de décision en promouvant les pratiques d'ouverture des données au sein des institutions publiques.
**Impact :** En exploitant des moteurs d'IA robustes tels que Azure OpenAI, l'application permet aux organisations d'évaluer les risques de manière quantitative, menant à des améliorations mesurables en matière de protection des données. Cela améliore non seulement la sécurité des données, mais soutient également une prise de décision transparente et fondée sur les données.
**Faisabilité :** Conçue comme un MVP en utilisant Streamlit et des principes de conception modulaires, la solution intègre des API éprouvées et des processus clairs, garantissant une mise en œuvre réaliste et déployable. Sa conception simple facilite l'intégration des pratiques d'open data dans les processus gouvernementaux.
**Scalabilité :** Grâce à son support multilingue intégré et à son architecture modulaire, l'application peut être facilement étendue et adaptée dans divers contextes gouvernementaux, favorisant ainsi l'intégration des données ouvertes et améliorant la transparence ainsi que l'efficacité opérationnelle.

### Deutsch
**Relevanz:** Die Anwendung greift ein zentrales Bedürfnis im öffentlichen Dienst auf, indem sie die automatische Erkennung sensibler Daten zur Einhaltung von DSGVO und IFG ermöglicht. Sie stärkt das Vertrauen in datenbasierte Entscheidungsprozesse, indem sie offene Datenpraktiken fördert.
**Impact:** Durch den Einsatz leistungsstarker KI-Technologien wie Azure OpenAI können Organisationen Risiken quantifizieren und messbare Verbesserungen im Datenschutz erzielen. Dies unterstützt transparente, fundierte Entscheidungsprozesse in der öffentlichen Verwaltung.
**Machbarkeit:** Als MVP konzipiert unter Verwendung von Streamlit und modularen Designprinzipien, integriert die Lösung bewährte APIs und klare Abläufe, was eine realistische und umsetzbare Implementierung gewährleistet. Das benutzerfreundliche Design erleichtert zudem die Integration von Open-Data-Praktiken in behördliche Abläufe.
**Skalierbarkeit:** Dank der integrierten Mehrsprachigkeit und modularen Architektur lässt sich die App problemlos erweitern und an verschiedene behördliche Kontexte anpassen, wodurch sie als digitales Gemeingut im öffentlichen Sektor dient und offene Dateninitiativen fördert.

# Inspect redacted content

## Convert PDF into text

Convert the document to text using `pdftotext` (part of `poppler-utils`):
```shell
pdftotext <`redacted_input.pdf`>
```

## Hidden layers

1. Using PDF debugging tools, e.g `qpdf` or `mutool`:

   **Installation**

   ```shell
   sudo apt update
   sudo apt install qpdf
   sudo apt install mupdf-tools
   ```

   To show internal pdf object, run `mutool show <redacted_input.pdf>`.

   To convert the PDF into an uncompressed format for manual inspection, run `qpdf --qdf --object-streams=disable <redacted_input.pdf> <output_qdf.pdf>`.

2. Adobe Acrobat Pro 

   Use "Content" pane or "Preflight" tools to inspect layers, hidden objects, or redactions. 


3. PDF Editors / Viewers

   Tools like PDF-XChange Editor or PDF Studio let you see and toggle visual layers manually.

## Metadata

Use `exiftool`

**Installation**

```shell
sudo apt update
sudo apt install libimage-exiftool-perl
```

To inspect metadata, run:
```shell
exiftool <redacted_input.pdf>
```