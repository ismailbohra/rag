# RAG Chatbot - Complete Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                   (http://localhost:8501)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              STREAMLIT FRONTEND (app.py)                  │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  Login/Signup Screen (auth.py)                  │    │  │
│  │  │  - Email & password input                       │    │  │
│  │  │  - Account creation                             │    │  │
│  │  │  - JWT token storage                            │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │                      ↓ (authenticated)                   │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  Main Chat Interface                             │    │  │
│  │  │  ┌──────────────┬──────────────────────────┐    │    │  │
│  │  │  │  Sidebar     │  Chat Content Area        │    │    │  │
│  │  │  │              │                            │    │    │  │
│  │  │  │ User Info    │ ┌──────────────────────┐ │    │    │  │
│  │  │  │ Logout       │ │ Message History      │ │    │    │  │
│  │  │  │ Sessions List│ │ - User messages      │ │    │    │  │
│  │  │  │ New Chat     │ │ - Assistant responses│ │    │    │  │
│  │  │  │ Delete       │ │ - Citations          │ │    │    │  │
│  │  │  │ Settings     │ │                      │ │    │    │  │
│  │  │  │              │ ├──────────────────────┤ │    │    │  │
│  │  │  │              │ │ Chat Input Box       │ │    │    │  │
│  │  │  │              │ │ (Query submission)   │ │    │    │  │
│  │  │  │              │ │                      │ │    │    │  │
│  │  │  └──────────────┴──────────────────────┘ │    │    │  │
│  │  │  Upload Tab                               │    │    │  │
│  │  │  - PDF file uploader                      │    │    │  │
│  │  │  - Progress tracking                      │    │    │  │
│  │  │  - Result reporting                       │    │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │                                                      │  │
│  │  STATE MANAGEMENT (state_manager.py)              │  │
│  │  - logged_in, token, user_info                    │  │
│  │  - active_session_id, messages                    │  │
│  │  - sessions_list, show_citations, top_k           │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API CLIENT (api_client.py)                             │  │
│  │  - HTTP requests with JWT Authorization header         │  │
│  │  - Login, signup, session management, query, upload    │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/HTTPS
                           │ JWT Bearer Token
                           │ JSON Payloads
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│               (http://localhost:8000)                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ROUTERS (src/api/routers/)                              │   │
│  │                                                           │   │
│  │  ┌─────────────────┐  ┌──────────────────────────────┐  │   │
│  │  │  auth_router    │  │  query_router                │  │   │
│  │  │  - POST /signup │  │  - POST /query/              │  │   │
│  │  │  - POST /login  │  │  - Store messages            │  │   │
│  │  │  - GET /me      │  │  - Create embeddings         │  │   │
│  │  │  - JWT tokens   │  │  - Retrieve documents        │  │   │
│  │  └─────────────────┘  │  - Generate response         │  │   │
│  │                       │  - Add citations             │  │   │
│  │  ┌─────────────────┐  │  - Return structured JSON    │  │   │
│  │  │ chat_router     │  └──────────────────────────────┘  │   │
│  │  │ - GET /sessions │                                    │   │
│  │  │ - POST /sessions│  ┌──────────────────────────────┐  │   │
│  │  │ - GET messages  │  │  ingest_router               │  │   │
│  │  │ - DELETE session│  │  - POST /upload (multipart)  │  │   │
│  │  │ - Session CRUD  │  │  - GET /files/{filename}     │  │   │
│  │  └─────────────────┘  │  - PDF upload & processing   │  │   │
│  │                       │  - Chunk & embed             │  │   │
│  │                       └──────────────────────────────┘  │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ↕                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  BUSINESS LOGIC (src/)                                   │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ embeddings/                                       │  │   │
│  │  │ - sentence_transformer_embedder.py (all-MiniLM)  │  │   │
│  │  │ - pipeline.py (chunk & embed documents)          │  │   │
│  │  │ - Produces 384-dimensional embeddings            │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ ingestion/                                        │  │   │
│  │  │ - pipeline.py (load documents)                    │  │   │
│  │  │ - pdf_loader.py (PyPDFLoader)                     │  │   │
│  │  │ - metadata_extractor.py (file paths, source)      │  │   │
│  │  │ - file_validator.py                              │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ retrieval/                                        │  │   │
│  │  │ - retriever.py (cosine similarity search)         │  │   │
│  │  │ - Queries vector store for similar docs           │  │   │
│  │  │ - Returns top_k results with relevance scores     │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ llm/                                              │  │   │
│  │  │ - gemini_generator.py / openai_generator.py       │  │   │
│  │  │ - prompt_manager.py (build prompts)               │  │   │
│  │  │ - response_formatter.py (citations + PDF links)   │  │   │
│  │  │ - Generate LLM responses with sources             │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ↕                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  VECTOR STORE (src/vectorstore/)                         │   │
│  │                                                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ pgvector_store.py                                 │  │   │
│  │  │ - upsert_chat_embedding() - Store with metadata   │  │   │
│  │  │ - search_chat_embeddings() - Find similar chunks  │  │   │
│  │  │ - Cosine similarity for retrieval                 │  │   │
│  │  │ - Stores: embedding (384-dim) + file metadata     │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ↕                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MODELS / ORM (src/models/)                              │   │
│  │                                                           │   │
│  │  SQLAlchemy Models:                                      │   │
│  │  - User (id, username, email, hashed_password)           │   │
│  │  - ChatSession (id, user_id, title, last_activity)       │   │
│  │  - Chat (id, session_id, role, content, created_at)      │   │
│  │  - ChatEmbedding (chat_id, embedding, metadata)          │   │
│  │                                                           │   │
│  │  Relationships:                                          │   │
│  │  - User → ChatSession (one-to-many, cascade)             │   │
│  │  - ChatSession → Chat (one-to-many, cascade)             │   │
│  │  - Chat → ChatEmbedding (one-to-one)                     │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ SQL Queries + Embeddings
                           │ psycopg2 + pgvector
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                   POSTGRESQL DATABASE                            │
│              (with pgvector extension)                           │
│                                                                   │
│  Tables:                                                         │
│  - users (id, username, email, password_hash)                   │
│  - chat_sessions (id, user_id, title, created_at, last_activity)│
│  - chats (id, session_id, user_id, role, content, created_at)   │
│  - chat_embeddings (chat_id, embedding<vector>, metadata)       │
│                                                                   │
│  Indexes:                                                        │
│  - user_id on chat_sessions and chats                           │
│  - session_id on chats                                          │
│  - Vector index on embeddings for fast similarity search        │
│                                                                   │
│  Vector Dimension: 384 (from all-MiniLM-L6-v2)                  │
│  Distance Metric: Cosine Similarity                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                   FILE STORAGE (data/)                           │
│                                                                   │
│  - Uploaded PDF files stored locally                            │
│  - Path tracked in Chat.metadata                                │
│  - Accessible via GET /ingest/files/{filename}                  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## 🔄 Query Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER SUBMITS QUERY                                           │
│    (Frontend chat_input_area)                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │ "What is RAG?"
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND PROCESSES                                           │
│    - Add message to state                                       │
│    - Display in chat UI                                         │
│    - Create/use session                                         │
└────────────────────┬────────────────────────────────────────────┘
                     │ POST /query/ with JWT
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. BACKEND RECEIVES QUERY                                       │
│    (query_router.py)                                            │
│    - Extract query text                                         │
│    - Verify user authentication                                 │
│    - Get/create session                                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. STORE USER MESSAGE                                           │
│    (Chat table)                                                 │
│    - role: "user"                                               │
│    - content: full query text                                   │
│    - session_id, user_id, created_at                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. CREATE EMBEDDING FOR USER MESSAGE                            │
│    (sentence_transformer)                                       │
│    - Query → 384-dimensional vector                             │
│    - Store in chat_embeddings table                             │
│    - Include metadata (session_id, user_id, role)               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. RETRIEVE CONVERSATION HISTORY                                │
│    (query_router.py)                                            │
│    - Query Chat table for session messages                      │
│    - Order by created_at (chronological)                        │
│    - Format as conversation context                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. RETRIEVE RELEVANT DOCUMENTS                                  │
│    (retriever.py - vector similarity search)                    │
│    - Embed query (same model)                                   │
│    - Search pgvector index                                      │
│    - Cosine similarity to document chunks                       │
│    - Return top_k results with scores                           │
│    - Include metadata (file_path, source, page)                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. BUILD COMPREHENSIVE PROMPT                                   │
│    - System instructions (RAG behavior rules)                   │
│    - Conversation history (previous messages)                   │
│    - Retrieved documents context                                │
│    - Current user query                                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. CALL LLM MODEL                                               │
│    (gemini_generator.py or openai_generator.py)                 │
│    - Send prompt with context                                   │
│    - Get generated response                                     │
│    - Apply streaming (if enabled)                               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. STORE ASSISTANT RESPONSE                                    │
│     (Chat table)                                                │
│     - role: "assistant"                                         │
│     - content: generated text                                   │
│     - session_id, user_id, created_at                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 11. CREATE EMBEDDING FOR RESPONSE                               │
│     (sentence_transformer)                                      │
│     - Response text → 384-dim vector                            │
│     - Store in chat_embeddings                                  │
│     - Link to response Chat record                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 12. FORMAT RESPONSE WITH CITATIONS                              │
│     (response_formatter.py)                                     │
│     - Extract relevant chunks                                   │
│     - Add PDF file information                                  │
│     - Create download links                                     │
│     - Include relevance scores                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 13. RETURN STRUCTURED RESPONSE                                  │
│     JSON Response:                                              │
│     {                                                           │
│       "session_id": "uuid",                                     │
│       "response": {                                             │
│         "answer": "RAG is a technique...",                      │
│         "citations": [                                          │
│           {                                                     │
│             "id": "document.pdf",                               │
│             "score": 0.95,                                      │
│             "pdf_file": "document.pdf",                         │
│             "pdf_link": "/api/files/document.pdf",              │
│             "meta": {...}                                       │
│           }                                                     │
│         ]                                                       │
│       }                                                         │
│     }                                                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 14. FRONTEND DISPLAYS RESPONSE                                  │
│     (chat_ui.py)                                                │
│     - Show assistant message                                    │
│     - Render citations expandable                               │
│     - Display PDF links with [Download]                         │
│     - Update chat history                                       │
│     - Add to Streamlit state                                    │
└─────────────────────────────────────────────────────────────────┘
```

## 🗂️ File Organization

### Frontend Files
```
frontend/
├── app.py (250 lines)                    # Main entry point
├── api_client.py (150 lines)             # API communication
├── auth.py (200 lines)                   # Auth UI
├── state_manager.py (100 lines)          # State management
├── components/
│   ├── chat_ui.py (100 lines)           # Message rendering
│   ├── session_sidebar.py (150 lines)    # Sidebar nav
│   └── document_upload.py (100 lines)    # File upload
├── requirements.txt                      # Dependencies
├── .env.example                          # Config template
└── README.md                             # Documentation
```

### Backend Files (Existing + Enhanced)
```
src/
├── api/
│   ├── main.py                          # FastAPI app
│   ├── routers/
│   │   ├── auth_router.py              # Auth endpoints
│   │   ├── chat_router.py              # Session CRUD
│   │   ├── query_router.py             # RAG query (enhanced)
│   │   └── ingest_router.py            # Upload (enhanced)
│   ├── schemas/
│   │   └── ingest_schema.py            # (enhanced)
│   └── dependencies/
│       └── [various dependencies]
├── models/
│   └── tables.py                        # SQLAlchemy ORM
├── embeddings/
│   ├── pipeline.py                      # Chunking + embedding
│   └── sentence_transformer_embedder.py
├── ingestion/
│   ├── pipeline.py                      # Document loading
│   └── utils/
│       └── metadata_extractor.py        # (enhanced)
├── retrieval/
│   └── retriever.py                     # Vector search
├── llm/
│   ├── response_formatter.py            # (enhanced with PDF links)
│   └── [generators and prompts]
└── vectorstore/
    └── pgvector_store.py               # Vector DB operations
```

## 📊 Data Models Relationships

```
User
 ├─ id (PK)
 ├─ username
 ├─ email
 └─ password_hash
    │
    └──┬─────────────────────────────┐
       │ (one-to-many)               │
       ▼                             ▼
    ChatSession                   Chat (without session)
    ├─ id (PK)                  ├─ id (PK)
    ├─ user_id (FK)             ├─ user_id (FK)
    ├─ title                    ├─ content
    ├─ created_at               ├─ role
    └─ last_activity            └─ created_at
       │
       └──┬──────────────────────┐
          │ (one-to-many)        │
          ▼                      ▼
        Chat                 ChatEmbedding
        ├─ id (PK)         ├─ chat_id (FK/PK)
        ├─ session_id (FK) ├─ embedding (vector 384)
        ├─ user_id (FK)    └─ metadata
        ├─ role                  (session_id, file_path,
        ├─ content               user_id, role, etc.)
        ├─ metadata
        └─ created_at
```

---

**Complete RAG System with Frontend + Backend!** 🚀
