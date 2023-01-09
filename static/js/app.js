// JavaScript code

function showError(error) {
  var errorMessageElement = document.getElementById('error-message');
  errorMessageElement.innerHTML = error;
}

document.getElementById('signup-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  fetch('http://127.0.0.1:5000/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, email, password})
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Successfully signed up');
        document.getElementById('signup-form').reset();
        // You can close the modal here
      } else {
        showError(data.error);
      }
    });
});


