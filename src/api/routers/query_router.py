"""Query and chat endpoint with user authentication and session management."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.api.schemas.chat_schema import QueryPayload, QueryResponse
from src.api.dependencies.retriever_dep import get_retriever
from src.api.dependencies.generator_dep import get_generator
from src.api.dependencies.auth_dep import get_current_user, get_db
from src.models.tables import ChatSession, Chat, User
from src.llm.response_formatter import ResponseFormatter
from src.embeddings.pipeline import EmbeddingPipeline
from src.vectorstore.store_factory import VectorStoreFactory
from src.api.utils.api_logging import log_api_call
from datetime import datetime
import os


router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
@log_api_call("query_documents")
def query_docs(
    payload: QueryPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    retriever = Depends(get_retriever),
    generator = Depends(get_generator)
):
    """
    Query endpoint with user authentication and per-session chat history.
    
    - Creates/uses chat session for current user
    - Stores user message in chat history
    - Creates embedding for user message
    - Performs retrieval (optionally restricted to session)
    - Generates response
    - Stores assistant message and its embedding
    """
    query = payload.query
    top_k = payload.top_k or 5

    # 1. Determine or create session
    session = None
    if payload.session_id:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == payload.session_id,
                ChatSession.user_id == current_user.id
            )
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        # Create new session if not provided
        session = ChatSession(user_id=current_user.id, title="New chat")
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Store incoming user message in chats table
    user_chat = Chat(
        session_id=session.id,
        user_id=current_user.id,
        role="user",
        content=query
    )
    db.add(user_chat)
    db.commit()
    db.refresh(user_chat)

    # 3. Create embedding for user message
    try:
        embed_pipeline = EmbeddingPipeline(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            chunk_size=1024,
            chunk_overlap=0
        )
        embedder = embed_pipeline.embedder
        user_embedding = embedder.embed_query(query)  # Returns List[float]

        # 4. Upsert embedding into chat_embeddings table
        db_url = os.getenv(
            "DATABASE_URL"
        )
        store = VectorStoreFactory.get_store(
            db_type="pgvector",
            conn_str=db_url,
            embedding_dim=384
        )
        store.upsert_chat_embedding(
            chat_id=user_chat.id,
            embedding=user_embedding,
            metadata={
                "session_id": str(session.id),
                "user_id": str(current_user.id),
                "role": "user"
            }
        )
    except Exception as e:
        # Log error but don't fail the whole request
        print(f"Error storing embedding: {e}")

    # 5. Retrieve documents (using existing retriever)
    results = retriever.retrieve(query, top_k)
    docs_text = "\n\n".join([doc.page_content for doc, _ in results])

    # 5a. Fetch recent conversation history (last 5 messages excluding current)
    recent_messages = (
        db.query(Chat)
        .filter(Chat.session_id == session.id)
        .order_by(Chat.created_at.desc())
        .limit(10)
        .all()
    )
    # Reverse to get chronological order
    recent_messages = list(reversed(recent_messages))
    
    # Build conversation history context
    conversation_history = ""
    if recent_messages:
        conversation_history = "\n==================== CONVERSATION HISTORY ====================\n"
        for msg in recent_messages:
            role = msg.role.upper()
            conversation_history += f"\n{role}: {msg.content}\n"
        conversation_history += "===========================================================\n"

    # 6. Build prompt with conversation history
    prompt = f"""
            You are an AI assistant in a Retrieval-Augmented Generation (RAG) system.

            Your job is to answer the user's query using ONLY the information provided in the context **unless** 
            the query is simply a greeting or a polite conversational phrase.
            {conversation_history}
            ==================== CONTEXT ====================
            {docs_text}
            =================================================

            BEHAVIOR RULES:
            1. If the user's query is a **greeting**, such as:
            - "hi", "hello", "hey", "good morning", "good evening", etc.
            Respond with a friendly greeting.

            2. If the user's query expresses **gratitude or politeness**, such as:
            - "thanks", "thank you", "great", "appreciate it", etc.
            Reply politely and positively.

            3. Otherwise, treat the query as a knowledge question:
            - Answer ONLY using the provided context.
            - Do NOT use outside knowledge.
            - Do NOT hallucinate or invent facts.
            - If information is incomplete, answer only what the context supports.
            - If the answer is NOT related to the context, say:
                "The provided context does not contain information about this."

            4. Keep your answer clear, concise, and factual.
            5. cite sources in square brackets like [source-id]    
            6. Use the conversation history to understand context for follow-up questions.
               For example, if a previous message mentioned a topic, refer to it when relevant.

            -------------------- CURRENT USER QUERY --------------------
            {query}

            ----------------------- ANSWER ----------------------
            """


    # 7. Generate response (non-streaming for now)
    response = generator.generate(prompt)
    assistant_text = response["text"].strip()

    # 11. Format response with citations BEFORE storing in DB
    formatted = ResponseFormatter.format_answer(assistant_text, results)
    citations = formatted.get("citations", [])

    # 8. Store assistant reply in chats table with citations
    assistant_chat = Chat(
        session_id=session.id,
        user_id=current_user.id,
        role="assistant",
        content=assistant_text,
        citations=citations
    )
    db.add(assistant_chat)
    db.commit()
    db.refresh(assistant_chat)

    # 9. Embed assistant reply and store embedding
    try:
        assistant_embedding = embedder.embed_query(assistant_text)
        store.upsert_chat_embedding(
            chat_id=assistant_chat.id,
            embedding=assistant_embedding,
            metadata={
                "session_id": str(session.id),
                "user_id": str(current_user.id),
                "role": "assistant"
            }
        )
    except Exception as e:
        print(f"Error storing assistant embedding: {e}")

    # 10. Update session last activity
    session.last_activity = datetime.utcnow()
    db.add(session)
    db.commit()

    return QueryResponse(session_id=session.id, response=formatted)
