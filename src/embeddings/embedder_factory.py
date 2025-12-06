from .sentence_transformer_embedder import SentenceTransformerEmbedder

class EmbedderFactory:

    @staticmethod
    def get_embedder(model_name: str):
        """
        Returns an embedder based on model name prefix.
        This allows plug-and-play of custom embedding providers.
        """

        # Sentence Transformer family
        if model_name.startswith("sentence-transformers") or model_name.startswith("all-"):
            return SentenceTransformerEmbedder(model_name)

        # Add more providers here
        # if model_name.startswith("openai"):
        #     return OpenAIEmbedder(model_name)

        raise ValueError(f"Unsupported embedding model: {model_name}")
