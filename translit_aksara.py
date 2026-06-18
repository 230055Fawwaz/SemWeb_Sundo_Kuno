# -*- coding: utf-8 -*-
"""
Transliterator Latin -> Aksara Sunda Baku (Unicode block U+1B80..U+1BBF).
Codepoint diverifikasi via unicodedata. Dipakai untuk membangkitkan bentuk
aksara per-kata pada lapisan leksikon (:aksaraKata).
"""
import unicodedata

# --- Konsonan dasar (ngalagena), inherent vowel /a/ ---
CONS = {
    'k': 'ᮊ', 'g': 'ᮌ', 'ng': 'ᮍ', 'c': 'ᮎ', 'j': 'ᮏ',
    'ny': 'ᮑ', 't': 'ᮒ', 'd': 'ᮓ', 'n': 'ᮔ', 'p': 'ᮕ',
    'b': 'ᮘ', 'm': 'ᮙ', 'y': 'ᮚ', 'r': 'ᮛ', 'l': 'ᮜ',
    'w': 'ᮝ', 's': 'ᮞ', 'h': 'ᮠ', 'f': 'ᮖ', 'v': 'ᮗ',
    'q': 'ᮋ', 'z': 'ᮐ', 'x': 'ᮟ', 'kh': 'ᮮ', 'sy': 'ᮯ',
}
# --- Aksara swara (vokal mandiri, di awal suku tanpa onset) ---
SWARA = {
    'a': 'ᮃ', 'i': 'ᮄ', 'u': 'ᮅ', 'é': 'ᮆ',
    'o': 'ᮇ', 'e': 'ᮈ', 'eu': 'ᮉ',
}
# --- Rarangkén vokal (menempel pada konsonan); 'a' = inherent (kosong) ---
RARANGKEN = {
    'a': '', 'i': 'ᮤ', 'u': 'ᮥ', 'é': 'ᮦ',
    'o': 'ᮧ', 'e': 'ᮨ', 'eu': 'ᮩ',
}
# --- Tanda sisipan konsonan medial ---
MEDIAL = {'r': 'ᮢ', 'y': 'ᮡ', 'l': 'ᮣ'}  # panyakra, pamingkal, panyiku
# --- Tanda akhir suku ---
PANYECEK = 'ᮀ'   # final -ng
PANGLAYAR = 'ᮁ'  # final -r
PANGWISAD = 'ᮂ'  # final -h
PAMAEH = '᮪'     # virama (mematikan vokal inheren)

VOWELS = set('aiueoé')
CONS_DIGRAPHS = ('ng', 'ny', 'kh', 'sy')


def segment(word):
    """Pecah kata menjadi list segmen: konsonan (mungkin digraf) atau vokal ('eu' digraf)."""
    segs = []
    i = 0
    w = word.lower()
    while i < len(w):
        ch = w[i]
        two = w[i:i+2]
        if two in CONS_DIGRAPHS:
            segs.append(('C', two)); i += 2
        elif two == 'eu':
            segs.append(('V', 'eu')); i += 2
        elif ch in VOWELS:
            segs.append(('V', ch)); i += 1
        elif ch in CONS or ch == "'":
            segs.append(('C', ch)); i += 1
        else:
            # karakter tak dikenal (mis. spasi) dilewati
            i += 1
    return segs


def final_sign(cons):
    if cons == 'ng':
        return PANYECEK
    if cons == 'r':
        return PANGLAYAR
    if cons == 'h':
        return PANGWISAD
    return CONS[cons] + PAMAEH


def to_aksara(word):
    segs = segment(word)
    out = []
    i = 0
    n = len(segs)
    prev_was_vowel = False
    while i < n:
        typ, val = segs[i]
        if typ == 'V':
            if i == 0 or prev_was_vowel:
                out.append(SWARA[val])      # vokal mandiri (awal / hiatus)
            # kalau didahului konsonan, vokal sudah ditangani saat konsonan
            prev_was_vowel = True
            i += 1
            continue
        # typ == 'C'
        # Cek gugus medial: C + (r/y/l) + V  -> base + medial + rarangkén
        if (i + 2 < n and segs[i+1][0] == 'C' and segs[i+1][1] in MEDIAL
                and segs[i+2][0] == 'V'):
            base = CONS[val]
            med = MEDIAL[segs[i+1][1]]
            vow = segs[i+2][1]
            out.append(base + med + RARANGKEN[vow])
            prev_was_vowel = True
            i += 3
            continue
        # C diikuti vokal -> suku onset biasa
        if i + 1 < n and segs[i+1][0] == 'V':
            out.append(CONS[val] + RARANGKEN[segs[i+1][1]])
            prev_was_vowel = True
            i += 2
            continue
        # C tanpa vokal sesudahnya -> koda (akhir suku)
        out.append(final_sign(val))
        prev_was_vowel = False
        i += 1
    return ''.join(out)


def names(s):
    return [unicodedata.name(c, '?') for c in s]


# Daftar 53 kata pada leksikon
WORDS = [
    'hayu', 'sadu', 'urang', 'ngaran', 'imah', 'buruan', 'ulah', 'mata', 'ceuli',
    'jalan', 'hurip', 'paéh', 'guru', 'janma', 'hayang', 'nyaho', 'leuweung',
    'talaga', 'kembang', 'bangbara', 'liman', 'cai', 'anak', 'éwé', 'hakan',
    'inum', 'héés', 'tuak', 'ratu', 'prebu', 'mantri', 'brahmana', 'tangan',
    'hyang', 'déwata', 'caang', 'sawah', 'huma', 'gajéndra', 'sagara', 'kreta',
    'kasukan', 'nguni', 'mangke', 'beuheula', 'ayeuna', 'dosa', 'munuh', 'drebya',
    'tunggak', 'watang', 'silih', 'curiga',
]

if __name__ == '__main__':
    import sys, json
    if '--map' in sys.argv:
        # keluarkan JSON {kata: aksara}
        result = {w: to_aksara(w) for w in WORDS}
        sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
    else:
        for w in WORDS:
            ak = to_aksara(w)
            short = [nm.replace('SUNDANESE ', '') for nm in names(ak)]
            print(f"{w:12} U+[{' '.join('%04X' % ord(c) for c in ak)}]")
            print(f"             {' + '.join(short)}")
