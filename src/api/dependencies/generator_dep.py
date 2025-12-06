from src.llm.generator_factory import GeneratorFactory
import os

def get_generator():
    api_key = os.getenv("GOOGLE_API_KEY")
    return GeneratorFactory.get_generator(
        provider="gemini", 
        api_key=api_key
    )
