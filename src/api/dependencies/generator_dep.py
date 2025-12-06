from src.llm.generator_factory import GeneratorFactory

def get_generator():
    return GeneratorFactory.get_generator(
        provider="gemini", 
        api_key="AIzaSyBDw-inTgYeJEaEdWax1EAeXw3CYMihm6k"
    )
