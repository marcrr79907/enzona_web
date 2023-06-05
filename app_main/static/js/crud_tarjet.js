
    const inputNumeroCard = document.getElementById('numero_card');
    inputNumeroCard.addEventListener('input', validarNumeroCard);
    
    function validarNumeroCard() {
      const regexSoloNumeros = /^[0-9]+$/;
      if (!regexSoloNumeros.test(inputNumeroCard.value)) {
        inputNumeroCard.value = inputNumeroCard.value.replace(/[^\d]/g, '');
      }
      if (inputNumeroCard.value.length > 16) {
        inputNumeroCard.value = inputNumeroCard.value.slice(0, 16);
      }
    }