# API Logging - Examples

This document shows actual examples of what logs will look like for different scenarios.

## Example 1: User Signup - Success

### Request
```
POST /auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "MySecurePassword123!"
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /auth/signup | User: ANONYMOUS | Query: None | Body: {"username": "john_doe", "email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: user_signup | User: ANONYMOUS | Payload: {"username": "john_doe", "email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: user_signup | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.142s | Response: {"access_token": "***REDACTED***", "token_type": "bearer"}
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /auth/signup | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.145s
```

---

## Example 2: User Login - Success

### Request
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "MySecurePassword123!"
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /auth/login | User: ANONYMOUS | Query: None | Body: {"email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: user_login | User: ANONYMOUS | Payload: {"email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: user_login | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.035s | Response: {"access_token": "***REDACTED***", "token_type": "bearer"}
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /auth/login | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.038s
```

---

## Example 3: User Login - Failed

### Request
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "WrongPassword!"
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /auth/login | User: ANONYMOUS | Query: None | Body: {"email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: user_login | User: ANONYMOUS | Payload: {"email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Error:**
```
API_CALL_ERROR | Endpoint: user_login | User: ANONYMOUS | Error: Invalid email or password | Duration: 0.032s
Traceback (most recent call last):
  File "src/api/routers/auth_router.py", line 56, in login
    raise HTTPException(status_code=401, detail="Invalid email or password")
HTTPException: Invalid email or password
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /auth/login | User: ANONYMOUS | Status: 401 | Duration: 0.035s
```

---

## Example 4: Create Chat Session - Success

### Request
```
POST /chats/sessions
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTcwMzAwMDAwMH0.abc123...
Content-Type: application/json

{
  "title": "Python Tutorial Discussion"
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /chats/sessions | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Query: None | Body: {"title": "Python Tutorial Discussion"}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: create_chat_session | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Payload: {"title": "Python Tutorial Discussion"}
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: create_chat_session | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.028s | Response: {"id": 5, "title": "Python Tutorial Discussion", "created_at": "2024-12-07T10:30:45.123456", "last_activity": "2024-12-07T10:30:45.123456"}
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /chats/sessions | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.031s
```

---

## Example 5: Query Documents - Success

### Request
```
POST /query/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTcwMzAwMDAwMH0.abc123...
Content-Type: application/json

{
  "query": "What is machine learning?",
  "session_id": 5,
  "top_k": 5
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /query/ | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Query: None | Body: {"query": "What is machine learning?", "session_id": 5, "top_k": 5}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: query_documents | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Payload: {"query": "What is machine learning?", "session_id": 5, "top_k": 5}
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: query_documents | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 2.345s | Response: {"answer": "Machine learning is a subset of artificial intelligence...", "citations": [{"source": "ml_fundamentals.pdf", "score": 0.92}, {"source": "ai_basics.pdf", "score": 0.87}]}
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /query/ | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 2.348s
```

---

## Example 6: Get Current User - Success

### Request
```
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTcwMzAwMDAwMH0.abc123...
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: GET | Path: /auth/me | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Query: None | Body: None
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: get_current_user | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Payload: None
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: get_current_user | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.012s | Response: {"id": 1, "username": "john_doe", "email": "john@example.com", "created_at": "2024-12-01T08:15:30.000000"}
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: GET | Path: /auth/me | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 0.015s
```

---

## Example 7: File Upload - Success

### Request
```
POST /ingest/upload
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTcwMzAwMDAwMH0.abc123...
Content-Type: multipart/form-data

Files:
  - document1.pdf (2.5 MB)
  - document2.pdf (1.8 MB)
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /ingest/upload | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Query: None | Body: <Unable to read body>
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: upload_files | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Payload: None
```

**Endpoint Decorator - Success:**
```
API_CALL_SUCCESS | Endpoint: upload_files | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 5.234s | Response: [{"filename": "document1.pdf", "chunks_created": 45, "total_size": 2621440}, {"filename": "document2.pdf", "chunks_created": 32, "total_size": 1887436}]
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /ingest/upload | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 200 | Duration: 5.237s
```

---

## Example 8: Delete Session - Authorization Failure

### Request
```
DELETE /chats/sessions/999
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTcwMzAwMDAwMH0.abc123...
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: DELETE | Path: /chats/sessions/999 | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Query: None | Body: None
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: delete_chat_session | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Payload: None
```

**Endpoint Decorator - Error:**
```
API_CALL_ERROR | Endpoint: delete_chat_session | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Error: Session not found | Duration: 0.018s
Traceback (most recent call last):
  File "src/api/routers/chat_router.py", line 110, in delete_session
    raise HTTPException(status_code=404, detail="Session not found")
HTTPException: Session not found
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: DELETE | Path: /chats/sessions/999 | User: eyJ0eXAiOiJKV1QiLCJhbGc... | Status: 404 | Duration: 0.021s
```

---

## Example 9: Missing Authentication Token

### Request
```
GET /chats/sessions
(No Authorization header)
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: GET | Path: /chats/sessions | User: ANONYMOUS | Query: None | Body: None
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: GET | Path: /chats/sessions | User: ANONYMOUS | Status: 401 | Duration: 0.005s
```

Note: Decorator logs are skipped because dependency validation fails before reaching the endpoint.

---

## Example 10: Signup with Duplicate Email

### Request
```
POST /auth/signup
Content-Type: application/json

{
  "username": "john_doe2",
  "email": "john@example.com",
  "password": "MySecurePassword123!"
}
```

### Logs Generated

**HTTP Middleware - Request:**
```
HTTP_REQUEST | Method: POST | Path: /auth/signup | User: ANONYMOUS | Query: None | Body: {"username": "john_doe2", "email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Start:**
```
API_CALL_START | Endpoint: user_signup | User: ANONYMOUS | Payload: {"username": "john_doe2", "email": "john@example.com", "password": "***REDACTED***"}
```

**Endpoint Decorator - Error:**
```
API_CALL_ERROR | Endpoint: user_signup | User: ANONYMOUS | Error: Email already registered | Duration: 0.042s
Traceback (most recent call last):
  File "src/api/routers/auth_router.py", line 33, in signup
    raise HTTPException(status_code=400, detail="Email already registered")
HTTPException: Email already registered
```

**HTTP Middleware - Response:**
```
HTTP_RESPONSE | Method: POST | Path: /auth/signup | User: ANONYMOUS | Status: 400 | Duration: 0.045s
```

---

## Log Patterns for Analysis

### Pattern 1: Track User Activity
```bash
grep "User: eyJ0eXAiOiJKV1QiLCJhbGc" logs/app.log | head -20
```
Shows all API calls by a specific user.

### Pattern 2: Find Failed Attempts
```bash
grep "API_CALL_ERROR.*user_login" logs/app.log
```
Shows all failed login attempts.

### Pattern 3: Performance Monitoring
```bash
grep "API_CALL_SUCCESS.*Duration" logs/app.log | grep "query_documents"
```
Shows query operation durations.

### Pattern 4: Error Rate by Endpoint
```bash
grep "API_CALL_ERROR" logs/app.log | cut -d'|' -f2 | sort | uniq -c
```
Shows which endpoints have most errors.

### Pattern 5: Database Operation Tracking
```bash
grep "HTTP_REQUEST.*ingest" logs/app.log
```
Shows all document ingestion operations.

---

## Key Insights from Logs

### Security Indicators
- Multiple failed logins from same IP → Potential attack
- Signup attempts with similar emails → Bot activity
- Unusual user activity times → Compromised account

### Performance Issues
- Query duration > 5 seconds → Need optimization
- File upload taking too long → Network/storage issue
- High 404 errors → API changes not communicated

### System Health
- Increasing error rate → System degradation
- Failed database operations → Connection issues
- Memory/timeout errors → Resource constraints
