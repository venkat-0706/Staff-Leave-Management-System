document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
    document.getElementById("searchInput");

    searchInput.addEventListener("keyup", function(){

        let filter =
        this.value.toLowerCase();

        let rows =
        document.querySelectorAll(
            "#reportTable tbody tr"
        );

        rows.forEach((row)=>{

            let name =
            row.cells[0]?.textContent
            .toLowerCase();

            let email =
            row.cells[1]?.textContent
            .toLowerCase();

            if(
                name?.includes(filter) ||
                email?.includes(filter)
            ){
                row.style.display = "";
            }
            else{
                row.style.display = "none";
            }

        });

    });

});