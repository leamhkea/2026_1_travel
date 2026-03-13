document.querySelectorAll(".deleteBtn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    if (!confirm("Are you sure you want to delete this destination?")) {
      e.preventDefault();
    }
  });
});
