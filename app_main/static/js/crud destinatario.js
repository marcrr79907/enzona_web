//imprimiendo datos en tabla y validaciones
const tabla = document.querySelector("table tbody");
const botonGuardarContacto = document.getElementById("Guardar");
const nombreInput = document.getElementById("nombre");
const numeroInput = document.getElementById("numero");
const acciones = document.getElementById("botones");
let contadorFilas = 2;

botonGuardarContacto.addEventListener("click", () => {
  const nombre = nombreInput.value.trim();
  const numero = numeroInput.value.trim();
  
  if (nombre === "" || numero === "") {
    alert("Por favor, completa todos los campos.");
    return;
  }
  
  if (!/^[A-Z][a-z]*$/.test(nombre)) {
    alert("El nombre debe empezar con mayúscula.");
    return;
  }
  
  if (!/^\d{16}$/.test(numero)) {
    alert("El número de tarjeta debe tener 16 dígitos.");
    return;
  }
  
  const nuevaFila = document.createElement("tr");
  nuevaFila.innerHTML = `
    <td class="centrar">${contadorFilas}</td>
    <td class="centrar">${nombre}</td>
    <td class="centrar">${numero}</td>
    <td class="centrar">${acciones}</td>
  `;
  
  tabla.appendChild(nuevaFila);
  
  contadorFilas++;
  
  nombreInput.value = "";
  numeroInput.value = "";
});