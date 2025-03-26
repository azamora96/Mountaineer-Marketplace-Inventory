document.addEventListener("DOMContentLoaded", function () {
    QuantityButtons();

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
                //These lines here are to stop the page from refreshing
                event.preventDefault(); 
                event.stopPropagation();  

                let quantitySpan = this.parentElement.querySelector(".quantity");
                let id = this.getAttribute("data-id");
                let action = this.classList.contains("minus") ? "minus" : "plus"; 

                //Had to format it with this async so that the POST request works properly
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
            `;
            tbody.appendChild(row);
        });

        //Have to recreate buttons so that quantity buttons work properly
        QuantityButtons();
    }
});
