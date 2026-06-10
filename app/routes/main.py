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
        
        if search_query:
            g = current_app.config['RDF_GRAPH']
            
            sparql_query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dcterms: <http://purl.org/dc/terms/>

            SELECT DISTINCT ?id ?lempir ?aksara ?translit ?terjemahan ?kategoriTeks ?lanjutKe 
            WHERE {
                
                # 1. LOGIKA SEMANTIK (Menggunakan OPTIONAL agar tidak mogok jika kata tidak ada di kamus)
                # Kita cari tahu apakah kata input memiliki sinonim
                OPTIONAL {
                    ?kataKonsep rdfs:label ?search_query .
                    ?kataKonsep :hasSynonym ?sinonim .
                    ?sinonim rdfs:label ?teksSinonim .
                }
                
                # Jika ketemu sinonimnya, pakai ?teksSinonim. Jika tidak, gunakan ?search_query asal dari user.
                BIND(COALESCE(?teksSinonim, ?search_query) AS ?teksCari)
                
                # 2. LOGIKA PENCARIAN NASKAH
                ?baris :hasTransliteration ?translit ;
                    :hasTranslation ?terjemahan ;
                    dcterms:identifier ?id ;
                    :lempirNaskah ?lempir ;
                    :hasAksara ?aksara ;
                    rdf:type ?tipeKategori .
                
                # Mengambil kategori baris teks dari RDFS
                ?tipeKategori rdfs:subClassOf* :BarisNaskah .
                
                # Mengambil kelanjutan baris dari OWL
                OPTIONAL {
                    ?baris :lanjutKeBaris ?nextBaris .
                    ?nextBaris dcterms:identifier ?lanjutKe .
                }
                
                # Pencarian parsial (LCASE memastikan pencarian aman dari huruf kapital)
                FILTER(
                    CONTAINS(LCASE(STR(?translit)), LCASE(STR(?teksCari))) || 
                    CONTAINS(LCASE(STR(?terjemahan)), LCASE(STR(?teksCari)))
                )
                
                BIND(REPLACE(STR(?tipeKategori), "^.*#", "") AS ?kategoriTeks)
            }
            ORDER BY ?id
            """
            
            try:
                qres = g.query(sparql_query, initBindings={'search_query': Literal(search_query)})
                for row in qres:
                    results.append({
                        "id": str(row.id),
                        "lempir": str(row.lempir),
                        "aksara": str(row.aksara),
                        "translit": str(row.translit),
                        "terjemahan": str(row.terjemahan),
                        "kategori": str(row.kategoriTeks) if row.kategoriTeks else "BarisNaskah", # Data RDFS
                        "lanjut_ke": str(row.lanjutKe) if row.lanjutKe else "-" # Data OWL
                    })
            except Exception as e:
                print(f"SPARQL Error: {e}")
 
    return render_template('index.html', results=results, query=search_query)
