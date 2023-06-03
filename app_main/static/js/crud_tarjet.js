


    

    function guardarTarjeta() {
      // Recoger los valores de los campos de entrada
      var numero = document.getElementById('numero').value;
        var pin = document.getElementById('fecha').value;
  
      // Hacer algo con los valores, como enviarlos al servidor
      // ...
  
      // Cerrar el modal
      $('#exampleModal').modal('hide');
  } 
  function validarTarjeta() {
    var tarjetanumber = document.getElementById('numero').value;
    if (isNaN(tarjetanumber) || tarjetanumber.length !== 16) {
      alert(' La Tarjeta no existe ');
      return false;
    }
    return true;
  }
  function validarPIN() {
    var pinnumber = document.getElementById('numero').value;
    if (isNaN(pinnumber) || pinnumber.length !== 4) {
      alert(' Su PIN es Incorrecto ');
      return false;
    }
    return true;
  }
  
  function guardarTarjeta() {
    if (validarTarjeta(),validarPIN()) {
      // Aquí puedes agregar el código para guardar el ID cliente
      // en tu base de datos o hacer cualquier otra acción necesaria
    }
  }


