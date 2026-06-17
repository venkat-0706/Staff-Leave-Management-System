document.addEventListener("DOMContentLoaded", () => {

    console.log("Manage Staff Loaded");

    const searchInput =
    document.querySelector('.search-box input');

    if(searchInput){

        searchInput.addEventListener('focus', () => {
            searchInput.style.boxShadow =
            '0 0 0 4px rgba(29,114,216,.15)';
        });

        searchInput.addEventListener('blur', () => {
            searchInput.style.boxShadow = 'none';
        });

    }

});