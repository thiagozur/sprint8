function mostrarToggle() {
    const contrasena = document.getElementById("pass");
    if (contrasena.type === "password") {
        contrasena.type = "text";
    } else {
        contrasena.type = "password";
    }
}