from src.ingestion.pipeline import IngestionPipeline
from src.embeddings.pipeline import EmbeddingPipeline
from src.vectorstore.store_factory import VectorStoreFactory

# 1. Load docs
# docs = IngestionPipeline().load("data/raw/test.pdf")

# # 2. Chunk + embed
# embed_pipeline = EmbeddingPipeline(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     chunk_size=350,
#     chunk_overlap=50
# )
# chunked_docs, embeddings = embed_pipeline.process(docs)

# 3. Connect to pgvector
store = VectorStoreFactory.get_store(
    db_type="pgvector",
    conn_str="postgresql://default:FqGEiXoH6jO2@ep-billowing-butterfly-a4sdj7jq-pooler.us-east-1.aws.neon.tech/vectordb?sslmode=require&channel_binding=require",
    embedding_dim=384
)

# # 4. Create table
# store.create_collection()

# # 5. Upsert vectors
# store.upsert(chunked_docs, embeddings)

from src.vectorstore.store_factory import VectorStoreFactory
from src.retrieval.retriever_factory import RetrieverFactory


# Create retriever
# retriever = RetrieverFactory.get_retriever(
#     retriever_type="vector",
#     vector_store=store,
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# Ask a question
# results = retriever.retrieve("Transformers", top_k=5)

# for doc, score in results:
#     print("Score:", score)
#     print("Content:", doc.page_content[:200])
#     print("----")



from src.retrieval.retriever_factory import RetrieverFactory
from src.vectorstore.store_factory import VectorStoreFactory
from src.llm.generator_factory import GeneratorFactory
from src.llm.prompt_manager import PromptManager
from src.llm.response_formatter import ResponseFormatter


retriever = RetrieverFactory.get_retriever("vector", vector_store=store, model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2) Retrieve docs
q = "What is Tranformers?"
retrieved = retriever.retrieve(q, top_k=8)  # List[(Document, score)]

# unpack docs for prompt manager
docs = [d for d, s in retrieved]

# 3) Build prompt
pm = PromptManager()
prompt = pm.build_prompt(docs, q, max_context_chars=3500)

# 4) Get generator and generate
generator = GeneratorFactory.get_generator(provider="gemini", api_key="AIzaSyBDw-inTgYeJEaEdWax1EAeXw3CYMihm6k")
resp = generator.generate(prompt, max_tokens=512, temperature=0.0)

# 5) Format final response
formatted = ResponseFormatter.format_answer(resp["text"], retrieved)
print(formatted)
