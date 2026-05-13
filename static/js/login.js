// login.js - Funcionalidades del login
// Sistema de Inventario Deportivo
// Fundación Escuela Tecnológica de Neiva
// Autor: Juan Diego Gonzalez Marin

// Función para mostrar/ocultar contraseña
function togglePassword() {
  const passwordInput = document.getElementById("password");
  const toggleIcon = document.querySelector(".toggle-password");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    toggleIcon.classList.remove("fa-eye-slash");
    toggleIcon.classList.add("fa-eye");
  }
}

// Animación de entrada
document.addEventListener("DOMContentLoaded", function () {
  const loginCard = document.querySelector(".login-card");
  loginCard.style.opacity = "0";
  loginCard.style.transform = "translateY(20px)";

  setTimeout(() => {
    loginCard.style.transition = "all 0.5s ease-out";
    loginCard.style.opacity = "1";
    loginCard.style.transform = "translateY(0)";
  }, 100);
});

// Validación del formulario
document.querySelector(".login-form").addEventListener("submit", function (e) {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    e.preventDefault();
    alert("Por favor, complete todos los campos.");
    return false;
  }

  // Mostrar loader
  const submitBtn = document.querySelector(".btn-login");
  const originalText = submitBtn.innerHTML;
  submitBtn.innerHTML = '<div class="loader"></div> Iniciando...';
  submitBtn.disabled = true;

  // Revertir después de 2 segundos si no se envía
  setTimeout(() => {
    if (submitBtn.disabled) {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  }, 2000);
});
