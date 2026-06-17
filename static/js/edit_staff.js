// Ready for future enhancements


document.addEventListener("DOMContentLoaded", () => {

    const passwordInput =
    document.getElementById("password");

    if(passwordInput){

        const toggleBtn =
        document.createElement("span");

        toggleBtn.innerHTML = "👁";
        toggleBtn.style.cursor = "pointer";
        toggleBtn.style.marginLeft = "10px";

        passwordInput.parentNode.appendChild(toggleBtn);

        toggleBtn.addEventListener("click", () => {

            if(passwordInput.type === "password"){
                passwordInput.type = "text";
            }else{
                passwordInput.type = "password";
            }

        });

    }

});