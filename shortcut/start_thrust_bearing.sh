#!/bin/bash

# ==========================================
# THRUST BEARING AI - START
# ==========================================

BACKEND_DIR="/home/kaizen/Desktop/demo_ai/be-demo-ai-thrust-bearing"
FRONTEND_FILE="/home/kaizen/Desktop/demo_ai/fe-thrust-bearing-AI/Home-page/Homepage.html"
PYTHON_ENV="/home/kaizen/Desktop/python_environtment/AI_ENV/bin/activate"

BACKEND_URL="http://127.0.0.1:5000"
PID_FILE="/tmp/thrust_bearing_ai.pid"

STOP_SCRIPT="/home/kaizen/Desktop/stop_thrust_bearing.sh"

echo "=========================================="
echo "       THRUST BEARING AI - START"
echo "=========================================="

# ==========================================
# 1. FORCE STOP PREVIOUS INSTANCE
# ==========================================

echo
echo "[1/4] Cleaning previous backend..."

if [ -x "$STOP_SCRIPT" ]; then
    "$STOP_SCRIPT"
else
    echo "WARNING: STOP script tidak ditemukan:"
    echo "$STOP_SCRIPT"
fi

echo
echo "Previous backend cleanup finished."

# ==========================================
# 2. CHECK PORT 5000
# ==========================================

echo
echo "[2/4] Checking port 5000..."

if lsof -i :5000 >/dev/null 2>&1; then

    echo
    echo "ERROR: Port 5000 masih digunakan!"
    echo
    lsof -i :5000

    echo
    echo "START dibatalkan."
    echo "Terminal akan tetap terbuka."

    while true; do
        sleep 60
    done
fi

echo "Port 5000 is available."

# ==========================================
# 3. START BACKEND
# ==========================================

cd "$BACKEND_DIR" || {
    echo "ERROR: Backend directory tidak ditemukan."
    exit 1
}

echo
echo "Activating AI_ENV..."

source "$PYTHON_ENV" || {
    echo "ERROR: AI_ENV tidak ditemukan."
    exit 1
}

echo "Python:"
which python

echo
echo "Starting Flask backend..."
echo

python app.py &

BACKEND_PID=$!

echo "$BACKEND_PID" > "$PID_FILE"

echo
echo "Backend PID: $BACKEND_PID"
echo "Waiting for backend..."

# ==========================================
# 4. WAIT BACKEND READY
# ==========================================

MAX_RETRY=60
RETRY=0

while true; do

    # Check apakah process masih hidup
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then

        echo
        echo "ERROR: Backend process mati sebelum READY."

        rm -f "$PID_FILE"

        echo
        echo "Terminal akan tetap terbuka."

        while true; do
            sleep 60
        done
    fi

    # Check HTTP
    if curl -s --connect-timeout 1 "$BACKEND_URL" >/dev/null 2>&1; then
        break
    fi

    RETRY=$((RETRY + 1))

    if [ "$RETRY" -ge "$MAX_RETRY" ]; then

        echo
        echo "ERROR: Backend tidak READY setelah 60 detik."

        kill "$BACKEND_PID" 2>/dev/null
        rm -f "$PID_FILE"

        echo
        echo "Terminal akan tetap terbuka."

        while true; do
            sleep 60
        done
    fi

    echo -n "."
    sleep 1

done

# ==========================================
# BACKEND READY
# ==========================================

echo
echo
echo "=========================================="
echo "       BACKEND READY!"
echo "=========================================="

# ==========================================
# OPEN FIREFOX
# ==========================================

echo
echo "Opening Firefox..."

firefox "$FRONTEND_FILE" >/dev/null 2>&1 &

echo
echo "=========================================="
echo "       SYSTEM RUNNING"
echo "=========================================="
echo
echo "Backend : $BACKEND_URL"
echo "Frontend: $FRONTEND_FILE"
echo "PID     : $BACKEND_PID"
echo
echo "=========================================="
echo
echo "BACKEND TERMINAL IS ACTIVE."
echo "DO NOT CLOSE THIS TERMINAL."
echo
echo "Use STOP shortcut to shutdown."
echo

# ==========================================
# KEEP TERMINAL ALIVE
# ==========================================

wait "$BACKEND_PID"

# ==========================================
# BACKEND EXITED
# ==========================================

rm -f "$PID_FILE"

echo
echo "=========================================="
echo "       BACKEND STOPPED"
echo "=========================================="

echo
echo "Terminal akan tetap terbuka."

while true; do
    sleep 60
done
