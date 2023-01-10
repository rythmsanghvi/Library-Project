function displayData() {
  // Send an HTTP request to the server to retrieve the data
  fetch("http://127.0.0.1:5000/data-fetch")
    .then((response) => response.json())
    .then((rows) => {
      document.getElementById("tbody").innerHTML = "";
      // Use vanilla JavaScript to append rows to the table body
      rows.forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${row.ID}</td>
          <td><a href="book/${row.ID}">${row.Books}</td>
          <td>${row.Author}</td>
          <td>${row.ISBN}</td>
        `;
        document.getElementById("tbody").appendChild(tr);
      });
    });
}

function openDiv() {
  document.getElementById('search-table-div').style.display = 'block';
}
function closeDiv() {
  document.getElementById('search-table-div').style.display = 'none';
}

function searchBooks() {
  // Get the search query from the search box
  const search_term = document.getElementById("search").value;
  // Send an HTTP POST request to the server with the search query
  fetch("http://127.0.0.1:5000/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({search_term}),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        openDiv();
      // Clear the search results container
      document.getElementById("search-results").innerHTML = "";

      // Loop through the search results and display them in the container
      (data.rows).forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${row.ID}</td>
          <td>${row.Books}</td>
          <td>${row.Author}</td>
          <td>${row.ISBN}</td>
        `;
        document.getElementById("search-results").appendChild(tr);
      });
    } else{
      alert("Data not found!")
      closeDiv();
    }});
}


document.addEventListener("DOMContentLoaded", function () {
  // Call the displayData function when the document is ready
  displayData();
});
// Add an event listener to the search form to handle search submissions
document.getElementById("search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  searchBooks();
});


