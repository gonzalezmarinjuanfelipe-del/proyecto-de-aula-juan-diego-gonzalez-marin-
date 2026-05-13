// dashboard.js - Funcionalidades del dashboard
// Sistema de Inventario Deportivo
// Fundación Escuela Tecnológica de Neiva
// Autor: Juan Diego Gonzalez Marin

document.addEventListener("DOMContentLoaded", function () {
  // Gráfico de categorías
  const ctx = document.getElementById("categoryChart");
  if (ctx) {
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Baloncesto", "Fútbol", "Voleibol", "Atletismo", "Natación"],
        datasets: [
          {
            data: [10, 15, 5, 20, 12], // Datos de ejemplo
            backgroundColor: [
              "#1a365d",
              "#2d3748",
              "#00bcd4",
              "#48bb78",
              "#ed8936",
            ],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              usePointStyle: true,
            },
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        },
      },
    });
  }

  // Animar números de estadísticas
  function animateNumbers() {
    const statNumbers = document.querySelectorAll(".stat-content h3");
    statNumbers.forEach((stat) => {
      const target = parseInt(stat.textContent);
      let current = 0;
      const increment = target / 50;
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          stat.textContent = target;
          clearInterval(timer);
        } else {
          stat.textContent = Math.floor(current);
        }
      }, 30);
    });
  }

  // Ejecutar animación después de un pequeño delay
  setTimeout(animateNumbers, 500);

  // Actualizar actividad reciente cada 30 segundos
  setInterval(() => {
    // Aquí se podría hacer una petición AJAX para actualizar la actividad
    console.log("Actualizando actividad reciente...");
  }, 30000);
});
