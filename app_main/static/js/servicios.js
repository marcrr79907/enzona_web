function guardarID() {
    // Recoger los valores de los campos de entrada
    var nombre = document.getElementById("nombre").value;
    var tipo_servicio = document.getElementById("tipo-servicio").value;
    var nuevo_campo = document.getElementById("nuevo-campo").value;

    // Hacer algo con los valores, como enviarlos al servidor
    // ...

    // Cerrar el modal
    $('#exampleModal').modal('hide');
} 
function validarID() {
  var idCliente = document.getElementById('nuevo-campo').value;
  if (isNaN(idCliente) || idCliente.length !== 13) {
    alert('El ID cliente debe ser un número de 13 dígitos');
    return false;
  }
  return true;
}

function guardarID() {
  if (validarID()) {
    // Aquí puedes agregar el código para guardar el ID cliente
    // en tu base de datos o hacer cualquier otra acción necesaria
  }
}