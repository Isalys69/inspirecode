/*****************************************************************/
/* SCRIPT GLOBAL – HEADER & NAVIGATION                           */
/* VERSION STABLE – DESKTOP / MOBILE / TACTILE                  */
/*****************************************************************/

document.addEventListener("DOMContentLoaded", () => {

  /* ============================================================= */
  /* MENU MOBILE (BURGER)                                          */
  /* ============================================================= */

  const burgerBtn = document.getElementById("burgerBtn");
  const mobileMenu = document.getElementById("mobileMenu");

  if (burgerBtn && mobileMenu) {

    /* ------------------------------------------------------------- */
    /* OUVERTURE / FERMETURE DU MENU MOBILE                           */
    /* ------------------------------------------------------------- */

    burgerBtn.addEventListener("click", (event) => {
      // Empêche le clic de remonter au document
      event.stopPropagation();

      // Toggle ouverture / fermeture
      mobileMenu.classList.toggle("ic-mobile-open");
    });

    /* ------------------------------------------------------------- */
    /* FERMETURE DU MENU SI CLIC EN DEHORS                            */
    /* ------------------------------------------------------------- */

    document.addEventListener("click", () => {
      if (mobileMenu.classList.contains("ic-mobile-open")) {
        mobileMenu.classList.remove("ic-mobile-open");
      }
    });

    /* ------------------------------------------------------------- */
    /* EMPÊCHER LA FERMETURE SI CLIC DANS LE MENU                     */
    /* ------------------------------------------------------------- */

    mobileMenu.addEventListener("click", (event) => {
      event.stopPropagation();
    });

    /* ------------------------------------------------------------- */
    /* SOUS-MENU "OFFRES" – MENU MOBILE                               */
    /* ------------------------------------------------------------- */

    const mobileDropdownToggles =
      mobileMenu.querySelectorAll(".ic-dropdown-toggle");

    mobileDropdownToggles.forEach(toggle => {
      toggle.addEventListener("click", (event) => {

        // Empêche le lien "#" de provoquer un scroll
        event.preventDefault();

        // Empêche la fermeture du menu mobile
        event.stopPropagation();

        // Le sous-menu est juste après le lien
        const submenu = toggle.nextElementSibling;
        if (!submenu) return;

        // Ouvre / ferme le sous-menu
        submenu.classList.toggle("open");
      });
    });
  }

  /* ============================================================= */
  /* MENU DESKTOP – ÉCRANS TACTILES (PAYSAGE, TABLETTE)            */
  /* ============================================================= */

  // Cible le lien "Offres" du menu desktop
  const desktopDropdownLinks =
    document.querySelectorAll(".ic-nav .ic-dropdown > a");

  desktopDropdownLinks.forEach(link => {
    link.addEventListener("click", (event) => {

      // On détecte un écran tactile (pas de hover fiable)
      const isTouchDevice = window.matchMedia(
        "(hover: none) and (pointer: coarse)"
      ).matches;

      if (!isTouchDevice) return;

      // Empêche la navigation immédiate
      event.preventDefault();

      // Le sous-menu est juste après le lien
      const submenu = link.nextElementSibling;
      if (!submenu) return;

      // Ouvre / ferme le sous-menu
      submenu.classList.toggle("open");
    });
  });

});
