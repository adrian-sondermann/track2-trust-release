from string import Template

from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    AZURE_OPENAI_DEPLOYMENT_VERSION
)
from utils.base_ai import BaseAIProcessor


class AzureAIProcessor(BaseAIProcessor):
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_OPENAI_DEPLOYMENT_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )

        self.analysis_prompt = BaseAIProcessor.load_analysis_prompt()

    def analyze_text(self, text: str):
        """Analyze text for sensitive information using Azure OpenAI."""
        prompt_template = Template(self.analysis_prompt)
        final_user_prompt = prompt_template.substitute(text=text)
        
        try:
            response = self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    #{"role": "system", "content": "You are a data privacy expert."},  ## TODO: optional; Is a system prompt beneficial?
                    {"role": "user", "content": final_user_prompt}
                ],
                temperature=0.0,  # DS-A default 0.0 (lowest temperature for more deterministic greedy sampling)
                top_p=1.0,  # Portal default 1.0
                max_tokens=3000,  # Portal default 3000
                stream=False,  # TODO: add streaming support
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Azure OpenAI: {str(e)}")
            raise e