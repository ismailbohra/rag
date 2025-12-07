# Logging System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Request                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────┐
         │   log_http_middleware (Global)   │
         │                                  │
         │  - Log HTTP method & path        │
         │  - Extract user from JWT         │
         │  - Log request body              │
         │  - Track execution time          │
         └────────────┬──────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  FastAPI Router Handler    │
        │  (auth, chat, etc)         │
        └──────────┬──────────────────┘
                   │
                   ▼
       ┌─────────────────────────────────┐
       │  @log_api_call() Decorator      │
       │                                 │
       │  - Log endpoint name            │
       │  - Redact sensitive fields      │
       │  - Log payload/request          │
       │  - Measure execution time       │
       │  - Capture response             │
       │  - Log errors with traceback    │
       └──────────┬──────────────────────┘
                  │
                  ▼
        ┌──────────────────────┐
        │  Endpoint Function  │
        │  (Business Logic)   │
        └──────────┬──────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
   Success                   Error
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
    ┌────────────────────────────────┐
    │  Response Serialization        │
    │  - Format payload              │
    │  - Redact sensitive data       │
    │  - Convert to JSON             │
    └────────────┬───────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │  Logger Output                 │
    │  - Console                     │
    │  - File handlers               │
    │  - Custom formatters           │
    └────────────┬───────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │  HTTP Response                 │
    │  (Sent to Client)              │
    └────────────────────────────────┘
```

## Component Details

### 1. log_http_middleware(app)

**Type:** ASGI Middleware

**Responsibilities:**
- Intercepts ALL HTTP requests before they reach routers
- Extracts user ID from JWT token in Authorization header
- Logs complete request details (method, path, query params, body)
- Measures total execution time
- Logs response status code

**Input:**
```
GET /chats/sessions
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Output:**
```
HTTP_REQUEST | Method: GET | Path: /chats/sessions | User: user123 | Query: None | Body: None
HTTP_RESPONSE | Method: GET | Path: /chats/sessions | User: user123 | Status: 200 | Duration: 0.045s
```

### 2. @log_api_call(endpoint_name) Decorator

**Type:** Function Decorator

**Responsibilities:**
- Wraps endpoint functions
- Logs endpoint name and user ID
- Extracts and redacts payload from Pydantic models
- Measures function execution time
- Captures response and formats for logging
- Catches and logs exceptions with stack traces

**Input:**
```python
@log_api_call("user_signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # Logic
```

**Output:**
```
API_CALL_START | Endpoint: user_signup | User: ANONYMOUS | Payload: {"username": "john", "password": "***REDACTED***"}
API_CALL_SUCCESS | Endpoint: user_signup | User: eyJhbGciOiJIUzI... | Status: 200 | Duration: 0.123s | Response: {...}
```

### 3. extract_user_id(request)

**Type:** Helper Function

**Responsibilities:**
- Extracts user ID from JWT Bearer token
- Returns token prefix if full ID extraction not needed
- Gracefully handles missing/malformed headers
- Returns "ANONYMOUS" for unauthenticated requests

**Processing:**
```
Header: "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
          ↓
      Extract Token
          ↓
      Return: "eyJhbGciOiJIUzI1NiIsInR5cC..." (first 20 chars + "...")
```

### 4. format_payload(data)

**Type:** Helper Function

**Responsibilities:**
- Converts Python objects to JSON strings
- Recursively searches for sensitive field names
- Replaces sensitive values with "***REDACTED***"
- Handles non-JSON-serializable objects gracefully
- Preserves data structure for readability

**Sensitive Fields:**
- password
- hashed_password
- token
- access_token
- secret

**Processing:**
```
Input: {
    "username": "john",
    "email": "john@example.com",
    "password": "secret123"
}

Output: {"username": "john", "email": "john@example.com", "password": "***REDACTED***"}
```

## Data Flow

### Request Path

```
1. HTTP Request arrives
   ↓
2. ASGI Middleware (log_http_middleware)
   - Log HTTP_REQUEST
   - Extract user from JWT
   - Log path, method, params, body
   ↓
3. FastAPI Route Handler
   - Match request to router
   ↓
4. Endpoint Function (with @log_api_call decorator)
   a. Decorator logs API_CALL_START
   b. Extract user ID
   c. Extract and format payload
   d. Log start message
   ↓
5. Function Execution (Business Logic)
   - Process payload
   - Query database
   - Generate response
   ↓
6. Response Processing (Decorator)
   - Measure execution time
   - Format response
   - Check for errors
   ↓
7. Logging
   - Log API_CALL_SUCCESS (success case)
   - Log API_CALL_ERROR (error case)
   - Include duration, response/error details
   ↓
8. Return Response
   - Send to client (via middleware)
   - Log HTTP_RESPONSE
   - Complete request cycle
```

### Error Path

```
1. Exception raised in endpoint function
   ↓
2. Decorator catches exception
   ↓
3. Extract error details
   - Error message
   - Stack trace
   - Execution time
   ↓
4. Log API_CALL_ERROR with full context
   ↓
5. Re-raise exception
   ↓
6. FastAPI error handler
   - Convert to HTTP response
   - Send error to client
   ↓
7. Middleware logs HTTP_RESPONSE with error status code
```

## Integration Points

### 1. With FastAPI Application

```python
# main.py
from fastapi import FastAPI
from src.api.utils.api_logging import log_http_middleware

app = FastAPI()

# Register middleware early
log_http_middleware(app)

# Add other middleware
app.add_middleware(CORSMiddleware, ...)

# Include routers
app.include_router(auth_router)
```

### 2. With Routers

```python
# src/api/routers/auth_router.py
from src.api.utils.api_logging import log_api_call

@router.post("/signup", response_model=Token)
@log_api_call("user_signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # Logic
```

### 3. With Existing Logger

```python
# src/api/utils/api_logging.py
from src.utils.logger import get_logger

logger = get_logger(__name__)

# All logs written through existing logger
logger.info("API_CALL_START | ...")
logger.error("API_CALL_ERROR | ...", exc_info=True)
```

## Log Output Hierarchy

```
src/utils/logger.py (Central Logger Configuration)
           ↓
    Handlers (Console, File, etc)
           ↓
    Formatters (Log format/structure)
           ↓
    Output Destinations
           ├── Console (stdout)
           ├── File (logs/app.log)
           └── Custom handlers
```

## Performance Considerations

### Overhead Analysis

| Component | Overhead | Notes |
|-----------|----------|-------|
| HTTP Middleware | 2-8ms | Per request, non-blocking |
| Decorator | 1-5ms | Per endpoint call |
| Payload Serialization | <1ms | Usually cached |
| Logging I/O | Variable | Depends on handler config |
| **Total** | **3-13ms** | Per request typical |

### Optimization Strategies

1. **Async Middleware** - Non-blocking HTTP logging
2. **Lazy Evaluation** - Payload only serialized if logged
3. **String Concatenation** - Minimal string operations
4. **Caching** - Reuse serialized payloads
5. **Sampling** - Could implement for high-volume endpoints

## Security Considerations

### Data Protection

1. **Sensitive Field Redaction**
   - Automatic identification and redaction
   - Covers all standard sensitive fields
   - Customizable field list

2. **Token Handling**
   - Full token never logged
   - Only prefix shown (first 20 chars)
   - Helps identify token but prevents reuse

3. **User Identification**
   - Anonymous requests labeled clearly
   - Token extraction safe and validated
   - No password/auth data in logs

### Audit Trail

1. **User Activity Tracking**
   - All API calls attributed to user
   - Complete request/response captured
   - Timestamp and duration recorded

2. **Error Tracking**
   - Stack traces preserved
   - Error context maintained
   - Helps with security incident investigation

## Monitoring & Analytics

### Available Metrics

From logs, can extract:
- API call frequency per endpoint
- User activity patterns
- Error rates and types
- Performance metrics (response times)
- Authentication attempts
- Data access patterns

### Log Analysis Examples

```bash
# Error rate
grep "API_CALL_ERROR" app.log | wc -l

# Slowest endpoints
grep "API_CALL_SUCCESS" app.log | sort -t':' -k4 -rn | head -10

# Most active users
grep "User:" app.log | cut -d'|' -f3 | sort | uniq -c | sort -rn

# Failed logins
grep "API_CALL_ERROR.*user_login" app.log
```

## Troubleshooting Guide

### Issue: Missing logs for specific endpoint

**Solution:**
1. Verify @log_api_call decorator is applied
2. Check logger configuration in src/utils/logger.py
3. Ensure log level is set to INFO or lower
4. Verify handler is enabled and writable

### Issue: Sensitive data visible in logs

**Solution:**
1. Add field name to redaction list in format_payload()
2. Example: Add 'ssn' to sensitive_fields list
3. Restart application

### Issue: Performance impact too high

**Solution:**
1. Use async-aware logging handlers
2. Implement log sampling for high-volume endpoints
3. Store logs to fast disk (SSD)
4. Implement log rotation to prevent disk full

### Issue: User ID always "ANONYMOUS"

**Solution:**
1. Verify JWT token is present in Authorization header
2. Check header format: "Bearer {token}"
3. Ensure token contains user_id claim
4. Verify JWT secret matches signing secret
