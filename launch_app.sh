#!/usr/bin/env bash

PORT=5000
APP_URL="http://localhost:${PORT}"

echo "========================================================"
echo "  AI-Powered Student Attendance System Launcher"
echo "========================================================"

# Check if port 5000 is listening
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "[INFO] Server is already running on port ${PORT}"
else
    echo "[INFO] Starting Flask backend server..."
    python3 app.py &
    sleep 3
fi

echo "[INFO] Opening ${APP_URL} in default browser..."
if command -v open > /dev/null; then
    open "${APP_URL}" # macOS
elif command -v xdg-open > /dev/null; then
    xdg-open "${APP_URL}" # Linux
else
    echo "Please open ${APP_URL} in your browser."
fi
