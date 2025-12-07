# API Logging System

Comprehensive logging for tracking API calls with user information, payloads, responses, and timing.

## Features

### 1. **log_api_call Decorator**
Decorator for individual endpoint functions to track:
- Endpoint name
- User identification from JWT token
- Request payload (with sensitive data redacted)
- Response data
- Execution time
- Error details and stack traces

### 2. **HTTP Middleware Logging**
Global middleware to log all HTTP requests and responses:
- Method and path
- Query parameters
- Request body
- Response status code
- Execution time
- User identification

### 3. **Security Features**
- Automatically redacts sensitive fields: `password`, `hashed_password`, `token`, `access_token`, `secret`
- Truncates long tokens for readability
- JSON serialization with proper error handling

## Usage

### Using the Decorator on Endpoints

```python
from src.api.utils.api_logging import log_api_call
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/endpoint")
@log_api_call("endpoint_name")
def my_endpoint(payload: MySchema, db: Session = Depends(get_db)):
    """Your endpoint logic here"""
    return result
```

### Enabling HTTP Middleware

In your `main.py`:

```python
from src.api.utils.api_logging import log_http_middleware

app = FastAPI()

# Add middleware (should be one of the first)
log_http_middleware(app)

# Then add other middleware and routes
app.add_middleware(CORSMiddleware, ...)
```

## Log Format

### API Call Logs

**Request:**
```
API_CALL_START | Endpoint: user_signup | User: ANONYMOUS | Payload: {"username": "john_doe", "email": "john@example.com", "password": "***REDACTED***"}
```

**Success Response:**
```
API_CALL_SUCCESS | Endpoint: user_signup | User: eyJ0eXAiOiJKV1QiLi.. | Status: 200 | Duration: 0.145s | Response: {"access_token": "***REDACTED***", "token_type": "bearer"}
```

**Error Response:**
```
API_CALL_ERROR | Endpoint: user_login | User: ANONYMOUS | Error: Invalid email or password | Duration: 0.032s
```

### HTTP Middleware Logs

**Request:**
```
HTTP_REQUEST | Method: POST | Path: /auth/signup | User: ANONYMOUS | Query: None | Body: {"username": "john_doe", "email": "john@example.com", "password": "***REDACTED***"}
```

**Response:**
```
HTTP_RESPONSE | Method: POST | Path: /auth/signup | User: ANONYMOUS | Status: 200 | Duration: 0.145s
```

## Available Log Decorators

The following endpoints have logging enabled:

### Authentication
- `user_signup` - POST /auth/signup
- `user_login` - POST /auth/login
- `get_current_user` - GET /auth/me

### Chat Sessions
- `get_user_sessions` - GET /chats/sessions
- `create_chat_session` - POST /chats/sessions
- `get_session_messages` - GET /chats/sessions/{session_id}
- `delete_chat_session` - DELETE /chats/sessions/{session_id}

### Document Ingestion
- `ingest_documents` - POST /ingest/
- `upload_files` - POST /ingest/upload

### Query & Chat
- `query_documents` - POST /query/

## Sensitive Data Handling

The logging system automatically redacts the following fields:
- `password`
- `hashed_password`
- `token`
- `access_token`
- `secret`

Any of these fields in payloads or responses will be replaced with `***REDACTED***`.

## Configuration

The logging module uses the application's logger configured in `src/utils/logger.py`.

### Log Levels
- `INFO`: API calls started/completed successfully
- `ERROR`: API calls with exceptions
- `WARNING`: Issues extracting user information

### Log Output
Logs are written to configured handlers (console, file, etc.) as specified in the logger configuration.

## Example Integration

```python
# In src/api/routers/your_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.utils.api_logging import log_api_call
from src.api.dependencies.auth_dep import get_db, get_current_user

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/users")
@log_api_call("create_user")
def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    """Create a new user"""
    user = User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/{user_id}")
@log_api_call("get_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
@log_api_call("delete_user")
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
```

## Log Analysis

### Monitoring User Activity
Filter logs by User ID to see all activities for a specific user:
```
grep "User: john_doe" logs/app.log
```

### Finding Failed Operations
```
grep "API_CALL_ERROR" logs/app.log
```

### Performance Monitoring
Track endpoint performance:
```
grep "API_CALL_SUCCESS" logs/app.log | awk -F'Duration:' '{print $2}' | sort -n
```

### Audit Trail
Complete audit trail of all API access:
```
grep "HTTP_REQUEST\|HTTP_RESPONSE" logs/app.log
```

## Troubleshooting

### "Unable to extract user from request"
This warning appears when the Authorization header is missing or malformed. This is expected for unauthenticated endpoints.

### "Unable to serialize payload"
This occurs when the payload contains non-JSON-serializable objects. The log will show a generic message instead.

### Missing logs
Ensure:
1. Logger is properly configured in `src/utils/logger.py`
2. Log handler is writing to appropriate destination (console/file)
3. Log level is set to INFO or lower

## Performance Impact

The logging system is designed to be lightweight:
- Decorator adds minimal overhead (~1-5ms per request)
- Payload serialization is cached and optimized
- No blocking I/O operations in critical path
- Async middleware for HTTP logging

## Best Practices

1. **Always decorate endpoints** - Apply `@log_api_call()` to all endpoints for consistency
2. **Use descriptive names** - Choose clear endpoint names for the decorator
3. **Monitor sensitive operations** - Ensure sensitive endpoints are logged
4. **Review logs regularly** - Check logs for unusual activity
5. **Archive logs** - Implement log rotation and archival strategy
6. **Test sensitive data handling** - Verify sensitive fields are properly redacted
