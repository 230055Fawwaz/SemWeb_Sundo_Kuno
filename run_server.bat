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

:: 1. Cek apakah sudah ada instance Flask yang berjalan (hindari duplikasi)
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if not errorlevel 1 (
    echo [PERINGATAN] Python sudah berjalan. Pastikan tidak ada Flask yang aktif sebelumnya.
    echo Lanjutkan tetap buka browser saja? [Y/N]
    set /p konfirmasi=Pilihan: 
    if /i "%konfirmasi%"=="Y" goto buka_browser
    goto akhir
)

:: 2. Validasi virtual environment
if not exist .semwebenv\Scripts\activate (
    echo [ERROR] Virtual Environment .semwebenv tidak ditemukan!
    pause
    exit /b 1
)

:: 3. Aktifkan .semwebenv
call .semwebenv\Scripts\activate

:: 4. Jalankan Flask di window terpisah yang BISA DITUTUP MANUAL
::    /MIN  = minimized agar tidak mengganggu
::    Menutup jendela CMD itu = mematikan Flask sepenuhnya
echo Menyalakan server Flask...
start "Flask Server - Tutup jendela ini untuk mematikan server" /MIN cmd /k "python run.py"

:: 5. Tunggu Flask siap dengan polling (lebih andal dari timeout tetap)
echo Menunggu Flask siap...
:tunggu
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:5000 >nul 2>&1
if errorlevel 1 goto tunggu

:: 6. Buka browser
:buka_browser
echo Membuka browser...
start http://127.0.0.1:5000

:akhir
exit
