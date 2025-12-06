from .openai_generator import OpenAIGenerator
from .gemini_generator import GeminiGenerator

class GeneratorFactory:
    @staticmethod
    def get_generator(provider: str, **kwargs):
        provider = provider.lower()
        if provider in ("openai", "openai.com"):
            return OpenAIGenerator(**kwargs)
        if provider in ("gemini", "google", "google.com"):
            return GeminiGenerator(**kwargs)
        
        raise ValueError(f"Unknown provider: {provider}")
