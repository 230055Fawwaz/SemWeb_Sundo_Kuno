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

import os
import traceback  # 1. Tambahkan import ini
from flask import Flask
from rdflib import Graph

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'semweb-sunda-kuno-secret'
    
    rdf_graph = Graph()
    ttl_path = os.path.join(app.root_path, 'dataset.ttl')
    
    if os.path.exists(ttl_path):
        try:
            # 2. Bungkus proses parse dengan try-except untuk melacak error
            rdf_graph.parse(ttl_path, format="turtle")
            print(f"--- [SUCCESS] Dataset RDF berhasil dimuat dari {ttl_path} ---")
        except Exception as e:
            # 3. Jika gagal, cetak detail error yang selama ini disembunyikan
            print("\n" + "!"*50)
            print("--- [ERROR] GAGAL MEMUAT DATASET TTL ---")
            traceback.print_exc() 
            print("!"*50 + "\n")
            # Kamu bisa memilih untuk membiarkan aplikasi tetap jalan atau berhenti
            # raise e  # Uncomment baris ini jika ingin aplikasi berhenti total saat error
    else:
        print(f"--- [WARNING] File {ttl_path} tidak ditemukan! ---")
        
    app.config['RDF_GRAPH'] = rdf_graph

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
