function displayData() {
  // Send an HTTP request to the server to retrieve the data
  fetch("http://127.0.0.1:5000/lend-fetch")
    .then((response) => response.json())
    .then((rows) => {
      document.getElementById("tbody").innerHTML = "";
      // Use vanilla JavaScript to append rows to the table body
      rows.forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
              <td>${row.ID}</td>
              <td>${row.Name}</td>
              <td>${row.Book}</td>
              <td>${row.Date}</td>
              <td>${row.Due_Date}</td>
              <td>${row.cardnumber}</td>
            `;
        document.getElementById("tbody").appendChild(tr);
      });
    });
}

function addData() {
  // Get the data from the form
  const name = document.getElementById("Name").value;
  const book = document.getElementById("Book").value;
  const cardnumber = document.getElementById("cardnumber").value;
  // Send an HTTP POST request to the server with the data
  fetch("http://127.0.0.1:5000/lend-add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, book, cardnumber }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Data added successfully");
        document.getElementById("lend-form").reset();
        displayData();
      } else {
        alert("Error adding data");
      }
    });
}

document.getElementById("lend-form").addEventListener("submit", function (e) {
  e.preventDefault();
  addData();
});

document.addEventListener("DOMContentLoaded", function () {
  // Call the displayData function when the document is ready
  displayData();
});
