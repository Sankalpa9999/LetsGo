console.log('Hello');

// Function to show notifications
function showNotification(message, type) {
    // Remove any existing notifications first
    $('.review-notification').remove();
    
    // Create notification element
    const notification = $(`
        <div class="alert alert-${type} alert-dismissible fade show review-notification" role="alert" 
             style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `);
    
    // Append to body
    $('body').append(notification);
}

// Toggle review form visibility
// $("#toggle-review-form").click(function() {
//     $("#review-form").toggle();
// });

// Form submission handler
$("#review-form").submit(function(e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function(response) {
            if (response.bool) {
                showNotification('Review saved successfully!', 'success');
                
                // Hide the "Add Review" button immediately
                $("#toggle-review-form").hide();
                
                // Refresh the page after 1.5 seconds
                setTimeout(function() {
                    location.reload();
                }, 1500);
            }
        },
        error: function(xhr) {
            let errorMessage = 'Error saving review';
            if (xhr.status === 403) {
                errorMessage = 'Please login to submit a review';
            }
            showNotification(errorMessage, 'error');
        }
    });
});

// Notification function
function showNotification(message, type) {
    $('.review-notification').remove();
    $('body').append(`
        <div class="alert alert-${type} alert-dismissible fade show review-notification" 
             style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
}