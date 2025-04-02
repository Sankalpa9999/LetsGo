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








// $(document).ready(function () {
//     $(".add-to-cart-btn").on("click", function () {
//         let this_val = $(this);
//         let parent = this_val.closest(".product-container"); // Find closest product container

//         let product_title = parent.find(".product-title").text().trim(); 
//         let product_price = parent.find(".current-product-price").text().trim(); 
//         let product_id = this_val.data("product-id"); // Fetch product ID properly

//         console.log("Title:", product_title);
//         console.log("Price:", product_price);
//         console.log("ID:", product_id);

//         $.ajax({
//             url: "/add-to-cart/",
//             type: "POST",
//             data: {
//                 id: product_id,
//                 title: product_title,
//                 price: product_price,
//                 csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
//             },
//             dataType: "json",
//             beforeSend: function () {
//                 console.log("Adding to cart...");
//             },
//             success: function (response) {
//                 this_val.html("Item added to cart");
//                 console.log("Cart updated:", response);
//                 $(".cart.item-count").text(response.totalcartitems);
//             },
//             error: function (error) {
//                 alert("Error adding to cart.");
//                 console.log(error);
//             }
//         });
//     });
// });

$(document).ready(function () {
    $(".add-to-cart-btn").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior

        let this_val = $(this);
        let parent = this_val.closest(".product-container"); // Adjust if necessary

        let product_title = parent.find(".product-title").text().trim(); 
        let product_price = parent.find(".current-product-price").text().trim(); 
        let product_id = this_val.data("product-id");

        $.ajax({
            url: "/add-to-cart/",
            type: "POST",
            data: {
                id: product_id,
                title: product_title || "Unknown",
                price: product_price || "0",
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Adding to cart...");
            },
            success: function (response) {
                this_val.html("✅").prop("disabled", true);
                console.log("Cart updated:", response);

                // ✅ Automatically update cart count without refreshing
                $(".cart-count").text(response.totalcartitems);
            },
            error: function (error) {
                alert("Error adding to cart.");
                console.log(error);
            }
        });
    });
});




