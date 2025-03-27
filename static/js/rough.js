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
