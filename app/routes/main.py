# ==========================================
# Nama File: main.py
# Deskripsi: Rute khusus bagian dasar
# Penulis:   Stan Fredheric, Miftah Rijallul Aziz, Fawwaz Areefa Yaqzhan
# NPM:        140810230046 ,     140810230053    ,     140810230055     
# Tanggal:   01-06-2026
# Catatan:
#   - File ini hanya berisi rute dasar seperti menampilkan halaman
#   - Rute lain ada di file tersendiri
# ==========================================

from flask import render_template, Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/beranda")
def beranda():
    return render_template(
        "beranda.html",
    )
