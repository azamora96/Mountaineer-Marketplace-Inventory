document.addEventListener("DOMContentLoaded", function () {

    QuantityButtons();
    setupDeleteButtons();
    setupImageModal();

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

    document.getElementById("searchbar").addEventListener("input", async function () {
        query = this.value.trim();

        try {
            let response = await fetch(`/search?q=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                let data = await response.json();
                updateTable(data.results);
            } else {
                console.error("Search failed");
            }
        } catch (error) {
            console.error("Error during search:", error);
        }
    })
    
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

                            

                            if(newQuantity == 0){
                                if (confirm("Do you want to delete this item?")) {
                                    fetch(`/delete/${id}`, {
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
                            }
                            

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
        setupImageModal();
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

    function setupImageModal() {
        document.querySelectorAll(".product-img").forEach(img => {
            img.addEventListener("click", function () {
                openModal(this);
            });
        });
    
        window.onclick = function(event) {
            const modal = document.getElementById("imageModal");
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }
    
    function openModal(imgElement) {
        const modal = document.getElementById("imageModal");
        const modalImg = document.getElementById("modalImage");
        const clostBtn = document.querySelector(".close-modal");

        modal.style.display = "flex";
        modalImg.src = imgElement.src;

        if (closeBtn) clostBtn.style.display = "none";
    }
});