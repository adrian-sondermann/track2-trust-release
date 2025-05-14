from langchain_ai_portal import UbitecAiPortalSdkChat
from langchain_core.messages import HumanMessage, SystemMessage
import os

class PortalAIProcessor:
    def __init__(self):

        self.chat_model = UbitecAiPortalSdkChat(
            portal_api_host=os.getenv("PORTAL_API_HOST"),
            portal_api_port=os.getenv("PORTAL_API_PORT"),
            portal_api_sdk_apikey=os.getenv("PORTAL_API_API_KEY"),
            portal_api_use_ssl=os.getenv("PORTAL_API_USE_SSL"),
            model=os.getenv("PORTAL_API_MODEL_IDENTIFIER"),
            model_kwargs={
               "temperature": 0
            },
            streaming=False, # streaming should probably be False within ProMoAI
    )

    def get_completion(self, prompt: str, text: str):
        system_message = "You are a data privacy expert."
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt + text}
        ]
        response = self.chat_model.invoke(messages)

        return response.content

    def analyze_text(self, text: str):
        """
        Analyze the provided text for sensitive information.
        This method wraps `get_completion` so it has the same interface as AzureAIProcessor.
        """
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

        return self.get_completion(prompt, text) 