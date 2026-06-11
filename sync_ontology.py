import os
import sys
from rdflib import Graph

def sync():
    # Definisikan path file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ttl_path = os.path.join(current_dir, 'app', 'dataset.ttl')
    owl_path = os.path.join(current_dir, 'ontology.owl')

    if not os.path.exists(ttl_path):
        print(f"[ERROR] File dataset.ttl tidak ditemukan di: {ttl_path}")
        sys.exit(1)

    print(f"Membaca dataset RDF dari: {ttl_path} ...")
    g = Graph()
    try:
        g.parse(ttl_path, format="turtle")
        print(f"[SUCCESS] Berhasil memuat {len(g)} triples dari dataset.")
    except Exception as e:
        print(f"[ERROR] Gagal mem-parsing file Turtle: {e}")
        sys.exit(1)

    print(f"Menyimpan ontologi ke format RDF/XML (Protege-compatible) di: {owl_path} ...")
    try:
        g.serialize(destination=owl_path, format="pretty-xml")
        print(f"[SUCCESS] File ontologi OWL berhasil diperbarui: {owl_path}")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file OWL: {e}")
        sys.exit(1)

if __name__ == '__main__':
    sync()
