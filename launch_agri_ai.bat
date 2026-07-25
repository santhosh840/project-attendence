@echo off
TITLE AgriAI - 24/7 Virtual Agriculture Extension Officer Server
COLOR 0A
CD /D "%~dp0"

echo ====================================================================
echo             AgriAI: AI-Based Personal Agriculture Officer
echo               24/7 Virtual Extension Officer Server
echo ====================================================================
echo.

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH! Please install Python 3.9+.
    pause
    exit /b 1
)

rem Open Browser automatically after 2 seconds delay
start "" "http://127.0.0.1:5000"

rem 24/7 Auto-Restart Server Loop
:SERVER_LOOP
echo [%date% %time%] Starting AgriAI Server on http://127.0.0.1:5000 ...
python app.py >> agri_ai_server.log 2>&1

echo [%date% %time%] WARNING: AgriAI Server stopped unexpected. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto SERVER_LOOP
