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
    $('.isotope-masonry').each(function(){
        var $container = $(this);
        $container.isotope({
            itemSelector : '.item',
            resizable: false, // disable normal resizing
            layoutMode: 'masonry',
            masonry: { columnWidth: Math.floor($container.width() / 12) }
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

var currentScrollPosition = 0;

$(document).scroll(function(){
    currentScrollPosition = $(this).scrollTop();
});

$(document).ready(function() {
    $('.navbar-toggle').on('click', function() {
        $('body').toggleClass('nav-expanded');
    });

    $("input").focus(function(e){
        e.preventDefault();
        e.stopPropagation();

        setTimeout(function() {
            $(document).scrollTop(currentScrollPosition);
        }, 1);

        setTimeout(function() {
            $(document).scrollTop(currentScrollPosition);
        }, 50);

        setTimeout(function () {
            $(document).scrollTop(currentScrollPosition);
        }, 100);

        setTimeout(function() {
            $(document).scrollTop(currentScrollPosition);
        }, 150);
    });
    currentScrollPosition = $(this).scrollTop();

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

    $("select").not('[name*="__prefix__"]').not('[sb]').not('[multiple]').selectbox();
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

$.postFix = function(url, data, success, data_type) {
    $.ajaxFix(url, 'post', data, success, data_type);
}

$.getFix = function(url, data, success, data_type) {
    $.ajaxFix(url, 'get', data, success, data_type);
}

$.ajaxFix = function(url, method, data, success, data_type) {

    $('#ajax_call_form').remove();
    $('#ajax_call_frame').remove();

    if (typeof method == "undefined" || !method) method="get";

    var $frame = $('<iframe id="ajax_call_frame" name="ajax_call_frame" src="#" style="display:none"></iframe>')
    var $form = $('<form id="ajax_call_form" method="'+method+'" action="'+url+'" target="ajax_call_frame"></form>');

    $('body').append($frame).append($form);

    var form = document.getElementById('ajax_call_form');
    if (typeof data != "undefined") {
        for (var key in data) {
            form[key] = data[key];
        }
    }
    form.submit();


    /*var query = "";
    if (typeof data != "undefined") {
        for (var key in data) {
            query += key+"="+encodeURIComponent(data[key]);
        }
    }
    if (query != "") query = "?"+query;

    var $frame = $('<iframe src="'+(url+query)+'" style="display:none"></iframe>');

    $('body').append($frame);*/
}
