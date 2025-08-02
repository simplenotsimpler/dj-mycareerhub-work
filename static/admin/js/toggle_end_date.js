const toggleEndDate = () => {
  const isCurrentCheckbox = document.querySelector("#id_is_current");
  const endDateInput = document.querySelector("#id_end_date");
  const endDateFieldBox = document.querySelector(".field-end_date.fieldBox");
  const endDateShortcuts = endDateFieldBox?.querySelector(".datetimeshortcuts");

  const disableEndDate = () => {
    endDateInput.disabled = true;
    endDateFieldBox?.classList.add("is-disabled");
    if (endDateShortcuts) {
      endDateShortcuts.querySelectorAll("a").forEach((link) => {
        link.setAttribute("tabindex", "-1");
        link.setAttribute("aria-disabled", "true");
        link.style.pointerEvents = "none";
        link.style.opacity = "0.5";
      });
    }
  };

  const enableEndDate = () => {
    endDateInput.disabled = false;
    endDateFieldBox?.classList.remove("is-disabled");
    if (endDateShortcuts) {
      endDateShortcuts.querySelectorAll("a").forEach((link) => {
        link.removeAttribute("tabindex");
        link.removeAttribute("aria-disabled");
        link.style.pointerEvents = "";
        link.style.opacity = "";
      });
    }
  };

  const updateEndDateState = () => {
    isCurrentCheckbox.checked ? disableEndDate() : enableEndDate();
  };

  if (isCurrentCheckbox && endDateInput && endDateFieldBox) {
    updateEndDateState();
    isCurrentCheckbox.addEventListener("change", updateEndDateState);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  toggleEndDate();
});
