"""
Quick test to verify API logging is working
Run with: python test_logging.py
"""
import asyncio
from src.api.main import app
from src.api.utils.api_logging import format_payload, extract_user_id
from src.utils.logger import get_logger

logger = get_logger(__name__)

def test_format_payload():
    """Test sensitive data redaction"""
    print("\n✅ Testing format_payload()...")
    
    payload = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "MySecurePassword123!",
        "token": "secret_token_xyz",
        "access_token": "jwt_token_abc",
        "api_key": "not_redacted_123"
    }
    
    formatted = format_payload(payload)
    print(f"Original keys: {list(payload.keys())}")
    print(f"Formatted: {formatted}")
    
    # Verify redaction
    assert "***REDACTED***" in formatted, "password not redacted!"
    assert "MySecurePassword123!" not in formatted, "password visible!"
    assert "secret_token_xyz" not in formatted, "token visible!"
    assert "jwt_token_abc" not in formatted, "access_token visible!"
    assert "john_doe" in formatted, "non-sensitive data removed!"
    assert "john@example.com" in formatted, "email data removed!"
    
    print("✅ format_payload() working correctly")

def test_imports():
    """Test all imports work"""
    print("\n✅ Testing imports...")
    
    try:
        from src.api.utils.api_logging import log_api_call, log_http_middleware
        from src.api.routers.auth_router import router as auth_router
        from src.api.routers.chat_router import router as chat_router
        from src.api.routers.ingest_router import router as ingest_router
        from src.api.routers.query_router import router as query_router
        print("✅ All routers imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        raise

def test_logger():
    """Test logger is working"""
    print("\n✅ Testing logger...")
    
    try:
        logger.info("Test log message - INFO level")
        logger.warning("Test log message - WARNING level")
        logger.error("Test log message - ERROR level")
        print("✅ Logger working correctly")
        print("✅ Check logs/app.log for logged messages")
    except Exception as e:
        print(f"❌ Logger error: {e}")
        raise

def test_app_startup():
    """Test FastAPI app initializes"""
    print("\n✅ Testing FastAPI app...")
    
    try:
        assert app is not None, "App is None!"
        assert len(app.routes) > 0, "No routes registered!"
        print(f"✅ FastAPI app initialized with {len(app.routes)} routes")
        print(f"✅ Middleware count: {len(app.user_middleware)}")
    except Exception as e:
        print(f"❌ App error: {e}")
        raise

def main():
    """Run all tests"""
    print("=" * 60)
    print("API Logging System - Quick Test")
    print("=" * 60)
    
    try:
        test_imports()
        test_logger()
        test_format_payload()
        test_app_startup()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nLogging system is ready to use!")
        print("Run: uvicorn src.api.main:app --reload")
        print("Then check logs/app.log for API call logs")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
