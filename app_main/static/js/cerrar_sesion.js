function cerrarSesion() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/logout/');
    xhr.send();
}