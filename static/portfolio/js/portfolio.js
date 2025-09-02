document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const navMenu = document.querySelector(".nav-menu");
  const navItems = document.querySelectorAll(".nav-item");

  // Ensure the hamburger menu button is clickable
  hamburger.addEventListener("click", function () {
    // Toggle the 'expanded' class for both nav-menu and hamburger
    navMenu.classList.toggle("expanded");
    hamburger.classList.toggle("expanded");
  });

  // Toggle the 'aria-expanded' attribute for accessibility
  const expanded = hamburger.getAttribute("aria-expanded") === "true";
  hamburger.setAttribute("aria-expanded", !expanded);

  // --- Remove hash & reset scroll on refresh ---
  if (window.location.hash) {
    history.replaceState(
      null,
      "",
      window.location.pathname + window.location.search
    );
    window.scrollTo(0, 0);
  }

  // --- Highlight menu items on click ---
  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Remove active class from all items
      navItems.forEach((i) => i.classList.remove("active"));

      // Add active class to the clicked item
      this.classList.add("active");
    });
  });

  // Special case: brand-name link clears active state
  const brandLink = document.querySelector(".brand-name");
  brandLink.addEventListener("click", () => {
    navItems.forEach((i) => i.classList.remove("active"));
  });
});
