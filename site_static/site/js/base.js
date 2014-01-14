function isotope_clear() {
    $('.isotope-clear').each(function(){
        var $container = $(this);
        $container.isotope({

            resizable: false, // disable normal resizing
            layoutMode: 'fitRows',
            fitRows: { columnWidth: $container.width() / 12 }
        });
    }); 
}

$(window).bind('scrollstop load', function() {
    $("img:in-viewport").lazyload({
        load : function(element, el_left, settings){
            $('.isotope').isotope();
            isotope_clear();
        }
    }).addClass("in");
    isotope_clear();
});

// $(window).bind('scrollstop load', function(){
//     $(".img img:in-viewport").lazyload().addClass("in");
// });

$(window).bind('smartresize', function() {
    $('.isotope').isotope();
});

$(document).ready(function() {
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

    $('#to-top').click(function() {
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

    $("select").not('[name*="__prefix__"]').not('[sb]').selectbox();

    $(".navbar-wrapper").headroom({
        // vertical offset in px before element is first unpinned
        offset : 400,
        // scroll tolerance in px before state changes
        tolerance : 0
    });
    // $('.panel-collapse').collapse('show');
});

// ADD crsftoken TO AJAX CALLS
(function() {
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})();

if ($.browser.msie) {
    $('html').addClass('msie');
}
