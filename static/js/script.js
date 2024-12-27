// Sélection des éléments
const burger = document.getElementById('burger');
const navLinks = document.getElementById('nav-links');

// Gestion du clic sur l'icône "burger"
burger.addEventListener('click', (event) => {
  // Empêche la propagation pour éviter la fermeture immédiate
  event.stopPropagation();

  // On bascule (toggle) la transformation sur la liste
  navLinks.style.transform =
    navLinks.style.transform === 'translateX(0%)'
      ? 'translateX(100%)'
      : 'translateX(0%)';

  // Ajout d'une classe pour une animation
  navLinks.classList.toggle('nav-active');
});

// Gestion du clic en dehors du menu burger
document.addEventListener('click', () => {
  if (navLinks.classList.contains('nav-active')) {
    navLinks.style.transform = 'translateX(100%)';
    navLinks.classList.remove('nav-active');
  }
});

// Fonction pour les animations au scroll
document.addEventListener('DOMContentLoaded', () => {
  const elementsToReveal = document.querySelectorAll('.reveal');

  const revealOnScroll = () => {
    const windowHeight = window.innerHeight;
    const scrollY = window.scrollY;

    elementsToReveal.forEach((el) => {
      const elementTop = el.getBoundingClientRect().top + scrollY;

      if (scrollY + windowHeight >= elementTop + 50) {
        el.classList.add('visible');
      } else {
        el.classList.remove('visible');
      }
    });
  };

  revealOnScroll(); // Initial call

  window.addEventListener('scroll', revealOnScroll);
});

// Ajout d'une animation au survol des éléments
const interactiveItems = document.querySelectorAll('.interactive');
interactiveItems.forEach((item) => {
  item.addEventListener('mouseover', () => {
    item.classList.add('hovered');
  });

  item.addEventListener('mouseout', () => {
    item.classList.remove('hovered');
  });
});
