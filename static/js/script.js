/*****************************************************************/
/* SCRIPT GLOBAL - VERSION STABLE                                */
/*****************************************************************/

// Gestion du menu burger
const burger = document.getElementById('burger');
const navLinks = document.getElementById('nav-links');

burger.addEventListener('click', (event) => {
  event.stopPropagation();
  navLinks.classList.toggle('nav-active');
});

// Ferme le menu si on clique ailleurs
document.addEventListener('click', () => {
  if (navLinks.classList.contains('nav-active')) {
    navLinks.classList.remove('nav-active');
  }
});
