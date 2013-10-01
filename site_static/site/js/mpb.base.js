
var django = {
  jQuery: jQuery
};

$(window).bind('scrollstop load', function(e){
  $(".img-detail img:in-viewport").lazyload({
    load : function(element, el_left, settings){
        $('.grid').isotope();
    }
  }).addClass("in");
  console.log(1);
});

$(window).bind('load', function(e){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(window).bind('smartresize', function(e){
  $('.grid').isotope();
  console.log("window resize");
});

$(window).bind('scrollstop', function(e){
  $(".img img:in-viewport").lazyload().addClass("in");
  console.log(3);
});

$(document).ready(function(){
  // $(".img img:in-viewport").lazyload().addClass("in");

  $("a[href^='http://']").attr("target","_blank");

  if ($('#cms_toolbar').length) { // cms toolbar fix
    if ($('body').css('margin-top') == "-43px") {
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
    } else {
      $('#to-top').removeClass('on');
    }
  });

  $("select").selectbox();
  // $('.panel-collapse').collapse('show');
});
