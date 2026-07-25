@echo off
title AI Student Attendance System Launcher
color 0A

echo ========================================================
echo   AI Facial Recognition Attendance Kiosk Launcher
echo ========================================================
echo.

set PORT=5005

:: Get Local Network IP Address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set LOCAL_IP=%%a
)
if defined LOCAL_IP set LOCAL_IP=%LOCAL_IP:~1%

set APP_LOCAL_URL=http://localhost:%PORT%
set APP_NETWORK_URL=http://%LOCAL_IP%:%PORT%

echo [INFO] Access URLs:
echo        - Local PC URL:      %APP_LOCAL_URL%
echo        - Network (Wi-Fi):   %APP_NETWORK_URL%
echo.

:: Check if server is already running on port 5005
netstat -o -n -a | findstr /R /C:":%PORT% " >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [INFO] Attendance server is already running on port %PORT%!
    echo [INFO] Opening %APP_LOCAL_URL% in default browser...
    start "" "%APP_LOCAL_URL%"
    exit /b 0
)

echo [INFO] Starting Student Attendance Flask Server on port %PORT% in background...
start /B pythonw app.py > nul 2>&1

echo [INFO] Waiting for server initialization...
timeout /t 3 /nobreak > nul

echo [INFO] Opening %APP_LOCAL_URL% in default web browser...
start "" "%APP_LOCAL_URL%"

echo.
echo Kiosk system is running live 24/7!
echo You can access it on mobile/tablet via: %APP_NETWORK_URL%
echo ========================================================
