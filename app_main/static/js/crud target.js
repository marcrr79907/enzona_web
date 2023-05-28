// Obtener el input del campo de "Numero"
var inputNumero = document.querySelector('#numero-input');

// Agregar un listener para el evento "keydown"
inputNumero.addEventListener('keydown', function(event) {
  // Obtener el valor actual del input
  var numero = inputNumero.value;
  
  // Remover cualquier carácter que no sea un dígito
  numero = numero.replace(/\D/g,'');
  
  // Verificar si el número tiene 16 dígitos y es un número válido
  if (numero.length >= 16 || isNaN(event.key)) {
    // Si tiene 16 dígitos o no es un número válido, prevenir el evento por defecto
    event.preventDefault();
  }
});


