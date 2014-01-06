
var django = {
  jQuery: jQuery
};

$(window).bind('scrollstop load', function(e){
  $(".img-detail img:in-viewport").lazyload({
    load : function(element, el_left, settings){
        $('.grid').isotope();
    }
  }).addClass("in");
});

$(window).bind('load', function(e){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(window).bind('smartresize', function(e){
  $('.grid').isotope();
});

$(window).bind('scrollstop', function(e){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(document).ready(function(){
  // $(".img img:in-viewport").lazyload().addClass("in");

  $("a[href^='http://']").attr("target","_blank");

  if ($('#cms_toolbar').length) { // cms toolbar fix
    if ($('body').css('margin-top') == "-42px") {
      $('body').css('margin-top', 0);
    }
  }

	if ($("[data-toggle=tooltip]").length) {
    $("[data-toggle=tooltip]").tooltip({
    });
  }

  $('#to-top').click(function(e){
    $('html, body').animate({scrollTop:0}, 'slow');
    return false;
  });

  $(window).scroll(function() {
    if ($('body').offset().top < $(window).scrollTop()) {
      $('#to-top').addClass('on');
      $('.navbar-wrapper').addClass('on');

    } else {
      $('#to-top').removeClass('on');
      $('.navbar-wrapper').removeClass('on');
    }
  });

  $("select").selectbox();
  // $('.panel-collapse').collapse('show');


  $(function(){
        var lastScrollTop = 0, delta = 15;
        $(window).scroll(function(event){
           var st = $(this).scrollTop();

           if(Math.abs(lastScrollTop - st) <= delta)
              return;

           if (st > lastScrollTop){
               // Scroll Down
                $(".navbar-wrapper").delay(10).queue(function() {
                    $(this).removeClass("nav-visible").addClass("nav-hidden");
                    $(this).dequeue();
                });

           } else {
              // Scroll Up
                $('.navbar-wrapper').delay(10).queue(function() {
                    $(this).removeClass("nav-hidden").addClass("nav-visible");
                    $(this).dequeue();
                });
           }
           lastScrollTop = st;
        });
    });
});
