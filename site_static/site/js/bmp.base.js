
$(function() {
  $("a[href^='http://']").attr("target","_blank");

  if ($('#cms_toolbar').length) { // cms toolbar fix
    if ($('body').css('margin-top') == "-43px") {
      $('body').css('margin-top', 0);
    }
  }

	if ($("[data-toggle=tooltip]").length) {
    $("[data-toggle=tooltip]").tooltip({});
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


	$(document).ready(function(){
	  $("select").selectbox()
	});
});

var django = {
  jQuery: jQuery
};

$(window).load(function() {
  $('.panel-collapse').collapse('show');
});
