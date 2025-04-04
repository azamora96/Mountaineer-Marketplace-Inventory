document.addEventListener("DOMContentLoaded", function () {

    form = document.querySelector('form');
    past_best_by_field = document.getElementById('past_best_by');
    exp_field = document.getElementById('exp');
    best_by_field = document.getElementById('best-by'); 

    function updateExpirationDate() {
        past_best_by = past_best_by_field.value;
        best_by = new Date(best_by_field.value);
        
        let expiration;
  
        switch (past_best_by) {
            case '0-days':
                expiration = new Date(best_by);
                break;
            case '5-days':
                expiration = new Date(best_by);
                expiration.setDate(expiration.getDate() + 5);
                break;
            case '7-days':
                expiration = new Date(best_by);
                expiration.setDate(expiration.getDate() + 7);
                break;
            case '14-days':
                expiration = new Date(best_by);
                expiration.setDate(expiration.getDate() + 14);
                break;
            case '1-month':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 1);
                break;
            case '2-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 2);
                break;
            case '3-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 3);
                break;
            case '6-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 6);
                break;
            case '12-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 12);
                break;
            case '18-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 18);
                break;
            case '24-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 24);
                break;
            case '30-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 30);
                break;
            case '36-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 36);
                break;
            case '48-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 48);
                break;
            case '60-months':
                expiration = new Date(best_by);
                expiration.setMonth(expiration.getMonth() + 60);
                break;
            default:
                expiration = new Date(best_by);
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

    form.addEventListener('submit', function(event) {
        quantityField = document.getElementById('quantity');
        alertNumField = document.getElementById('alertNum');
        
        quantity = parseInt(quantityField.value, 10);
        alertNum = parseInt(alertNumField.value, 10);

        if (alertNum > quantity) {
            event.preventDefault();
            alert('Alert quantity cannot be greater than the total quantity.');
        }
    });
});