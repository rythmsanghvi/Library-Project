function displayData() {
    // Send an HTTP request to the server to retrieve the data
    fetch('http://127.0.0.1:5000/data-fetch-management')
      .then(response => response.json())
      .then(rows => {
        document.getElementById('tbody').innerHTML = ''
        // Use vanilla JavaScript to append rows to the table body
        rows.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${row.ID}</td>
            <td><a href="book/${row.ID}">${row.Books}</td>
            <td>${row.Author}</td>
            <td>${row.ISBN}</td>
          `;
          document.getElementById('tbody').appendChild(tr);
      });
    });
}

function addData() {
  // Get the data from the form
  const book = document.getElementById('Book').value;
  const author = document.getElementById('Author').value;
  const isbn = document.getElementById('ISBN').value;
  const description = document.getElementById('Description').value;

  // Send an HTTP POST request to the server with the data
  fetch('http://127.0.0.1:5000/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({book, author, isbn, description})
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Data added successfully');
        document.getElementById('add-form').reset();
        displayData();
        document.getElementById('add-form').reset();
      } else {
        alert('Error adding data');
      }
    });
}

document.getElementById('add-form').addEventListener('submit', function(e) {
  e.preventDefault();
  addData();
});

function deleteData() {
  // Get the data from the form
  const book = document.getElementById('Book-del').value;

  // Send an HTTP POST request to the server with the data
  fetch('http://127.0.0.1:5000/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(book)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Data deleted successfully');
        document.getElementById('delete-form').reset();
        displayData();
      } else {
        alert('Error deleting data');
      }
    });
}

document.getElementById('delete-form').addEventListener('submit', function(e) {
  e.preventDefault();
  deleteData();
});

document.addEventListener('DOMContentLoaded', function() {
  // Call the displayData function when the document is ready
  displayData();
});