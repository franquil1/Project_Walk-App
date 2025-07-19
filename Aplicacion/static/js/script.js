const QRCode = require('qrcode');

// URL de la imagen que dice "No disponible aún"
const imageUrl = 'https://via.placeholder.com/300x200.png?text=No+disponible+aun';

// Generar el código QR
QRCode.toFile('qrcode.png', imageUrl, (err) => {
    if (err) {
        console.error('Error al generar el código QR:', err);
    } else {
        console.log('Código QR generado exitosamente como "qrcode.png".');
    }
});

// animacion de texto

const elementsToFadeIn = document.querySelectorAll('.fade-in-element');

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // Opcional: dejar de observar una vez que aparece
        }
    });
}, {
    threshold: 0.1 // Define qué porcentaje del elemento debe ser visible para activar la animación
});

elementsToFadeIn.forEach(element => {
    observer.observe(element);
});

//boton verde 
document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".card__button.secondary");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const heart = document.createElement("span");
            heart.classList.add("heart-icon");
            heart.innerHTML = "&#x1F49A;"; // Green heart emoji
            heart.style.cursor = "pointer";
            heart.style.marginLeft = "10px";

            button.parentNode.appendChild(heart);

            heart.addEventListener("click", () => {
                heart.remove();
            });
        });
    });
});

// menu desplegable

