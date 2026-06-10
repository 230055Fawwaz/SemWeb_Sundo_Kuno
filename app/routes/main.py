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
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_query = ""
    synonyms_found = []
    
    if request.method == 'POST':
        search_query = request.form.get('keyword', '').strip().lower()
        
        if search_query:
            g = current_app.config['RDF_GRAPH']
            
            # 1. LOGIKA SEMANTIK (Mencari konsep dan sinonimnya di graf RDF)
            find_synonyms_query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?synLabel
            WHERE {
                ?concept rdfs:label ?inputLabel .
                FILTER(LCASE(STR(?inputLabel)) = ?keyword)
                
                {
                    ?concept :hasSynonym ?synConcept .
                } UNION {
                    ?synConcept :hasSynonym ?concept .
                }
                
                ?synConcept rdfs:label ?synLabel .
            }
            """
            
            try:
                q_syn = g.query(find_synonyms_query, initBindings={'keyword': Literal(search_query)})
                for row in q_syn:
                    syn_label = str(row.synLabel).strip()
                    if syn_label.lower() != search_query:
                        synonyms_found.append(syn_label)
            except Exception as e:
                print(f"Error finding synonyms: {e}")
                
            # Gabungkan keyword asli dengan semua sinonim untuk pencarian utama
            all_search_terms = [search_query] + [s.lower() for s in synonyms_found]
            # Melakukan escaping regex untuk keamanan dan menggabungkannya dengan operator OR |
            pattern = "|".join(re.escape(term) for term in all_search_terms)
            
            # 2. LOGIKA PENCARIAN NASKAH UTAMA
            sparql_query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dcterms: <http://purl.org/dc/terms/>

            SELECT DISTINCT ?id ?lempir ?aksara ?translit ?terjemahan ?kategoriTeks ?lanjutKe 
            WHERE {
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
                
                # Pencarian parsial case-insensitive menggunakan regex OR
                FILTER(
                    REGEX(STR(?translit), ?pattern, "i") || 
                    REGEX(STR(?terjemahan), ?pattern, "i")
                )
                
                BIND(REPLACE(STR(?tipeKategori), "^.*#", "") AS ?kategoriTeks)
            }
            ORDER BY ?id
            """
            
            try:
                qres = g.query(sparql_query, initBindings={'pattern': Literal(pattern)})
                for row in qres:
                    results.append({
                        "id": str(row.id),
                        "lempir": str(row.lempir),
                        "aksara": str(row.aksara),
                        "translit": str(row.translit),
                        "terjemahan": str(row.terjemahan),
                        "kategori": str(row.kategoriTeks) if row.kategoriTeks else "BarisNaskah", # Data RDFS
                        "lanjut_ke": str(row.lanjut_ke) if (hasattr(row, 'lanjut_ke') and row.lanjut_ke) or (hasattr(row, 'lanjutKe') and row.lanjutKe) else "-" # Data OWL
                    })
            except Exception as e:
                print(f"SPARQL Error: {e}")
 
    return render_template('index.html', results=results, query=search_query, synonyms=synonyms_found)
