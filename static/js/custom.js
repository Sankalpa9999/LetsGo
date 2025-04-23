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
                $("#toggle-review-form").hide();
        
                // Append the new review dynamically with proper star formatting
                $(".reviews-list").prepend(`
                    <div class="review-item border-bottom pb-4 mb-4">
                        <div class="d-flex justify-content-between">
                            <h5 class="fw-bold">${response.user}</h5>
                            <p class="text-muted">Just now</p>
                        </div>
                        <div class="review-stars">${response.stars}</div>
                        <p class="review-text">${response.review}</p>
                    </div>
                `);
                
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





function changeImage(element) {
    document.getElementById('mainProductImage').src = element.src;
}



document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".rent-form").forEach((form) => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
  
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
        const url = form.action;
  
        fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((res) => res.json())
          .then((data) => {
            showToast(data.message, data.status);
          })
          .catch(() => {
            showToast("Something went wrong!", "error");
          });
      });
    });
  

    function showToast(message, status) {
      const toast = document.createElement("div");
      toast.innerText = message;
  
      toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${
          status === "success" ? "#28a745" : status === "info" ? "#007bff" : "#dc3545"
        };
        color: white;
        padding: 12px 20px;
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.4s ease;
      `;
  
      document.body.appendChild(toast);
      setTimeout(() => (toast.style.opacity = "1"), 100);
      setTimeout(() => (toast.style.opacity = "0"), 3500);
      setTimeout(() => toast.remove(), 4000);
    }
  });




// ✅ Unified Toast Function (Place this only ONCE)
function showToast(message, status) {
  const toast = document.createElement("div");
  toast.innerText = message;

  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${
      status === "success"
        ? "#28a745"   // green
        : status === "info"
        ? "#0dcaf0"   // sky blue
        : "#dc3545"   // red
    };
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.4s ease;
  `;

  document.body.appendChild(toast);
  setTimeout(() => (toast.style.opacity = "1"), 100);
  setTimeout(() => (toast.style.opacity = "0"), 3500);
  setTimeout(() => toast.remove(), 4000);
}

// ✅ Wishlist Button Handler
$(document).on("click", ".add-to-wishlist", function () {
  let product_id = $(this).attr("data-product-item");
  let this_val = $(this);

  console.log("Product ID:", product_id);
  if (!product_id) {
    showToast("Product ID is missing!", "error");
    return;
  }


  $.ajax({
    url: "/add-to-wishlist/",
    data: {
      id: product_id,
    },
    dataType: "json",
    beforeSend: function () {
      console.log("Adding to wishlist...");
    },
    success: function (response) {
      if (response.bool === true) {
        showToast(response.message, response.status); // ← use dynamic status
        this_val.addClass("in-wishlist");
        this_val.html("💖"); // Optional: Change button content
      } else {
        showToast("Something went wrong.", "error");
      }
    },
    error: function () {
      showToast("Failed to add to wishlist. Please try again.", "error");
    },
  });
});


