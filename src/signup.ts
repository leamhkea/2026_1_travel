// Function to add error messages to the list
function addErrorLiSignup(errorMessage: string): void {
  const errors = document.getElementById("errors");

  if (!errors) return;

  const li = document.createElement("li");
  li.textContent = errorMessage;
  errors.appendChild(li);
}

// Wait until page is loaded
window.addEventListener("load", () => {
  const form = document.getElementById("formUser") as HTMLFormElement;

  if (!form) return;

  form.addEventListener("submit", (e: Event) => {
    const firstname = (document.getElementById("firstname") as HTMLInputElement)
      .value;
    const lastname = (document.getElementById("lastname") as HTMLInputElement)
      .value;
    const email = (document.getElementById("email") as HTMLInputElement).value;
    const password = (document.getElementById("password") as HTMLInputElement)
      .value;

    console.log(firstname, lastname, email, password);

    const errors = document.getElementById("errors");

    if (errors) {
      errors.innerHTML = "";
    }

    let hasError = false;

    // Firstname validation
    if (firstname.trim() === "") {
      addErrorLiSignup("Firstname must be filled out");
      hasError = true;
    }

    // Lastname validation
    if (lastname.trim() === "") {
      addErrorLiSignup("Lastname must be filled out");
      hasError = true;
    }

    // Email validation
    if (email.trim() === "") {
      addErrorLiSignup("Email must be filled out");
      hasError = true;
    } else if (!email.includes("@")) {
      addErrorLiSignup("Email must contain @");
      hasError = true;
    }

    // Password validation
    if (password.trim() === "") {
      addErrorLiSignup("Password must be filled out");
      hasError = true;
    }

    // If errors then stop submit
    if (hasError) {
      e.preventDefault();
      return;
    }
  });
});
