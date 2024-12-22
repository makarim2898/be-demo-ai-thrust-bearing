#!/bin/bash

# Tutup Google Chrome
pkill chrome

# Hentikan proses yang berjalan di port 5000
fuser -k 5000/tcp

# Masuk ke direktori program
cd /home/kaizen-ai/Desktop/thrust_bearing_app/python-backend/

# Source conda.sh untuk mengaktifkan conda
source /home/kaizen-ai/miniconda3/etc/profile.d/conda.sh

# Aktifkan environment Conda 'AI'
conda activate AI

# Jalankan Flask app di background
python app.py &

# Simpan PID dari proses Flask
FLASK_PID=$!

# Tunggu hingga Flask berjalan dengan polling port 5000
echo "Menunggu Flask berjalan di port 5000..."
while ! nc -z localhost 5000; do   
  sleep 1 # Tunggu 1 detik sebelum mencoba lagi
done

echo "Flask sudah berjalan di port 5000!"

echo "tunggu 10 detik sebelum membuka browser"

sleep 10
google-chrome --start-fullscreen /home/kaizen-ai/Desktop/thrust_bearing_app/frontend/html-old/Home-page/Homepage.html
# Tunggu Flask selesai berjalan
wait $FLASK_PID

# Tunggu input dari user sebelum menutup terminal
echo "Tekan Enter untuk keluar..."
read

