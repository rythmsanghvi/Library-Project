// JavaScript code
function openLoginModal() {
  document.getElementById('id01').style.display = 'none';
  document.getElementById('id02').style.display = 'block';
}
function showError(error) {
  var errorMessageElement = document.getElementById("error-message");
  errorMessageElement.innerHTML = error+".<a href='/login' onclick='openLoginModal();return false;'> Try logging in.</a>";
}

document.getElementById("signup-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name1").value;
  const email = document.getElementById("email1").value;
  const password = document.getElementById("password1").value;

  fetch("http://127.0.0.1:5000/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Successfully signed up");
        document.getElementById("signup-form").reset();
        openLoginModal();
        // You can close the modal here
      } else {
        showError(data.error);
      }
    });
});
