@echo off
REM Windows Batch Script to Setup and Run RAG Chatbot
REM This script sets up both backend and frontend

echo.
echo ========================================
echo   RAG Chatbot - Setup & Launch Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if we're in the project root
if not exist "main.py" (
    echo Error: Please run this script from the project root directory (d:\work\RAG)
    pause
    exit /b 1
)

REM Backend Setup
echo.
echo [1/5] Setting up backend...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
echo Installing backend dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install backend dependencies
    pause
    exit /b 1
)

REM Initialize Database
echo [2/5] Initializing database...
python bootstrap_db.py
if errorlevel 1 (
    echo Error: Failed to initialize database
    echo Make sure PostgreSQL is running and DATABASE_URL is set
    pause
    exit /b 1
)

REM Frontend Setup
echo [3/5] Setting up frontend...
cd frontend
if not exist "venv" (
    echo Creating frontend virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo Installing frontend dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install frontend dependencies
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Start Backend Server (in terminal 1):
echo    cd d:\work\RAG
echo    .venv\Scripts\activate.bat
echo    python -m uvicorn src.api.main:app --reload
echo    (Backend will run on http://localhost:8000)
echo.
echo 2. Start Frontend App (in terminal 2):
echo    cd d:\work\RAG\frontend
echo    venv\Scripts\activate.bat
echo    streamlit run app.py
echo    (Frontend will open on http://localhost:8501)
echo.
echo 3. Open http://localhost:8501 in your browser
echo.
echo 4. Sign up for an account
echo.
echo 5. Upload PDF documents
echo.
echo 6. Start asking questions!
echo.
echo ========================================
echo.

pause
