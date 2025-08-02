const isISODate = (value) => /^\d{4}-\d{2}-\d{2}$/.test(value.trim());

const getFieldBox = (input) => input.closest('.fieldBox');
const getFormRow = (input) => input.closest('.form-row');
const getAdminForm = (input) => input.closest('form');

const ensureErrorNote = (form) => {
  if (!form.querySelector('.errornote[data-iso-error]')) {
    const errorNote = document.createElement('p');
    errorNote.className = 'errornote';
    errorNote.dataset.isoError = 'true';
    errorNote.textContent = 'Please correct the error below.';
    form.insertBefore(errorNote, form.firstChild);
  }
};

const removeErrorNoteIfNoErrors = (form) => {
  if (!form.querySelector('input.vDateField.error')) {
    const note = form.querySelector('.errornote[data-iso-error]');
    if (note) note.remove();
  }
};

const updateFormRowErrors = (formRow) => {
  const hasError = !!formRow.querySelector('input.vDateField.error');
  if (hasError) {
    formRow.classList.add('errors');
  } else {
    formRow.classList.remove('errors');
  }
};

const showFieldError = (input) => {
  const fieldBox = getFieldBox(input);
  const formRow = getFormRow(input);

  fieldBox?.classList.add('errors');
  updateFormRowErrors(formRow);

  // remove old errorlist
  const oldError = formRow.querySelector('.errorlist[data-iso-error]');
  if (oldError) oldError.remove();

  // create errorlist
  const errorList = document.createElement('ul');
  errorList.className = 'errorlist';
  errorList.dataset.isoError = 'true';
  errorList.id = `${input.id}_error`;

  const errorItem = document.createElement('li');
  errorItem.textContent = 'Enter a valid date in YYYY-MM-DD format.';
  errorList.appendChild(errorItem);

  // ✅ Insert errorlist as the FIRST CHILD of formRow
  formRow.insertBefore(errorList, formRow.firstChild);

  // update ARIA attributes
  input.setAttribute('aria-invalid', 'true');
  const describedBy = input.getAttribute('aria-describedby') || '';
  if (!describedBy.includes(errorList.id)) {
    input.setAttribute(
      'aria-describedby',
      (describedBy + ' ' + errorList.id).trim()
    );
  }
};

const clearFieldError = (input) => {
  const fieldBox = getFieldBox(input);
  const formRow = getFormRow(input);

  fieldBox?.classList.remove('errors');
  updateFormRowErrors(formRow);

  const errorList = formRow.querySelector('.errorlist[data-iso-error]');
  if (errorList) errorList.remove();

  input.removeAttribute('aria-invalid');

  // clean up aria-describedby
  const errorId = `${input.id}_error`;
  const describedBy = input.getAttribute('aria-describedby') || '';
  input.setAttribute(
    'aria-describedby',
    describedBy
      .split(' ')
      .filter((id) => id !== errorId)
      .join(' ')
      .trim()
  );
};

const handleDateBlur = (event) => {
  const input = event.target;
  const form = getAdminForm(input);

  if (input.value && !isISODate(input.value)) {
    input.classList.add('error');
    showFieldError(input);
    ensureErrorNote(form);
  } else {
    input.classList.remove('error');
    clearFieldError(input);
    removeErrorNoteIfNoErrors(form);
  }
};

const attachISODateValidation = () => {
  document.querySelectorAll('input.vDateField').forEach((input) => {
    input.addEventListener('blur', handleDateBlur);
  });
};

document.addEventListener('DOMContentLoaded', attachISODateValidation);
