// ==========================================
// Nama File: scripts.js
// Deskripsi: Pengatur interaksi user bagi base.html 
// Penulis:   Stan Fredheric, Miftah Rijallul Aziz, Fawwaz Areefa Yaqzhan
// NPM:        140810230046 ,     140810230053    ,     140810230055     
// Tanggal:   01-06-2026
// Catatan:
// - Hanya berisi aturan interaksi bagi base.html
// - Aturan interaksi halaman lain ada di file tersendiri
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    
    /* =========================================
       Logika Collapsible Menu (Sidebar)
    ========================================= */
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

});
