/*****************************************************************/
/* SCRIPT GLOBAL - VERSION OPTIMISÉE POUR NOUVEAU HEADER        */
/*****************************************************************/

/* ---- MENU MOBILE ---- */

const burgerBtn = document.getElementById("burgerBtn");
const mobileMenu = document.getElementById("mobileMenu");

if (burgerBtn && mobileMenu) {

  // Toggle ouverture/fermeture du menu mobile
  burgerBtn.addEventListener("click", (event) => {
    event.stopPropagation(); // empêche la fermeture immédiate
    mobileMenu.classList.toggle("ic-mobile-open");
  });

  // Fermer le menu si clic hors menu
  document.addEventListener("click", () => {
    if (mobileMenu.classList.contains("ic-mobile-open")) {
      mobileMenu.classList.remove("ic-mobile-open");
    }
  });

  // Empêcher fermeture si clic à l'intérieur du menu
  mobileMenu.addEventListener("click", (event) => {
    event.stopPropagation();
  });
}
