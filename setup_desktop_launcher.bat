@echo off
title Setting up AI Attendance System Desktop Shortcut
color 0A

echo ========================================================
echo   Setting up Desktop Launcher for AI Attendance System
echo ========================================================
echo.

set TARGET_DIR=%~dp0
set VBS_SCRIPT=%TARGET_DIR%launch_silent.vbs
set DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\AI Student Attendance System.lnk

:: Create launch_silent.vbs
(
echo Set WshShell = CreateObject^("WScript.Shell"^^)
echo Set fso = CreateObject^("Scripting.FileSystemObject"^^)
echo strPath = fso.GetAbsolutePathName^("."^)
echo WshShell.Run "pythonw app.py", 0, False
echo WScript.Sleep 2000
echo WshShell.Run "http://localhost:5000", 1, False
) > "%VBS_SCRIPT%"

:: Create Desktop Shortcut using PowerShell
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP_SHORTCUT%'); $s.TargetPath='%VBS_SCRIPT%'; $s.WorkingDirectory='%TARGET_DIR%'; $s.IconLocation='C:\Windows\System32\shell32.dll,220'; $s.Save()"

echo [SUCCESS] Desktop Shortcut Created Successfully!
echo [LOCATION] %DESKTOP_SHORTCUT%
echo.
echo You can now double-click "AI Student Attendance System" on your Desktop anytime.
echo It will run 24/7 in the background even if Antigravity or CMD is closed!
echo ========================================================
pause
