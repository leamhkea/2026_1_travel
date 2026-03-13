// Function to add error messages to the list
function addErrorLiLogin(errorMessage: string): void {
  const errors = document.getElementById("errors");

  if (!errors) return;

  const li = document.createElement("li");
  li.textContent = errorMessage;
  errors.appendChild(li);
}

// Wait until page is loaded
window.addEventListener("load", () => {
  const form = document.getElementById("formLogin") as HTMLFormElement;

  if (!form) return;

  form.addEventListener("submit", (e: Event) => {
    const email = (document.getElementById("email") as HTMLInputElement).value;
    const password = (document.getElementById("password") as HTMLInputElement)
      .value;

    console.log(email, password);

    const errors = document.getElementById("errors");

    if (errors) {
      errors.innerHTML = "";
    }

    let hasError = false;

    // Email validation
    if (email.trim() === "") {
      addErrorLiLogin("Email must be filled out");
      hasError = true;
    } else if (!email.includes("@")) {
      addErrorLiLogin("Email must contain @");
      hasError = true;
    }

    // Password validation
    if (password.trim() === "") {
      addErrorLiLogin("Password must be filled out");
      hasError = true;
    }

    // If errors then stop submit
    if (hasError) {
      e.preventDefault();
      return;
    }
  });
});
