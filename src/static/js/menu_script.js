// Main menu Click
$("#main_menu_link").click(function() {
    $(".main_menu").css({
        'display': 'flex'
    });
    $(".exclusive_menu").css({
        'display': 'none'
    });
    $(".dessert_menu").css({
        'display': 'none'
    });
    $(".bar_menu").css({
        'display': 'none'
    });

    // Nav Links Styles
    $("#main_menu_link").addClass("active_link");
    $("#exclusive_link").removeClass("active_link");
    $("#dessert_link").removeClass("active_link");
    $("#bar_menu_link").removeClass("active_link");
});

// Exclusive menu Click
$("#exclusive_link").click(function() {
    $(".exclusive_menu").css({
        'display': 'flex'
    });
    $(".main_menu").css({
        'display': 'none'
    });
    $(".dessert_menu").css({
        'display': 'none'
    });
    $(".bar_menu").css({
        'display': 'none'
    });

    // Nav Links Styles
    $("#exclusive_link").addClass("active_link");
    $("#main_menu_link").removeClass("active_link");
    $("#dessert_link").removeClass("active_link");
    $("#bar_menu_link").removeClass("active_link");
});

// Dessert menu Click
$("#dessert_link").click(function() {
    $(".dessert_menu").css({
        'display': 'flex'
    });
    $(".exclusive_menu").css({
        'display': 'none'
    });
    $(".main_menu").css({
        'display': 'none'
    });
    $(".bar_menu").css({
        'display': 'none'
    });

    // Nav Links Styles
    $("#dessert_link").addClass("active_link");
    $("#main_menu_link").removeClass("active_link");
    $("#exclusive_link").removeClass("active_link");
    $("#bar_menu_link").removeClass("active_link");
});

// Bar menu Click
$("#bar_menu_link").click(function() {
    $(".bar_menu").css({
        'display': 'flex'
    });
    $(".exclusive_menu").css({
        'display': 'none'
    });
    $(".main_menu").css({
        'display': 'none'
    });
    $(".dessert_menu").css({
        'display': 'none'
    });

    // Nav Links Styles
    $("#bar_menu_link").addClass("active_link");
    $("#main_menu_link").removeClass("active_link");
    $("#exclusive_link").removeClass("active_link");
    $("#dessert_link").removeClass("active_link");
});