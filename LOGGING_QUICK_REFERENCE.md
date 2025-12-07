# API Logging - Quick Reference

## Decorator Usage

```python
from src.api.utils.api_logging import log_api_call

@router.post("/endpoint")
@log_api_call("endpoint_name")
def endpoint(payload: Schema):
    return result
```

## Log Messages

### API Call Decorator
- **START:** `API_CALL_START | Endpoint: {name} | User: {user} | Payload: {payload}`
- **SUCCESS:** `API_CALL_SUCCESS | Endpoint: {name} | User: {user} | Status: 200 | Duration: {time}s | Response: {response}`
- **ERROR:** `API_CALL_ERROR | Endpoint: {name} | User: {user} | Error: {error} | Duration: {time}s`

### HTTP Middleware
- **REQUEST:** `HTTP_REQUEST | Method: {method} | Path: {path} | User: {user} | Query: {params} | Body: {body}`
- **RESPONSE:** `HTTP_RESPONSE | Method: {method} | Path: {path} | User: {user} | Status: {code} | Duration: {time}s`

## Endpoints with Logging

| Feature | Endpoint | Decorator |
|---------|----------|-----------|
| **Auth** | POST /auth/signup | user_signup |
| | POST /auth/login | user_login |
| | GET /auth/me | get_current_user |
| **Chat** | GET /chats/sessions | get_user_sessions |
| | POST /chats/sessions | create_chat_session |
| | GET /chats/sessions/{id} | get_session_messages |
| | DELETE /chats/sessions/{id} | delete_chat_session |
| **Ingest** | POST /ingest/ | ingest_documents |
| | POST /ingest/upload | upload_files |
| **Query** | POST /query/ | query_documents |

## Redacted Fields
- password
- hashed_password
- token
- access_token
- secret

## Enabling Logging

In `main.py`:
```python
from src.api.utils.api_logging import log_http_middleware

app = FastAPI()
log_http_middleware(app)  # Enable global logging
```

## Viewing Logs

```bash
# All logs
tail -f logs/app.log

# API calls only
grep "API_CALL" logs/app.log

# Errors only
grep "API_CALL_ERROR" logs/app.log

# Specific endpoint
grep "query_documents" logs/app.log

# User activity
grep "User: user123" logs/app.log
```

## Log Locations
Logs are written to locations configured in `src/utils/logger.py`
Default: Console output + file handler

## Notes
- User ID extracted from JWT Bearer token
- Unauthenticated requests show "ANONYMOUS"
- Long tokens truncated to first 20 chars + "..."
- Execution times in seconds with 3 decimal precision
