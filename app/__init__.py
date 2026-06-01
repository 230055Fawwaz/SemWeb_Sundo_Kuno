# ==========================================
# Nama File: __init__.py
# Deskripsi: Inisialisasi Flask
# Penulis:   Stan Fredheric, Miftah Rijallul Aziz, Fawwaz Areefa Yaqzhan
# NPM:        140810230046 ,     140810230053    ,     140810230055     
# Tanggal:   01-06-2026
# Catatan:
#   - Rute blueprint di-impor untuk menghindari circular import
#   - Cache busting agar web browser menampilkan kode terbaru
# ==========================================

from flask import Flask

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# ====================================================
# PROSES REGISTRASI BLUEPRINT BARU DI SINI
# ====================================================
# Jalankan import di paling bawah untuk menghindari circular import

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.main import main_bp

# Daftarkan ke aplikasi utama Anda
app.register_blueprint(main_bp, url_prefix="/")
