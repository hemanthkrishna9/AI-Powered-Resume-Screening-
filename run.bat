@echo off
REM Quick Run Script - Start the AI Resume Screener (Windows)

echo ===============================================
echo  Starting AI Resume Screener...
echo ===============================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [X] Virtual environment not found!
    echo Please run: setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check .env file
if not exist ".env" (
    echo [!] .env file not found. Using defaults...
    echo.
)

echo ===============================================
echo   AI-Powered Resume Screening System
echo   Opening in browser...
echo   URL: http://localhost:8501
echo ===============================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
streamlit run frontend\streamlit_app.py
