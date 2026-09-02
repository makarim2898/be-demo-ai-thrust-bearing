#!/bin/bash

# ==========================================
# THRUST BEARING AI - STOP SCRIPT
# ==========================================

PID_FILE="/tmp/thrust_bearing_ai.pid"

echo "=========================================="
echo "       STOP THRUST BEARING AI"
echo "=========================================="

if [ ! -f "$PID_FILE" ]; then
    echo "Backend PID file tidak ditemukan."
    echo "Mungkin backend memang sedang tidak berjalan."

    echo
    echo "Terminal akan ditutup dalam 5 detik..."
    sleep 5
    exit 0
fi

BACKEND_PID=$(cat "$PID_FILE")

echo "Backend PID: $BACKEND_PID"

if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "Backend sudah tidak berjalan."

    rm -f "$PID_FILE"

    echo
    echo "Terminal akan ditutup dalam 5 detik..."
    sleep 5
    exit 0
fi

echo "Stopping backend..."

kill "$BACKEND_PID"

for i in {1..10}; do

    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "Backend stopped."
        rm -f "$PID_FILE"
        break
    fi

    sleep 1
done

# Kalau masih hidup, force kill
if kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "Backend masih berjalan."
    echo "Force stopping..."

    kill -9 "$BACKEND_PID" 2>/dev/null

    rm -f "$PID_FILE"
fi

echo
echo "=========================================="
echo "       THRUST BEARING AI STOPPED"
echo "=========================================="

echo
echo "Terminal akan ditutup dalam 5 detik..."

sleep 5

exit 0
