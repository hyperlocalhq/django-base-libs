var django = {
  jQuery: jQuery
};

$(window).bind('scrollstop load', function(){
  $(".img-detail img:in-viewport").lazyload({
    load : function(element, el_left, settings){
        $('.grid').isotope();
    }
  }).addClass("in");
});

$(window).bind('load', function(){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(window).bind('smartresize', function(){
  $('.grid').isotope();
});

$(window).bind('scrollstop', function(){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(document).ready(function(){
  // $(".img img:in-viewport").lazyload().addClass("in");

  $("a[href^='http://']").attr("target","_blank");

  if ($('#cms_toolbar').length) { // cms toolbar fix
    if ($('body').css('margin-top') === "-42px") {
      $('body').css('margin-top', 0);
    }
  }

	if ($("[data-toggle=tooltip]").length) {
    $("[data-toggle=tooltip]").tooltip({
    });
  }

  $('#to-top').click(function(){
    $('html, body').animate({scrollTop:0}, 'slow');
    return false;
  });

  $(window).scroll(function() {
    if ($('body').offset().top < $(window).scrollTop()) {
      $('#to-top').addClass('on');

    } else {
      $('#to-top').removeClass('on');
    }
  });

  $("select").selectbox();
  // $('.panel-collapse').collapse('show');
});
