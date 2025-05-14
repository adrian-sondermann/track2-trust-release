import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_DEPLOYMENT_VERSION = os.getenv("AZURE_OPENAI_DEPLOYMENT_VERSION")

# Configuration for the LangChain AI Portal API.
PORTAL_API_HOST=os.getenv("PORTAL_API_HOST")
PORTAL_API_KEY=os.getenv("PORTAL_API_KEY")
PORTAL_API_PORT=os.getenv("PORTAL_API_PORT")
PORTAL_API_USE_SSL=os.getenv("PORTAL_API_USE_SSL")

PORTAL_API_MODEL_IDENTIFIER=os.getenv("PORTAL_API_MODEL_IDENTIFIER")

# Sensitivity Check Configuration
SENSITIVITY_RULES = {
    "personal_data": {
        "name": "Personal Data (GDPR Art. 4)",
        "description": "Information relating to identified or identifiable natural person"
    },
    "special_categories": {
        "name": "Special Categories (GDPR Art. 9)",
        "description": "Racial/ethnic origin, political opinions, religious beliefs, health data, etc."
    },
    "official_secrets": {
        "name": "Official Secrets (IFG §3)",
        "description": "Information classified as confidential by German law"
    },
    "business_secrets": {
        "name": "Business Secrets (IFG §6)",
        "description": "Trade secrets and confidential business information"
    }
} 