AOS.init({
    duration:1000,
    once:true
});

function togglePassword(){

    const password =
    document.getElementById("password");

    const icon =
    document.querySelector(".input-box i");

    if(password.type === "password"){
        password.type = "text";
        icon.classList.replace("fa-eye","fa-eye-slash");
    }else{
        password.type = "password";
        icon.classList.replace("fa-eye-slash","fa-eye");
    }
}