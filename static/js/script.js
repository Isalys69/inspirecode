document.addEventListener("DOMContentLoaded", () => {

  /* ===================================================== */
  /* MENU MOBILE (BURGER)                                  */
  /* ===================================================== */

  const burgerBtn = document.getElementById("burgerBtn");
  const mobileMenu = document.getElementById("mobileMenu");

  if (burgerBtn && mobileMenu) {
    burgerBtn.addEventListener("click", e => {
      e.stopPropagation();
      mobileMenu.classList.toggle("ic-mobile-open");
    });

    document.addEventListener("click", () => {
      mobileMenu.classList.remove("ic-mobile-open");
    });

    mobileMenu.addEventListener("click", e => e.stopPropagation());
  }

  /* ===================================================== */
  /* DROPDOWN "OFFRES" – OUVERTURE / FERMETURE PROPRE      */
  /* ===================================================== */

  const dropdowns = document.querySelectorAll(".ic-dropdown");
  const dropdownToggles = document.querySelectorAll(".ic-dropdown-toggle");

  dropdownToggles.forEach(button => {
    button.addEventListener("click", e => {
      e.stopPropagation();

      const currentDropdown = button.closest(".ic-dropdown");
      if (!currentDropdown) return;

      // Ferme tous les autres dropdowns
      dropdowns.forEach(dropdown => {
        if (dropdown !== currentDropdown) {
          dropdown.classList.remove("is-open");
        }
      });

      // Toggle du dropdown courant
      currentDropdown.classList.toggle("is-open");
    });
  });

  // Clic ailleurs → fermeture de tous les dropdowns
  document.addEventListener("click", () => {
    dropdowns.forEach(dropdown => {
      dropdown.classList.remove("is-open");
    });
  });


  /* ===================================================== */
  /* AFFICHAGE DE LA BULLE INFORMATIVE                     */
  /* ===================================================== */
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el))



});
