"""Main FastAPI application with authentication, chat sessions, and RAG."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.api.routers.auth_router import router as auth_router
from src.api.routers.chat_router import router as chat_router
from src.api.routers.ingest_router import router as ingest_router
from src.api.routers.query_router import router as query_router
from src.api.utils.api_logging import log_http_middleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Modular RAG API with Auth & Chat Sessions",
    version="2.0",
    description="Production RAG architecture with JWT authentication, per-user chat sessions, and embeddings storage",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "persistAuthorization": True  # Keep token in browser storage
    }
)

# Add HTTP logging middleware (before other middleware)
log_http_middleware(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(query_router)


def custom_openapi():
    """Generate OpenAPI schema with Bearer token security configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Define Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token from /auth/login or /auth/signup in the format: Bearer <your_token>"
        }
    }
    
    # Add security to all protected endpoints
    protected_paths = {
        "/chats/sessions": True,
        "/query/": True,
        "/auth/me": True
    }
    
    for path, path_item in openapi_schema.get("paths", {}).items():
        # Check if path is protected
        is_protected = any(path.startswith(p) for p in protected_paths.keys())
        
        if is_protected:
            for method, operation in path_item.items():
                if isinstance(operation, dict) and "operationId" in operation:
                    # Add global security requirement
                    operation["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {
        "status": "RAG API running",
        "docs": "/docs",
        "version": "2.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
