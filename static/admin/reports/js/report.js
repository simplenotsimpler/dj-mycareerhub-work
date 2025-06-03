// https://stackoverflow.com/questions/20101409/how-can-i-insert-a-print-button-that-prints-a-form-in-a-webpage
/* alignment:
    https://stackoverflow.com/questions/6632340/place-a-button-right-aligned

    answered Apr 10, 2020 at 10:11
    phan kosal's user avatar
    phan kosal
*/
//NOTE: semantic - debatable if should be div or another option
const buildPrint = () => {
  const reportDate = document.querySelector(".report-header");

  if (reportDate) {
    const printHTML = `
      <div id="print-action">
        <div><strong>NOTE:</strong> browser headers and footers have to be removed in the browser print dialog</div>
        <div><input type="button" value="Print" onClick="window.print()"></div>
      </div>
    `;
    reportDate.insertAdjacentHTML("afterend", printHTML);
  }
};

// have to wait until DOM loads
document.addEventListener("DOMContentLoaded", () => {
  buildPrint();
});
