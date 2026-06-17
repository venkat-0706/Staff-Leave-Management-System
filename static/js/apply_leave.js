document.addEventListener("DOMContentLoaded", () => {

const startDate =
document.querySelector(
    'input[name="start_date"]'
);

const endDate =
document.querySelector(
    'input[name="end_date"]'
);

if(startDate && endDate){

    startDate.addEventListener("change", () => {

        endDate.min =
        startDate.value;

    });

}


});
