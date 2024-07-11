// MOBILE HEADER MENU WITH HAMBURGER MENU

function menuBtnFunction(menuBtn) {
    menuBtn.classList.toggle("active");
}

let menuOpen = 0;

$('.menu-btn-6').click(function() {
  if(menuOpen == 0) {
    menuOpen = 1;
    $(".header_menu").css({
        "visibility": "visible",
        "max-height": "100vh",
        "opacity": "1"
    });
  } else if(menuOpen == 1) {
    menuOpen = 0;
    $(".header_menu").css({
        "visibility": "hidden",
        "max-height":"0",
        "opacity": "0"
    });
  }
});


// Language BTN and Language Menu

let langMenuOpen = 0;

$('.lang_btn p').click(function() {
  if(langMenuOpen == 0) {
    langMenuOpen = 1;
    $(".lang_menu_sel").css({
        "visibility": "visible",
        "max-height": "100vh",
        "opacity": "1"
    });
    $(".lang_btn img").css({
        "rotate":"180deg"
    });
    $(".lang_btn img").css({
        "rotate":"180deg"
    });
  } else if(langMenuOpen == 1) {
    langMenuOpen = 0;
    $(".lang_menu_sel").css({
        "visibility": "hidden",
        "max-height":"0",
        "opacity": "0"
    });
    $(".lang_btn img").css({
        "rotate":"0deg"
    });
  }
});

$('.lang_btn img').click(function() {
  if(langMenuOpen == 0) {
    langMenuOpen = 1;
    $(".lang_menu_sel").css({
        "visibility": "visible",
        "max-height": "100vh",
        "opacity": "1"
    });
    $(".lang_btn img").css({
        "rotate":"180deg"
    });
    $(".lang_btn img").css({
        "rotate":"180deg"
    });
  } else if(langMenuOpen == 1) {
    langMenuOpen = 0;
    $(".lang_menu_sel").css({
        "visibility": "hidden",
        "max-height":"0",
        "opacity": "0"
    });
    $(".lang_btn img").css({
        "rotate":"0deg"
    });
  }
});

// Plavnoye poyavleniye

// let x = document.querySelector(".plav")
// setTimeout(function(){
//   x.style.animation = "fade 3s";
//   x.style.opacity = "1"
// });

// $(document).ready(function(){
//   $('body').toggle("show");
// });

$(window).ready(function(){
  $("body").toggleClass("page_show");
});