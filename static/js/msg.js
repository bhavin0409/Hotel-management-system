document.addEventListener('DOMContentLoaded', function() {
    // Find the error alert element
    var errorAlert = document.getElementById('error-alert');
   
    // Check if the error alert exists
    if (errorAlert) {
        // Remove the error alert after 7 seconds
        setTimeout(function() {
            errorAlert.remove();
        }, 7000); // 7 seconds
    }
});