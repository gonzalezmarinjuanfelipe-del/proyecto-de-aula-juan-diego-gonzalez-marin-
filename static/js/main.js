// main.js - Funcionalidades principales
// Sistema de Inventario Deportivo
// Fundación Escuela Tecnológica de Neiva
// Autor: Juan Diego Gonzalez Marin

// Función para toggle del menú hamburguesa
function toggleMenu() {
  const navbar = document.querySelector(".navbar");
  const hamburger = document.querySelector(".hamburger");

  navbar.classList.toggle("active");
  hamburger.classList.toggle("active");
}

// Cerrar menú al hacer clic fuera
document.addEventListener("click", function (e) {
  const navbar = document.querySelector(".navbar");
  const hamburger = document.querySelector(".hamburger");

  if (!navbar.contains(e.target) && !hamburger.contains(e.target)) {
    navbar.classList.remove("active");
    hamburger.classList.remove("active");
  }
});

// Animaciones de entrada para elementos
document.addEventListener("DOMContentLoaded", function () {
  // Animar tarjetas de estadísticas
  const statCards = document.querySelectorAll(".stat-card");
  statCards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";

    setTimeout(() => {
      card.style.transition = "all 0.5s ease-out";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, index * 100);
  });

  // Animar filas de tabla
  const tableRows = document.querySelectorAll(".table-modern tbody tr");
  tableRows.forEach((row, index) => {
    row.style.opacity = "0";
    row.style.transform = "translateY(10px)";

    setTimeout(() => {
      row.style.transition = "all 0.3s ease-out";
      row.style.opacity = "1";
      row.style.transform = "translateY(0)";
    }, index * 50);
  });
});

// Función para mostrar notificaciones toast
function showToast(message, type = "success") {
  // Crear elemento toast
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${type === "success" ? "fa-check-circle" : type === "error" ? "fa-exclamation-circle" : "fa-info-circle"}"></i>
            <span>${message}</span>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;

  // Agregar al DOM
  document.body.appendChild(toast);

  // Animar entrada
  setTimeout(() => {
    toast.style.transform = "translateX(0)";
    toast.style.opacity = "1";
  }, 100);

  // Auto-remover después de 5 segundos
  setTimeout(() => {
    toast.style.transform = "translateX(100%)";
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

// Agregar estilos para toast
const toastStyles = `
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    padding: 15px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    transform: translateX(100%);
    opacity: 0;
    transition: all 0.3s ease;
    z-index: 10000;
    min-width: 300px;
}

.toast-success {
    border-left: 4px solid #48bb78;
}

.toast-error {
    border-left: 4px solid #f56565;
}

.toast-warning {
    border-left: 4px solid #ed8936;
}

.toast-content {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}

.toast-content i {
    font-size: 20px;
}

.toast-success .toast-content i {
    color: #48bb78;
}

.toast-error .toast-content i {
    color: #f56565;
}

.toast-warning .toast-content i {
    color: #ed8936;
}

.toast-close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #718096;
    padding: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}
`;

// Agregar estilos al head
const styleSheet = document.createElement("style");
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);

// Función para confirmar acciones
function confirmAction(message, callback) {
  if (confirm(message)) {
    callback();
  }
}

// Validación de formularios
function validateForm(form) {
  const inputs = form.querySelectorAll(
    "input[required], select[required], textarea[required]",
  );
  let isValid = true;

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.style.borderColor = "#f56565";
      isValid = false;
    } else {
      input.style.borderColor = "#e2e8f0";
    }
  });

  return isValid;
}

// Event listeners para validación en tiempo real
document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        if (this.hasAttribute("required") && !this.value.trim()) {
          this.style.borderColor = "#f56565";
        } else {
          this.style.borderColor = "#e2e8f0";
        }
      });

      input.addEventListener("input", function () {
        if (this.value.trim()) {
          this.style.borderColor = "#00bcd4";
        }
      });
    });
  });
});
