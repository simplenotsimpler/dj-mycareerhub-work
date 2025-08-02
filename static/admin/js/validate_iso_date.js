const isISODate = (value) => /^\d{4}-\d{2}-\d{2}$/.test(value.trim());

const showInvalidDateAlert = (input) => {
  alert('Please enter the date in ISO format: YYYY-MM-DD');
  input.focus();
};

const handleDateBlur = (event) => {
  const input = event.target;
  if (input.value && !isISODate(input.value)) {
    showInvalidDateAlert(input);
  }
};

const attachISODateValidation = () => {
  document.querySelectorAll('input.vDateField')
    .forEach((input) => input.addEventListener('blur', handleDateBlur));
};

document.addEventListener('DOMContentLoaded', attachISODateValidation);
