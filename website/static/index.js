document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('past_best_by') && document.getElementById('exp') && document.getElementById('best-by')) {
        initializeAddPage();
    }

    if (document.querySelector(".quantity-container")) {
        initializeHomePage();
    }
});

function initializeAddPage() {
    past_best_by_field = document.getElementById('past_best_by');
    exp_field = document.getElementById('exp');
    best_by_field = document.getElementById('best-by'); 

    function updateExpirationDate() {
        past_best_by = past_best_by_field.value;
        best_by = new Date(best_by_field.value);
        
        let expiration;
  
        if (past_best_by === '5-days') {
            expiration = new Date(best_by);
            expiration.setDate(expiration.getDate() + 5);
        } else if (past_best_by === '1-month') {
            expiration = new Date(best_by);
            expiration.setMonth(expiration.getMonth() + 1);
        } else if (past_best_by === '6-months') {
            expiration = new Date(best_by);
            expiration.setMonth(expiration.getMonth() + 6);
        }
        
        formatted_date = expiration.toISOString().split('T')[0];
        exp_field.value = formatted_date;
    }

    past_best_by_field.addEventListener('change', updateExpirationDate);  
    best_by_field.addEventListener('change', updateExpirationDate);

    document.getElementById('imageUpload').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.getElementById('previewImg');
                img.src = e.target.result;
                img.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
}

function initializeHomePage() {
    QuantityButtons();
    setupDeleteButtons();

    document.getElementById("filter").addEventListener("change", async function () {
        let filterValue = this.value;

        try {
            let response = await fetch(`/filter/${filterValue}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                let data = await response.json();  
                updateTable(data.results); 
            } else {
                console.error("Filtering failed");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
    
    function QuantityButtons() {
        const buttons = document.querySelectorAll(".button");

        buttons.forEach(button => {
            button.onclick = async function (event) { 
                event.preventDefault(); 
                event.stopPropagation();  

                let quantitySpan = this.parentElement.querySelector(".quantity");
                let id = this.getAttribute("data-id");
                let action = this.classList.contains("minus") ? "minus" : "plus"; 

                try {
                    let response = await fetch(`/${action}/${id}`, {
                        method: "POST",
                    });

                    if (response.ok) {
                        let newQuantity = action === "minus"
                            ? Math.max(0, parseInt(quantitySpan.textContent, 10) - 1)
                            : parseInt(quantitySpan.textContent, 10) + 1;

                        quantitySpan.textContent = newQuantity;
                    } else {
                        console.error("Failed to update quantity");
                    }
                } catch (error) {
                    console.error("Error:", error);
                }
            };
        });
    }

    function updateTable(results) {
        let tbody = document.querySelector("tbody");
        tbody.innerHTML = ""; 

        results.forEach(result => {
            let row = document.createElement("tr");
            row.id = `row-${result.primary_id}`;
            row.innerHTML = `
                <td>${result.image ? `<img src="/static/uploads/${result.image}" alt="${result.name}" class="product-img">` : "No Image"}</td>
                <td>${result.name}</td>
                <td>${result.date_arrived}</td>
                <td>${result.tefap}</td>
                <td>${result.best_by}</td>
                <td>${result.expiration}</td>
                <td>${result.location}</td>
                <td>
                    <div class="quantity-container">
                        <button type="button" class="button minus" data-id="${result.primary_id}"> - </button>
                        <span class="quantity" data-id="${result.primary_id}">${result.quantity}</span>
                        <button type="button" class="button plus" data-id="${result.primary_id}"> + </button>
                    </div>
                </td>                        
                <td>
                    <a href="/edit/${result.primary_id}" class="edit-button">Edit</a>
                </td>
                <td>
                    <button class="delete-button" data-id="${result.primary_id}">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        QuantityButtons();
        setupDeleteButtons();
    }

    function setupDeleteButtons() {
        document.querySelectorAll(".delete-button").forEach(button => {
            button.addEventListener("click", function() {
                let itemId = this.getAttribute("data-id");
                if (confirm("Are you sure you want to delete this item?")) {
                    fetch(`/delete/${itemId}`, {
                        method: "DELETE",
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Item deleted successfully.");
                            location.reload(); 
                        } else {
                            alert("Error deleting item.");
                        }
                    })
                    .catch(error => console.error("Error:", error));
                }
            });
        });
    }
}
