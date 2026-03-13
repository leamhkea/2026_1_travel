// Function to add error messages to the list
function addErrorLiDestination(errorMessage: string): void {
  const errors = document.getElementById("errors");

  if (!errors) return;

  const li = document.createElement("li");
  li.textContent = errorMessage;
  errors.appendChild(li);
}

// Wait until page is loaded
window.addEventListener("load", () => {
  const form = document.getElementById("formDestination") as HTMLFormElement;

  if (!form) return;

  form.addEventListener("submit", (e: Event) => {
    const title = (document.getElementById("title") as HTMLInputElement).value;
    const country = (document.getElementById("country") as HTMLInputElement)
      .value;
    const location = (document.getElementById("location") as HTMLInputElement)
      .value;
    const description = (
      document.getElementById("description") as HTMLTextAreaElement
    ).value;
    const datefrom = (document.getElementById("datefrom") as HTMLInputElement)
      .value;
    const dateto = (document.getElementById("dateto") as HTMLInputElement)
      .value;

    console.log(title, country, location, description, datefrom, dateto);

    const errors = document.getElementById("errors");
    if (errors) {
      errors.innerHTML = "";
    }

    let hasError = false;

    // Title validation
    if (title.trim() === "") {
      addErrorLiDestination("Title must be filled out");
      hasError = true;
    } else if (title.trim().length < 2) {
      addErrorLiDestination("Title must be at least 2 characters");
      hasError = true;
    }

    // Country validation
    if (country.trim() === "") {
      addErrorLiDestination("Country must be filled out");
      hasError = true;
    }

    // Location validation
    if (location.trim() === "") {
      addErrorLiDestination("Location must be filled out");
      hasError = true;
    }

    // Date validation
    if (datefrom && dateto && datefrom > dateto) {
      addErrorLiDestination("Date from cannot be after date to");
      hasError = true;
    }

    // If errors then stop submit
    if (hasError) {
      e.preventDefault();
      return;
    }
  });
});
