// ==========================================
// Nama File: halaman1.js
// Deskripsi: Pengatur interaksi bagi beranda
// Penulis:   Stan Fredheric, Miftah Rijallul Aziz, Fawwaz Areefa Yaqzhan
// NPM:        140810230046 ,     140810230053    ,     140810230055     
// Tanggal:   01-06-2026
// Catatan:
//   - Hanya beranda yang diatur interaksinya
//   - Halaman lain diatur oleh file js lain
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    
    console.log("Halaman Semantik Sunda Kuno Berhasil Dimuat.");

    const categorySelect = document.getElementById('category');
    const infoBox = document.getElementById('category-info-box');
    const descText = document.getElementById('category-desc');

    function updateCategoryInfo() {
        if (!categorySelect || !infoBox || !descText) return;
        const selectedVal = categorySelect.value;
        const comment = window.categoryComments ? window.categoryComments[selectedVal] : "";
        if (comment) {
            descText.textContent = comment;
            infoBox.style.display = 'flex';
            infoBox.classList.add('fade-in');
        } else {
            infoBox.style.display = 'none';
        }
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', updateCategoryInfo);
        updateCategoryInfo(); // run initially
    }

});