REM ==========================================
REM Nama File: run_server.bat
REM Deskripsi: Otomatisasi menyalakan server flask
REM Penulis:   Stan Fredheric, Miftah Rijallul Aziz, Fawwaz Areefa Yaqzhan
REM NPM:        140810230046 ,     140810230053    ,     140810230055     
REM Tanggal:   01-06-2026
REM Catatan:
REM ==========================================

@echo off
cd /d %~dp0

:: 1. Validasi cek apakah virtual environment ada
if not exist semwebenv\Scripts\activate (
    echo [ERROR] Virtual Environment semwebenv tidak ditemukan!
    goto error
)

:: 2. Aktifkan venv
call semwebenv\Scripts\activate

:: 3. Jalankan server Flask di latar belakang (background) menggunakan 'start'
:: Ini membuat Flask menyala, dan CMD utama bisa lanjut mengeksekusi perintah berikutnya
echo Menyalakan server Flask...
start "" python run.py

:: 4. Beri jeda 3 detik agar Flask benar-benar siap
timeout /t 3 /nobreak >nul

:: 5. Buka browser setelah server dipastikan naik
echo Membuka browser...
start http://127.0.0.1:5000
exit

:error
pause
