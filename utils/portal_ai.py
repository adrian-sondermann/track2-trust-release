from string import Template

from langchain_ai_portal import UbitecAiPortalSdkChat
from config import (
    PORTAL_API_HOST,
    PORTAL_API_PORT,
    PORTAL_API_USE_SSL,
    PORTAL_API_KEY,
    PORTAL_API_MODEL_IDENTIFIER,
)
from utils.base_ai import BaseAIProcessor

class PortalAIProcessor(BaseAIProcessor):
    def __init__(self):

        self.chat_model = UbitecAiPortalSdkChat(
            portal_api_host=PORTAL_API_HOST,
            portal_api_port=PORTAL_API_PORT,
            portal_api_sdk_apikey=PORTAL_API_KEY,
            portal_api_use_ssl=PORTAL_API_USE_SSL,
            model=PORTAL_API_MODEL_IDENTIFIER,
            model_kwargs={
               "temperature": 0.0,  # DS-A default 0.0 (lowest temperature for more deterministic greedy sampling)
               "top_p": 1.0,  # Portal default 1.0
            },
            max_tokens=3000,  # Portal default 3000
            streaming=False, # TODO: add streaming support
        )

        self.analysis_prompt = BaseAIProcessor.load_analysis_prompt()

    def analyze_text(self, text: str):
        """
        Analyze the provided text for sensitive information.
        """
        prompt_template = Template(self.analysis_prompt)
        final_user_prompt = prompt_template.substitute(text=text)

        messages = [
            #{"role": "system", "content": "You are a data privacy expert."},  # TODO: optional; Is a system prompt beneficial?
            {"role": "user", "content": final_user_prompt},
        ]
        response = self.chat_model.invoke(messages)
        print(f"Response: {response}\n")
        return response.content