AOS.init({
    duration:1200,
    once:false
});

function togglePassword(id, icon){

    const input =
    document.getElementById(id);

    if(input.type==="password"){
        input.type="text";
        icon.classList.replace("fa-eye","fa-eye-slash");
    }
    else{
        input.type="password";
        icon.classList.replace("fa-eye-slash","fa-eye");
    }
}

function checkStrength(){

    const password =
    document.getElementById("password").value;

    const bar =
    document.getElementById("strengthBar");

    let strength = 0;

    if(password.length > 5) strength += 25;
    if(/[A-Z]/.test(password)) strength += 25;
    if(/[0-9]/.test(password)) strength += 25;
    if(/[^A-Za-z0-9]/.test(password)) strength += 25;

    bar.style.width = strength + "%";

    if(strength <= 25){
        bar.style.background = "#ff3b30";
    }
    else if(strength <= 50){
        bar.style.background = "#ff9500";
    }
    else if(strength <= 75){
        bar.style.background = "#34c759";
    }
    else{
        bar.style.background = "#0071e3";
    }
}