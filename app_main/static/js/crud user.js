function validateUsername() {
    const usernameInput = document.getElementById("fullName");
    const usernameValidation = document.getElementById("usernameValidation");
    const usernameRegex = /^[a-zA-Z0-9]{1,8}$/;
    if (!usernameRegex.test(usernameInput.value)) {
        usernameValidation.style.display = "block";
    } else {
        usernameValidation.style.display = "none";
    }
}

function validatePhone() {
    const phoneInput = document.getElementById("phone");
    const phoneValidation = document.getElementById("phoneValidation");
    const cubaMobilePrefixes = ["5", "52", "53", "54", "55"];
    const isValid = cubaMobilePrefixes.some((prefix) => phoneInput.value.startsWith(prefix));
    if (!isValid) {
        phoneValidation.style.display = "block";
    } else {
        phoneValidation.style.display = "none";
    }
}