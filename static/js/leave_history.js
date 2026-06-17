document.addEventListener("DOMContentLoaded", () => {

const rows =
document.querySelectorAll("table tr");

rows.forEach((row,index)=>{

    row.style.opacity = "0";
    row.style.transform =
    "translateY(20px)";

    setTimeout(()=>{

        row.style.transition =
        "all .5s ease";

        row.style.opacity = "1";
        row.style.transform =
        "translateY(0)";

    }, index * 100);

});


});
