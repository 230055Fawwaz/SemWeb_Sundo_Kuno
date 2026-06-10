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
from rdflib import Literal, URIRef
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_query = ""
    selected_category = ""
    synonyms_found = []
    
    g = current_app.config['RDF_GRAPH']
    
    # 1. LOAD DYNAMIC CATEGORIES FROM RDF SCHEMA (RDFS)
    categories_query = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?class ?label ?comment
    WHERE {
        ?class rdfs:subClassOf :BarisNaskah .
        OPTIONAL { ?class rdfs:label ?label . }
        OPTIONAL { ?class rdfs:comment ?comment . }
    }
    ORDER BY ?label
    """
    
    categories = []
    try:
        q_cats = g.query(categories_query)
        for row in q_cats:
            class_uri = str(row.get('class'))
            class_name = class_uri.split('#')[-1]
            categories.append({
                "uri": class_uri,
                "name": class_name,
                "label": str(row.get('label')) if row.get('label') else class_name,
                "comment": str(row.get('comment')) if row.get('comment') else ""
            })
    except Exception as e:
        print(f"Error fetching categories: {e}")
        
    if request.method == 'POST':
        search_query = request.form.get('keyword', '').strip().lower()
        selected_category = request.form.get('category', '').strip()
        
        if search_query or selected_category:
            # 2. SEMANTIC LOGIC: Find synonyms using property path (Symmetric & Transitive)
            if search_query:
                find_synonyms_query = """
                PREFIX : <http://contoh.org/ontology#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT DISTINCT ?synLabel
                WHERE {
                    ?concept rdfs:label ?inputLabel .
                    FILTER(LCASE(STR(?inputLabel)) = ?keyword)
                    ?concept (:hasSynonym|^:hasSynonym)+ ?synConcept .
                    ?synConcept rdfs:label ?synLabel .
                }
                """
                try:
                    q_syn = g.query(find_synonyms_query, initBindings={'keyword': Literal(search_query)})
                    for row in q_syn:
                        syn_label = str(row.get('synLabel')).strip()
                        if syn_label.lower() != search_query:
                            synonyms_found.append(syn_label)
                except Exception as e:
                    print(f"Error finding synonyms: {e}")
            
            # Combine keyword and its synonyms
            all_search_terms = [search_query] + [s.lower() for s in synonyms_found]
            
            # Prepare search category URI filter
            if selected_category:
                category_uri = f"http://contoh.org/ontology#{selected_category}"
            else:
                category_uri = "http://contoh.org/ontology#BarisNaskah"
                
            init_bindings = {'categoryFilter': URIRef(category_uri)}
            filter_clauses = []
            
            if search_query:
                # Regex pattern matching keyword OR synonyms
                pattern = "|".join(re.escape(term) for term in all_search_terms)
                init_bindings['pattern'] = Literal(pattern)
                filter_clauses.append("""
                FILTER(
                    REGEX(STR(?translit), ?pattern, "i") || 
                    REGEX(STR(?terjemahan), ?pattern, "i")
                )
                """)
                
            filter_str = "\n".join(filter_clauses)
            
            # 3. MAIN SPARQL SEARCH: Filters by class hierarchies and fetches OWL sequences
            sparql_query = f"""
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dcterms: <http://purl.org/dc/terms/>

            SELECT DISTINCT ?id ?lempir ?aksara ?translit ?terjemahan ?kategoriTeks ?lanjutKe ?sebelumKe
            WHERE {{
                ?baris :hasTransliteration ?translit ;
                    :hasTranslation ?terjemahan ;
                    dcterms:identifier ?id ;
                    :lempirNaskah ?lempir ;
                    :hasAksara ?aksara ;
                    rdf:type ?tipeKategori .
                
                # RDFS subClassOf reasoning (dynamic classification)
                ?tipeKategori rdfs:subClassOf* ?categoryFilter .
                
                # OWL transitive relation navigation
                OPTIONAL {{
                    ?baris :lanjutKeBaris ?nextBaris .
                    ?nextBaris dcterms:identifier ?lanjutKe .
                }}
                
                # OWL inverse relation navigation (inverse of lanjutKeBaris)
                OPTIONAL {{
                    ?prevBaris :lanjutKeBaris ?baris .
                    ?prevBaris dcterms:identifier ?sebelumKe .
                }}
                
                {filter_str}
                
                BIND(REPLACE(STR(?tipeKategori), "^.*#", "") AS ?kategoriTeks)
            }}
            ORDER BY ?id
            """
            
            try:
                qres = g.query(sparql_query, initBindings=init_bindings)
                for row in qres:
                    results.append({
                        "id": str(row.get('id')),
                        "lempir": str(row.get('lempir')),
                        "aksara": str(row.get('aksara')),
                        "translit": str(row.get('translit')),
                        "terjemahan": str(row.get('terjemahan')),
                        "kategori": str(row.get('kategoriTeks')) if row.get('kategoriTeks') else "BarisNaskah",
                        "lanjut_ke": str(row.get('lanjutKe')) if row.get('lanjutKe') else "-",
                        "sebelum_ke": str(row.get('sebelumKe')) if row.get('sebelumKe') else "-"
                    })
            except Exception as e:
                print(f"SPARQL Error: {e}")
                
    return render_template(
        'index.html', 
        results=results, 
        query=search_query, 
        synonyms=synonyms_found,
        categories=categories,
        selected_category=selected_category
    )
