"""
API Logging Decorator
Tracks API calls with user information, payloads, responses, and timing
"""
import json
import time
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional
from fastapi import Request
from src.utils.logger import get_logger

logger = get_logger(__name__)


def format_payload(data: Any) -> str:
    """Format payload for logging, hiding sensitive information"""
    if data is None:
        return "None"
    
    try:
        if isinstance(data, dict):
            # Create a copy to avoid modifying original
            safe_data = data.copy()
            
            # Hide sensitive fields
            sensitive_fields = ['password', 'hashed_password', 'token', 'access_token', 'secret']
            for field in sensitive_fields:
                if field in safe_data:
                    safe_data[field] = "***REDACTED***"
            
            return json.dumps(safe_data, default=str)
        else:
            return json.dumps(data, default=str)
    except Exception as e:
        return f"<Unable to serialize: {str(e)}>"


def extract_user_id(request: Request) -> Optional[str]:
    """Extract user ID from JWT token in request headers"""
    try:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            # In production, you'd decode the JWT here to get the user_id
            # For now, we log the token prefix
            token = auth_header[7:]  # Remove "Bearer "
            return token[:20] + "..." if len(token) > 20 else token
        return "ANONYMOUS"
    except Exception as e:
        logger.warning(f"Error extracting user from request: {str(e)}")
        return "UNKNOWN"


def log_api_call(endpoint_name: Optional[str] = None):
    """
    Decorator to log API calls with comprehensive information.
    
    Logs:
    - Endpoint name
    - User information (from JWT token)
    - Request payload (with sensitive data redacted)
    - Response data
    - Execution time
    - Status codes and errors
    
    Usage:
        @log_api_call("user_registration")
        def signup(payload: UserCreate, db: Session = Depends(get_db)):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Get the current request from context if available
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            # Extract user information
            user_identifier = "ANONYMOUS"
            if request:
                user_identifier = extract_user_id(request)
            
            # Get endpoint name
            api_endpoint = endpoint_name or func.__name__
            
            # Extract payload for logging
            payload_str = "None"
            for arg in args:
                if hasattr(arg, 'dict'):  # Pydantic model
                    payload_str = format_payload(arg.dict())
                    break
                elif isinstance(arg, dict):
                    payload_str = format_payload(arg)
                    break
            
            # Log the incoming request
            logger.info(
                f"API_CALL_START | "
                f"Endpoint: {api_endpoint} | "
                f"User: {user_identifier} | "
                f"Payload: {payload_str}"
            )
            
            start_time = time.time()
            response = None
            error = None
            
            try:
                # Execute the actual function
                response = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log successful response
                response_str = format_payload(response)
                logger.info(
                    f"API_CALL_SUCCESS | "
                    f"Endpoint: {api_endpoint} | "
                    f"User: {user_identifier} | "
                    f"Status: 200 | "
                    f"Duration: {execution_time:.3f}s | "
                    f"Response: {response_str}"
                )
                
                return response
            
            except Exception as e:
                execution_time = time.time() - start_time
                error = str(e)
                
                # Log error response
                logger.error(
                    f"API_CALL_ERROR | "
                    f"Endpoint: {api_endpoint} | "
                    f"User: {user_identifier} | "
                    f"Error: {error} | "
                    f"Duration: {execution_time:.3f}s",
                    exc_info=True
                )
                
                raise
        
        return wrapper
    
    return decorator


def log_http_middleware(app):
    """
    Middleware to log all HTTP requests and responses.
    
    Usage in main.py:
        from src.api.utils.api_logging import log_http_middleware
        app = FastAPI()
        log_http_middleware(app)
    """
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # Extract request details
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        
        user_id = extract_user_id(request)
        
        # Read request body if available
        body = ""
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                body = format_payload(json.loads(body_bytes))
            except Exception:
                body = "<Unable to read body>"
        
        # Log incoming request
        logger.info(
            f"HTTP_REQUEST | "
            f"Method: {method} | "
            f"Path: {path} | "
            f"User: {user_id} | "
            f"Query: {query_params if query_params else 'None'} | "
            f"Body: {body if body else 'None'}"
        )
        
        start_time = time.time()
        
        # Call the next middleware/route
        response = await call_next(request)
        
        execution_time = time.time() - start_time
        
        # Log outgoing response
        logger.info(
            f"HTTP_RESPONSE | "
            f"Method: {method} | "
            f"Path: {path} | "
            f"User: {user_id} | "
            f"Status: {response.status_code} | "
            f"Duration: {execution_time:.3f}s"
        )
        
        return response
    
    return app
