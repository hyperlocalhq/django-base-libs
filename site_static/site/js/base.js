/* jshint unused:false, eqnull:false */
/* global self: false */
/* global jQuery: false */

function isotope_list() {
    $('.isotope').each(function(){
        var $container = $(this);
        $container.isotope({
            itemSelector : '.item',
            resizable: false, // disable normal resizing
            layoutMode: 'fitRows',
            fitRows: { columnWidth: Math.floor($container.width() / 12) }
        });
    });
}

function lazyload_images() {
    $(".img img:in-viewport").lazyload({
        load : function(element, el_left, settings){
            $(this).closest('.img').addClass('loaded');
        }
    });
}

$(window).bind('scrollstop smartresize', lazyload_images);
$(window).bind('load smartresize', isotope_list);
$(document).ready(lazyload_images);

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
