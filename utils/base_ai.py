from abc import ABC, abstractmethod

class BaseAIProcessor(ABC):
    """
    Abstract base class for AI models.
    """

    @abstractmethod
    def analyze_text(self, model_path: str) -> str:
        """
        Analyze the provided text for sensitive information.
        """
        pass

    
    @staticmethod
    def load_analysis_prompt() -> str:
        """
        Load the analysis prompt from a file.
        """
        with open("./prompts/analysis_prompt_de.md", 'r') as file:
            return file.read()
