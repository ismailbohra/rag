#!/usr/bin/env python3
"""
Quick-start script for RAG API with JWT Auth & Chat Sessions

This script guides you through the initial setup and testing.
Run: python quickstart.py
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(num, text):
    """Print formatted step."""
    print(f"\n📍 Step {num}: {text}")
    print("-" * 60)


def check_command(cmd, name):
    """Check if a command is available."""
    result = subprocess.run(
        ["which", cmd] if sys.platform != "win32" else ["where", cmd],
        capture_output=True
    )
    if result.returncode == 0:
        print(f"✅ {name} found")
        return True
    else:
        print(f"❌ {name} not found - please install it")
        return False


def check_python_package(package_name, import_name=None):
    """Check if Python package is installed."""
    import_name = import_name or package_name
    try:
        __import__(import_name)
        print(f"✅ {package_name} installed")
        return True
    except ImportError:
        print(f"❌ {package_name} not installed")
        return False


def run_command(cmd, description):
    """Run shell command."""
    print(f"\n🔧 {description}...")
    result = subprocess.run(cmd, shell=True, cwd=str(Path(__file__).parent))
    return result.returncode == 0


def main():
    """Main quickstart flow."""
    print_header("🚀 RAG API Quick Start")
    
    cwd = Path(__file__).parent
    env_file = cwd / ".env"
    env_example = cwd / ".env.example"
    
    # Step 1: Check prerequisites
    print_step(1, "Checking Prerequisites")
    
    checks = [
        check_command("python", "Python"),
        check_command("pip", "pip"),
        check_command("psql", "PostgreSQL client"),
    ]
    
    if not all(checks):
        print("\n⚠️  Please install missing prerequisites and try again")
        return False
    
    # Step 2: Check environment file
    print_step(2, "Environment Configuration")
    
    if not env_file.exists():
        if env_example.exists():
            print(f"📝 Creating {env_file.name} from {env_example.name}...")
            import shutil
            shutil.copy(env_example, env_file)
            print(f"✅ {env_file.name} created")
            print(f"\n⚠️  Please edit {env_file.name} with your configuration:")
            print("   - DATABASE_URL: PostgreSQL connection string")
            print("   - JWT_SECRET: Random secret key")
            print("   - API keys for your LLM providers")
            return False
        else:
            print(f"❌ {env_example.name} not found")
            return False
    else:
        print(f"✅ {env_file.name} exists")
    
    # Step 3: Check Python packages
    print_step(3, "Checking Python Packages")
    
    packages = [
        ("fastapi", "fastapi"),
        ("sqlalchemy", "sqlalchemy"),
        ("pyjwt", "jwt"),
        ("passlib", "passlib"),
    ]
    
    missing_packages = [pkg for pkg, imp in packages if not check_python_package(pkg, imp)]
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Step 4: Install dependencies
    print_step(4, "Installing Dependencies")
    
    if run_command("pip install -r requirements.txt", "Installing packages"):
        print("✅ Packages installed")
    else:
        print("❌ Package installation failed")
        return False
    
    # Step 5: Initialize database
    print_step(5, "Initializing Database")
    
    if run_command("python bootstrap_db.py", "Running database bootstrap"):
        print("✅ Database initialized")
    else:
        print("❌ Database initialization failed")
        print("   Make sure PostgreSQL is running and DATABASE_URL is correct")
        return False
    
    # Step 6: Quick test
    print_step(6, "Quick Health Check")
    
    try:
        from src.models.tables import User, ChatSession, Chat, ChatEmbedding
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return False
    
    try:
        from src.api.utils.auth import create_access_token, decode_access_token
        token = create_access_token("test_user_123")
        payload = decode_access_token(token)
        if payload and payload.get("sub") == "test_user_123":
            print("✅ JWT auth working")
        else:
            print("❌ JWT auth failed")
            return False
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
        return False
    
    # Success!
    print_header("✨ Setup Complete!")
    
    print("📋 Next Steps:")
    print("   1. Review .env configuration")
    print("   2. Start the application:")
    print("      uvicorn src.api.main:app --reload")
    print("   3. Open http://localhost:8000/docs")
    print("   4. Try signup/login endpoints")
    print("\n📚 Documentation:")
    print("   - IMPLEMENTATION_SUMMARY.md - Overview of changes")
    print("   - ARCHITECTURE.md - System design")
    print("   - INTEGRATION_GUIDE.md - Usage examples")
    print("   - TEST_GUIDE.md - API endpoint tests")
    print("   - DEPLOYMENT_CHECKLIST.md - Deployment steps")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
