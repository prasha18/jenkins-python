$(document).ready(function () {
    // Toggle mobile menu
    $('#menuToggle').click(function () {
        $('.sticky-navbar').toggleClass('menu-open');
        $('#navbarMenu').toggleClass('open');
        $('body').toggleClass('overflow-hidden');
    });

    // Dropdown toggle on click (for mobile)
    $('.navbar-menu > li > a').click(function (e) {
        const $parentLi = $(this).parent();
        if ($(window).width() <= 768) {
            e.preventDefault();
            $('.navbar-menu li').not($parentLi).removeClass('dropdown-open');
            $parentLi.toggleClass('dropdown-open');
        }
    });
});
