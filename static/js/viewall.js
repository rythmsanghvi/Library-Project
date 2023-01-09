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
document.addEventListener("DOMContentLoaded", function () {
  // Call the displayData function when the document is ready
  displayData();
});
