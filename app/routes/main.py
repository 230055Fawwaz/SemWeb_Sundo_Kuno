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

from flask import Blueprint, render_template, request, current_app
from rdflib import Literal

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_query = ""
    
    if request.method == 'POST':
        search_query = request.form.get('keyword', '').strip().lower()
        
        # Hanya jalankan kueri jika input pencarian tidak kosong untuk menghindari pengembalian semua baris
        if search_query:
            # Ambil graph RDF dari konfigurasi aplikasi
            g = current_app.config['RDF_GRAPH']
            
            # Query SPARQL yang aman menggunakan parameter binding ?search_query
            sparql_query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            
            SELECT ?id ?lempir ?aksara ?translit ?terjemahan WHERE {
                ?baris a :BarisNaskah ;
                       dcterms:identifier ?id ;
                       :lempirNaskah ?lempir ;
                       :hasAksara ?aksara ;
                       :hasTransliteration ?translit ;
                       :hasTranslation ?terjemahan .
                
                # Membungkus dengan STR() dan LCASE() agar pencarian kebal huruf besar/kecil
                FILTER(
                    CONTAINS(LCASE(STR(?translit)), ?search_query) || 
                    CONTAINS(LCASE(STR(?terjemahan)), ?search_query)
                )
            }
            ORDER BY ?id
            """
            
            # Eksekusi query ke rdflib dengan parameter binding initBindings untuk mencegah SPARQL Injection
            try:
                qres = g.query(sparql_query, initBindings={'search_query': Literal(search_query)})
                for row in qres:
                    results.append({
                        "id": str(row.id),
                        "lempir": str(row.lempir),
                        "aksara": str(row.aksara),
                        "translit": str(row.translit),
                        "terjemahan": str(row.terjemahan)
                    })
            except Exception as e:
                print(f"SPARQL Error: {e}")
 
    return render_template('index.html', results=results, query=search_query)
