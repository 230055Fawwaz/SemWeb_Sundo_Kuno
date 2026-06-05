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
from flask import Flask
from rdflib import Graph

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi secret key standar
    app.config['SECRET_KEY'] = 'semweb-sunda-kuno-secret'
    
    # Load dataset TTL ke dalam rdflib Graph saat aplikasi startup
    # Ini mengeliminasi kebutuhan Apache Jena Fuseki
    rdf_graph = Graph()
    ttl_path = os.path.join(app.root_path, 'dataset.ttl')
    
    if os.path.exists(ttl_path):
        rdf_graph.parse(ttl_path, format="turtle")
        print(f"--- [SUCCESS] Dataset RDF berhasil dimuat dari {ttl_path} ---")
    else:
        print(f"--- [WARNING] File {ttl_path} tidak ditemukan! ---")
        
    # Simpan graph ke dalam config agar bisa dipanggil di routes
    app.config['RDF_GRAPH'] = rdf_graph

    # Registrasi Blueprint Utama
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
