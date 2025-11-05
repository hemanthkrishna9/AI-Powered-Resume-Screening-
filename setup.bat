@echo off
REM Quick Setup Script for Local Testing (Windows)

echo ===============================================
echo  AI Resume Screener - Quick Setup (Windows)
echo ===============================================
echo.

REM Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [X] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo [*] Installing dependencies (2-3 minutes)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Download spaCy model
echo [*] Downloading spaCy model...
python -m spacy download en_core_web_sm
echo [OK] spaCy model downloaded
echo.

REM Create directories
echo [*] Creating directories...
if not exist "data\resumes" mkdir "data\resumes"
if not exist "data\vector_db" mkdir "data\vector_db"
if not exist "logs" mkdir "logs"
echo [OK] Directories created
echo.

REM Create .env file
if not exist ".env" (
    echo [*] Creating .env file...
    (
        echo # Azure OpenAI Configuration
        echo AZURE_OPENAI_ENDPOINT=https://itcmentor.openai.azure.com/
        echo AZURE_OPENAI_API_KEY=4FuAkN0MCCjWTv2zGuwvOw622IjmsnwWbh0SCo7U2xuNhP3rY3AoJQQJ99BlACYeBjFXj3w3AAABACOGrcAG
        echo AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
        echo AZURE_GPT_DEPLOYMENT=gpt-4o-mini
        echo AZURE_OPENAI_API_VERSION=2024-02-15-preview
        echo AZURE_EMBEDDING_DIMENSION=3072
        echo.
        echo # App Configuration
        echo AI_PROVIDER=azure
        echo AZURE_OPENAI_ENABLED=True
        echo USE_SAMPLE_DATA=True
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] .env file created
) else (
    echo [OK] .env file already exists
)
echo.

echo ===============================================
echo  Setup Complete!
echo ===============================================
echo.
echo To run the app:
echo   run.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   streamlit run frontend\streamlit_app.py
echo.
pause
