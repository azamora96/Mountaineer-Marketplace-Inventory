document.addEventListener("DOMContentLoaded", function () {   
  // FOR UPDATING EXP DATE FUNCTIONALITY:
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
})   