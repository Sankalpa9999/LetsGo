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




// $(document).ready(function() {

//     // Add to cart functionality
//     $(".add-to-cart-btn").on("click", function(e) {
//         e.preventDefault();
//         const button = $(this);
//         const parent = button.closest(".featured__item, .product-container, .product-detail-container");

//         // Get product details
//         const product_title = parent.find(".product-title, .product-name").first().text().trim() || "Unknown";
//         let product_price = parent.find(".discount-price, .current-product-price, .price").first().text().trim() || "0";
//         const product_id = button.data("product-id");

//         // Clean price
//         product_price = product_price.replace(/[^0-9.]/g, "");

//         // Get image
//         let product_image = parent.find(".featured__item__pic, .product-image").css("background-image");
//         product_image = product_image && product_image !== "none" 
//             ? product_image.replace(/^url\(["']?/, "").replace(/["']?\)$/, "")
//             : parent.find("img").attr("src") || "";

//         if (!product_id) {
//             alert("Product ID missing!");
//             return;
//         }

//         // Show loading state
//         button.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i>');

//         $.ajax({
//             url: "/add-to-cart/",
//             type: "POST",
//             data: {
//                 id: product_id,
//                 title: product_title,
//                 price: product_price,
//                 image: product_image,
//                 csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
//             },
//             dataType: "json",
//             success: function(response) {
//                 button.html("✅").prop('disabled', true);
//                 $(".cart-count").text(response.totalcartitems || 0);
//                 showToast('Product added to cart!');
//             },
//             error: function(xhr) {
//                 button.prop('disabled', false).html('Add to Cart');
//                 try {
//                     const response = JSON.parse(xhr.responseText);
//                     alert(response.error || "Error adding to cart");
//                 } catch {
//                     alert("Network error. Please try again.");
//                 }
//             }
//         });
//     });

//     // Handle checkbox changes with AJAX
//     $(document).on('change', '.item-checkbox', function() {
//         const checkbox = $(this);
//         const productId = checkbox.val();
//         const isChecked = checkbox.is(':checked');
        
//         // Show loading state
//         checkbox.prop('disabled', true);
        
//         $.ajax({
//             url: "/update-cart/",
//             type: "POST",
//             data: {
//                 product_id: productId,
//                 action: "toggle_select",
//                 csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
//             },
//             dataType: "json",
//             success: function(response) {
//                 if (response.success) {
//                     updateCartTotals(response);
//                 } else {
//                     alert(response.error || "Failed to update selection");
//                     checkbox.prop('checked', !isChecked);
//                 }
//                 checkbox.prop('disabled', false);
//             },
//             error: function(xhr) {
//                 try {
//                     const response = JSON.parse(xhr.responseText);
//                     alert(response.error || "Error updating selection");
//                 } catch {
//                     alert("Network error. Please try again.");
//                 }
//                 checkbox.prop('checked', !isChecked).prop('disabled', false);
//             }
//         });
//     });

//     // Function to update cart totals
//     function updateCartTotals(data) {
//         if (data.subtotal) {
//             $('.cart-subtotal').text('$' + data.subtotal);
//         }
//         if (data.total) {
//             $('.cart-total').text('$' + data.total);
//         }
//         if (data.selected_count !== undefined) {
//             $('.selected-count').text(data.selected_count);
//         }
//         if (data.has_selected_items !== undefined) {
//             const btn = $('.btn-proceed-to-book');
//             data.has_selected_items ? btn.removeClass('disabled') : btn.addClass('disabled');
//         }
//     }

//     // Helper function for notifications
//     function showToast(message) {
//         const toast = $(`<div class="toast align-items-center text-white bg-success border-0" role="alert">
//                            <div class="d-flex">
//                              <div class="toast-body">${message}</div>
//                              <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
//                            </div>
//                          </div>`);
//         $('.toast-container').append(toast);
//         new bootstrap.Toast(toast[0]).show();
//         setTimeout(() => toast.remove(), 3000);
//     }
// });


function changeImage(element) {
    document.getElementById('mainProductImage').src = element.src;
}

// Debug function to show what's being added to rentlist
document.querySelector('.add-to-cart-btn').addEventListener('click', function(e) {
    const productId = this.getAttribute('data-product-id');
    console.log("Adding to rentlist:", {
        id: productId,
        title: "{{ p.title }}",
        vendor: "{{ p.vendor.title }}",
        image: "{{ p.image.url }}"
    });
});