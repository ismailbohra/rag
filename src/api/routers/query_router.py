from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from src.api.schemas.query_schema import QueryRequest
from src.api.dependencies.retriever_dep import get_retriever
from src.api.dependencies.generator_dep import get_generator

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/")
def query_docs(
    payload: QueryRequest,
    retriever = Depends(get_retriever),
    generator = Depends(get_generator)
):

    query = payload.query
    top_k = payload.top_k

    # 1. Retrieve documents
    results = retriever.retrieve(query, top_k)
    docs_text = "\n\n".join([doc.page_content for doc, _ in results])

    prompt = f"""
You are a helpful assistant. Use the following context to answer:

Context:
{docs_text}

User Query:
{query}

Answer:
"""

    # --------------- STREAMING MODE --------------------
    if payload.stream:
        from src.llm.streaming.print_stream_handler import PrintStreamHandler
        handler = PrintStreamHandler()

        def generate_stream():
            generator.generate(prompt, stream_handler=handler)
            for chunk in handler.streamed_text:
                yield chunk

        return StreamingResponse(generate_stream(), media_type="text/plain")

    # --------------- NORMAL MODE -----------------------
    response = generator.generate(prompt)
    return {"response": response["text"]}
