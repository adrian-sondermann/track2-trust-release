from openai import AzureOpenAI
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_DEPLOYMENT_NAME
import os


class AzureAIProcessor:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def analyze_text(self, text):
        """Analyze text for sensitive information using Azure OpenAI."""
        prompt = """
        Analyze the following text for sensitive information according to GDPR and German 
        Informationsfreiheitsgesetz (IFG). Identify any:
        1. Personal data (names, addresses, contact info)
        2. Special category data (health, religion, political opinions)
        3. Official secrets
        4. Business secrets or confidential information

        Return the results in the following JSON format:
        {
            "sensitive_sections": [
                {
                    "text": "sensitive text excerpt",
                    "category": "category name",
                    "reason": "explanation why this is sensitive"
                }
            ]
        }
        Just give back the JSON and nothing else. Don't add any comments or explanations. Don't say "Here is the JSON" or anything like that.
        Text to analyze:
        """
        
        try:
            response = self.client.chat.completions.create(
                model=AZURE_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a data privacy expert."},
                    {"role": "user", "content": prompt + text}
                ],
                #temperature=0.3
            )
            #print(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Azure OpenAI: {str(e)}")
            raise 