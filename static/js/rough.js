console.log('Hello from custom.js');



    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });

$("#commentform").submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function (response) {
            console.log("Comment saved");
        }
    });
});


// JavaScript to toggle form visibility
document.getElementById('toggle-review-form').addEventListener('click', function () {
    const reviewForm = document.getElementById('review-form');
    // Toggle display style between none and block
    reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
});




// add to cart

$("#add-to-cart-btn").on("click",function() {
    let product_title = $(".product-title").val()
    let product_price = $(".current-product-price").text()
    let product_id = $(".product-id").val()
    let this_val = $(this)

    console.log("Title: ", product_title);
    console.log("Price: ", product_price);
    console.log("ID: ", product_id);
    console.log("current Element:", this_val);



    $.ajax({
        url: "/add-to-cart/",  // Update with your cart endpoint
        type: "POST",
        data: {
            id: product_id,
            title: product_title,
            price: product_price,
            csrfmiddlewaretoken: "{{ csrf_token }}",
        },
        dataType: "json",
        beforesend: function () {
            console.log("Adding to cart...");
        },
        success: function (response) {
            this_val.html("Item added to cart");
            console.log("Added to cart successfully");
            // alert("Added to cart successfully!");
        },
        error: function (error) {
            alert("Error adding to cart.");
            console.log(error);
        }
    });
})



// $(document).ready(function () {
//     $(".add-to-cart-btn").on("click", function (e) {
//         e.preventDefault(); // Prevent default anchor behavior (for index.html)

//         let this_val = $(this);
//         let parent = this_val.closest(".product-container"); // Adjust this if needed

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
//                 title: product_title || "Unknown", // Fallback to avoid errors
//                 price: product_price || "0",
//                 csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
//             },
//             dataType: "json",
//             beforeSend: function () {
//                 console.log("Adding to cart...");
//             },
//             success: function (response) {
//                 this_val.html("✅").prop("disabled", true);
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
