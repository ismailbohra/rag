# API Logging - Visual Diagrams

## 1. Request/Response Flow with Logging

```
┌──────────────────────────────────────────────────────────────────────┐
│                         API Request Lifecycle                        │
└──────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────────┐
                        │   HTTP Request      │
                        │  POST /auth/signup  │
                        └────────┬────────────┘
                                 │
                    ┌────────────▼──────────────┐
                    │  HTTP Middleware Logs     │  ← 🔍 HTTP_REQUEST
                    │  - Method: POST           │     Logged here
                    │  - Path: /auth/signup     │
                    │  - User: ANONYMOUS       │
                    │  - Body: {...}           │
                    └────────────┬──────────────┘
                                 │
                    ┌────────────▼──────────────┐
                    │  Route Matching           │
                    │  Find endpoint handler    │
                    └────────────┬──────────────┘
                                 │
                    ┌────────────▼──────────────────────┐
                    │  @log_api_call Decorator Starts   │  ← 🔍 API_CALL_START
                    │  ┌──────────────────────────────┐ │     Logged here
                    │  │ - Endpoint: user_signup      │ │
                    │  │ - User: ANONYMOUS           │ │
                    │  │ - Payload: {...}            │ │
                    │  └──────────────────────────────┘ │
                    └────────────┬──────────────────────┘
                                 │
                    ┌────────────▼──────────────────────┐
                    │  Endpoint Function Executes       │
                    │  signup(payload, db)              │
                    │  - Validate input                 │
                    │  - Create user                    │
                    │  - Generate JWT token            │
                    └────────────┬──────────────────────┘
                                 │
                    ┌────────────┴──────────────────────┐
                    │                                    │
            ┌───────▼───────┐              ┌────────────▼──────────┐
            │    SUCCESS    │              │      EXCEPTION        │
            │               │              │                       │
            │  Return {     │              │  Raise HTTPException  │
            │  access_token │              │  or other error       │
            │  }            │              │                       │
            └───────┬───────┘              └────────────┬──────────┘
                    │                                    │
                    │         ┌──────────────────────────┤
                    │         │                          │
            ┌───────▼──────────▼─────────────────────┐
            │  @log_api_call Decorator Ends          │  ← 🔍 API_CALL_SUCCESS/ERROR
            │  ┌────────────────────────────────────┐│     Logged here
            │  │ Success:                           ││
            │  │ - Status: 200                      ││
            │  │ - Duration: 0.142s                 ││
            │  │ - Response: {...}                  ││
            │  │                                    ││
            │  │ OR                                 ││
            │  │                                    ││
            │  │ Error:                             ││
            │  │ - Error message                    ││
            │  │ - Duration: 0.045s                 ││
            │  │ - Stack trace                      ││
            │  └────────────────────────────────────┘│
            └───────┬──────────────────────────────────┘
                    │
            ┌───────▼─────────────────────────────────┐
            │  HTTP Middleware Logs Response          │  ← 🔍 HTTP_RESPONSE
            │  - Method: POST                         │     Logged here
            │  - Path: /auth/signup                   │
            │  - User: eyJ0eXAiOiJKV...              │
            │  - Status: 200 or 400/500              │
            │  - Duration: 0.145s                     │
            └───────┬─────────────────────────────────┘
                    │
            ┌───────▼─────────────────────────────────┐
            │     HTTP Response to Client             │
            │     {                                   │
            │       "access_token": "...",            │
            │       "token_type": "bearer"            │
            │     }                                   │
            └─────────────────────────────────────────┘
```

---

## 2. Two-Layer Logging Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    API Request Handling Stack                     │
└────────────────────────────────────────────────────────────────────┘

                          LAYER 1
                 ╔═══════════════════════╗
                 ║  HTTP MIDDLEWARE LOG  ║
                 ║  (Global, all routes) ║
                 ╚═════════╤═════════════╝
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    Logs:            Logs:               Logs:
    - Path           - Method            - Query
    - User           - Status Code       - User ID
    - Execution      - Duration          - Timestamp
    - All requests   - All responses

                      ROUTER LAYER
              ┌────────────────────────────┐
              │  FastAPI Router/Endpoints  │
              │  (auth, chat, ingest, etc) │
              └────────────┬───────────────┘
                           │
                          LAYER 2
            ╔══════════════════════════════════╗
            ║  @log_api_call DECORATOR LOG     ║
            ║  (Endpoint-specific)             ║
            ╚══════════════╤═══════════════════╝
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    Logs:            Logs:               Logs:
    - Endpoint       - User ID           - Response
    - Payload        - Duration          - Errors
    - Request        - Status            - Stack trace
    - Response       - Errors

                   BUSINESS LOGIC
         ┌────────────────────────────────┐
         │  Your endpoint function        │
         │  (signup, create_session, etc) │
         └────────────────────────────────┘
```

---

## 3. Sensitive Data Redaction Flow

```
Input Data:
┌────────────────────────────────────┐
│ {                                  │
│   "username": "john_doe",          │
│   "email": "john@example.com",     │
│   "password": "SecurePass123!",    │
│   "api_token": "secret_key_xyz"    │
│ }                                  │
└──────────────┬──────────────────────┘
               │
       ┌───────▼────────────┐
       │ Check Field Names  │
       │ Against Sensitive  │
       │ Field List:        │
       │ - password        │
       │ - hashed_password │
       │ - token           │
       │ - access_token    │
       │ - secret          │
       └───────┬────────────┘
               │
┌──────────────┴──────────────┐
│                             │
▼                             ▼
SENSITIVE              NOT SENSITIVE
FIELDS                 FIELDS
│                      │
│                      ├─ username: "john_doe"
│                      └─ email: "john@example.com"
│
├─ password (found!)
│   └─ Replace: "***REDACTED***"
│
└─ api_token (found!)
    └─ Replace: "***REDACTED***"

Output Data:
┌────────────────────────────────────┐
│ {                                  │
│   "username": "john_doe",          │
│   "email": "john@example.com",     │
│   "password": "***REDACTED***",    │
│   "api_token": "***REDACTED***"    │
│ }                                  │
└────────────────────────────────────┘
```

---

## 4. Endpoint Decorator Pattern

```
WITHOUT Decorator:
┌─────────────────────────────┐
│ @router.post("/endpoint")   │  ← No logging
│ def endpoint(payload):      │
│     # Do work               │
│     return result           │
└─────────────────────────────┘


WITH Decorator:
┌─────────────────────────────────────────┐
│ @router.post("/endpoint")               │
│ @log_api_call("endpoint_name")          │  ← Logging added
│ def endpoint(payload):                  │
│     # Do work                           │
│     return result                       │
└─────────────────────────────────────────┘

Execution Flow:
┌──────────────────────────────────────────────────┐
│         @log_api_call Wrapper                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  1. Log START                                    │
│     ├─ API_CALL_START                          │
│     ├─ Endpoint name                           │
│     └─ Payload (redacted)                      │
│                                                 │
│  2. Execute Function                            │
│     ├─ Start timer                             │
│     ├─ Call original function                  │
│     └─ Catch any exceptions                    │
│                                                 │
│  3. Log RESULT                                  │
│     ├─ API_CALL_SUCCESS or ERROR               │
│     ├─ Duration                                │
│     └─ Response or Error info                  │
│                                                 │
│  4. Return Result                               │
│     └─ To caller or re-raise exception         │
│                                                 │
└──────────────────────────────────────────────────┘
```

---

## 5. User Identification Flow

```
HTTP Request:
┌────────────────────────────────────────────┐
│ POST /auth/signup                          │
│ Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... │
│ Content-Type: application/json             │
│ ...                                        │
└────────────┬─────────────────────────────────┘
             │
    ┌────────▼────────────────┐
    │  Extract JWT Token from │
    │  Authorization Header   │
    └────────┬────────────────┘
             │
    ┌────────▼────────────────────────────────────────┐
    │  Validate Token Format                         │
    │  Must start with "Bearer "                     │
    └────────┬────────────────────────────────────────┘
             │
    ┌────────▼────────────────────────────────────────┐
    │  If Valid:                                     │
    │  - Take token                                  │
    │  - Return first 20 chars + "..."               │
    │  - Example: eyJ0eXAiOiJKV1QiLCJhbGc...        │
    │                                                │
    │  If Invalid/Missing:                           │
    │  - Return "ANONYMOUS"                          │
    └────────┬────────────────────────────────────────┘
             │
    ┌────────▼──────────────────┐
    │  Use in Log Messages      │
    │  "User: eyJ0eXAiOi...     │
    │  "User: ANONYMOUS"        │
    └───────────────────────────┘
```

---

## 6. Log Output Destinations

```
Logger Configuration (src/utils/logger.py)
            │
    ┌───────┴───────┬──────────┬──────────┐
    │               │          │          │
    ▼               ▼          ▼          ▼
 Console    File Handler  Syslog?   Custom?
    │               │          │          │
    │           logs/          │          │
    │           app.log        │          │
    │               │          │          │
    └───────────────┼──────────┼──────────┘
                    │          │
            Real-time      Permanent
            Viewing        Storage

Log Content:
┌──────────────────────────────────────────────┐
│ 2024-12-07 10:30:45,123 - INFO               │
│ API_CALL_START | Endpoint: user_signup |     │
│ User: ANONYMOUS | Payload: {...}            │
├──────────────────────────────────────────────┤
│ 2024-12-07 10:30:45,265 - INFO               │
│ API_CALL_SUCCESS | Endpoint: user_signup |   │
│ User: eyJ0eXAi... | Duration: 0.142s         │
└──────────────────────────────────────────────┘
```

---

## 7. Error Handling Flow

```
Function Execution:
┌─────────────────────────────┐
│ try:                        │
│   result = func(...)        │
│   return result             │
└─────────────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
 Success    Exception
    │          │
    │      ┌───▼───────────────────┐
    │      │ Catch Exception        │
    │      │ - Get error message    │
    │      │ - Get stack trace      │
    │      │ - Record duration      │
    │      └───┬───────────────────┘
    │          │
    │      ┌───▼──────────────────────────────┐
    │      │ Log API_CALL_ERROR               │
    │      │ - Endpoint name                  │
    │      │ - User identification            │
    │      │ - Error message                  │
    │      │ - Execution time                 │
    │      │ - Stack trace                    │
    │      └───┬──────────────────────────────┘
    │          │
    │      ┌───▼──────────────────────────────┐
    │      │ Re-raise Exception               │
    │      │ (Let FastAPI handle it)          │
    │      └───┬──────────────────────────────┘
    │          │
    └──────────┼──────────────────┐
               │                  │
           ┌───▼────┐        ┌───▼────┐
           │ Success│        │ Error  │
           │ Response        │Response│
           └────────┘        └────────┘
```

---

## 8. Performance Impact Visualization

```
Typical Request Timeline (milliseconds):

Without Logging:
┌────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ Business Logic    │
│ 0          50          100        150       │
│ Total: ~145ms                               │
└────────────────────────────────────────────┘


With Logging:
┌────────────────────────────────────────────┐
│ ▒ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ░               │
│ 0 2 50          100        150   152       │
│ ▒ = Decorator overhead (~2-5ms)            │
│ ░ = Middleware logging (~3-8ms)            │
│ Total: ~150-160ms (~4-7% overhead)         │
└────────────────────────────────────────────┘

Summary:
- Decorator adds: 1-5ms
- Middleware adds: 2-8ms
- Total overhead: 3-13ms per request
- Acceptable for most applications
- Use caching/async for high-volume endpoints
```

---

## 9. Security: Data Flow

```
Sensitive Data in Request:
┌─────────────────────────────────┐
│ {                               │
│   "password": "MySecret123!",   │
│   "email": "user@example.com"   │
│ }                               │
└────────────┬────────────────────┘
             │
    ┌────────▼──────────────────────┐
    │ Logging Module Receives Data  │
    │ format_payload() function     │
    └────────┬──────────────────────┘
             │
    ┌────────▼──────────────────────────────┐
    │ Scan Field Names                      │
    │ Is "password" in sensitive list?      │
    │ YES → Replace with "***REDACTED***"   │
    └────────┬──────────────────────────────┘
             │
    ┌────────▼──────────────────────┐
    │ Redacted Data in Log:         │
    │ {                             │
    │   "password": "***REDACTED*",│
    │   "email": "user@example.com" │
    │ }                             │
    └──────────────────────────────┘

Result:
✅ Sensitive data NEVER appears in logs
✅ Email safely logged (not sensitive)
✅ Password replaced before logging
✅ Meets security compliance requirements
```

---

## 10. Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          API Gateway                            │
│                    (Client Requests Enter)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────▼────────────────┐
         │  ASGI Middleware Stack         │
         ├────────────────────────────────┤
         │                                │
         │  1. log_http_middleware        │  ← 🔍 HTTP_REQUEST
         │     └─ Logs all requests       │     🔍 HTTP_RESPONSE
         │                                │
         │  2. CORSMiddleware             │
         │                                │
         │  3. Other middleware...        │
         │                                │
         └────────────┬────────────────────┘
                      │
         ┌────────────▼──────────────────┐
         │  FastAPI Route Handler        │
         │  (Matches request to endpoint)│
         └────────────┬──────────────────┘
                      │
         ┌────────────▼─────────────────────┐
         │  Router Handlers                 │
         ├──────────────────────────────────┤
         │                                  │
         │  auth_router ────┬─────────────┐ │
         │  ├─ signup()     │ @log_api_   │ │
         │  ├─ login()      │ call()      │ │
         │  └─ get_me()     │             │ │
         │                  └──┬──────────┘ │
         │  chat_router ────┬─────────────┐ │
         │  ├─ get_sessions()│ @log_api_  │ │
         │  ├─ create_s()    │ call()     │ │
         │  └─ delete_s()    │            │ │
         │                  └──┬──────────┘ │
         │  ingest_router ──┬─────────────┐ │
         │  ├─ ingest()     │ @log_api_   │ │
         │  └─ upload()     │ call()      │ │
         │                  └──┬──────────┘ │
         │  query_router ───┬─────────────┐ │
         │  └─ query()      │ @log_api_   │ │
         │                  │ call()      │ │
         │                  └──┬──────────┘ │
         │                     │            │
         └─────────────────────┼────────────┘
                               │
              ┌────────────────▼────────────┐
              │  Business Logic             │
              │  (DB operations, RAG, etc)  │
              └────────────┬─────────────────┘
                           │
              ┌────────────▼────────────┐
              │  Logger Instance        │
              │  (src/utils/logger.py)  │
              └────────────┬────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
         Console        File (logs/)   Other Handlers
          Output        app.log        (Syslog, etc)

Legend:
🔍 = Logging point
```

---

## Summary

These diagrams show:
1. **Request flow** - How a request goes through the logging system
2. **Two-layer logging** - Middleware + decorator approach
3. **Data redaction** - How sensitive data is protected
4. **Decorator pattern** - How logging is added to endpoints
5. **User identification** - How users are identified from JWTs
6. **Output destinations** - Where logs are stored
7. **Error handling** - How exceptions are logged
8. **Performance** - Minimal overhead visualization
9. **Security** - Data protection mechanisms
10. **Complete architecture** - Full system overview
