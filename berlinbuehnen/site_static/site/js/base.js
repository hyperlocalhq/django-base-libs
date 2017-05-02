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


    var current_width_sniffer = 'is-nothing';
    var widthSniffer = function() {

        var new_width_sniffer = false;
        $('.width-sniffer').each(function() {

            var $this = $(this);
            if ($this.css('display') == 'block') {

                if ($this.hasClass('visible-xs')) {
                    new_width_sniffer = 'is-xs';
                } else if ($this.hasClass('visible-sm')) {
                    new_width_sniffer = 'is-sm';
                } else if ($this.hasClass('visible-md')) {
                    new_width_sniffer = 'is-md';
                } else if ($this.hasClass('visible-lg')) {
                    new_width_sniffer = 'is-lg';
                }

                return false;
            }
        });

        if (new_width_sniffer && new_width_sniffer != current_width_sniffer) {
            var $body = $('body').removeClass(current_width_sniffer);
            current_width_sniffer = new_width_sniffer;
            $body.addClass(new_width_sniffer);
        }
    }
    $(window).resize(widthSniffer);
    widthSniffer();


    var cmsSniffer = function() {

        var search = location.search.substr(1);
        console.log(search);
        search = search.split("&");
        for (var i=0; i<search.length; i++) {
            var item = search[i].split("=");
            if (item[0] == "edit") break;
        }
        if (i != search.length) $('body').addClass('cms-edit');
    }
    cmsSniffer();
});

// ADD crsftoken TO AJAX CALLS
(function() {
    var csrftoken = "";
    if (typeof $.cookie != "undefined" ) csrftoken = $.cookie('csrftoken');
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


window.tooltipAdjustments = function() {

    var tooltipFix = function(event) {

        var $element = $(event.target);
        var $tooltip = $element.next('.tooltip');

        var getValue = function(data) {

            if (typeof data == "undefined") return 0;

            var default_value = 0;
            var values = data.split(';');
            for (var i=0, length=values.length; i<length; i++) {
                values[i] = values[i].split(',');
                if (values[i].length == 1 && default_value == 0) default_value = parseInt(values[i][0]);
            }

            if (length == 0) return 0;

            for (var i=0, length=values.length; i<length; i++) {
                if (values[i].length == 2) {
                    if ($element.parents(values[i][1]).length) return parseInt(values[i][0]);
                }
            }

            return default_value;
        }

        var clear = function(event) {

            var $element = $(event.target);
            var $tooltip = $element.next('.tooltip');

            $element.off('hidden.bs.tooltip');

            $tooltip.css("min-width", "");
        }

        if ($tooltip.length) {

            var top_offset = getValue($element.attr('data-tooltip-top'));
            var left_offset = getValue($element.attr('data-tooltip-left'));
            var top_absolute = getValue($element.attr('data-tooltip-top-abs'));
            var bottom_absolute = getValue($element.attr('data-tooltip-bottom-abs'));
            var left_absolute = getValue($element.attr('data-tooltip-left-abs'));
            var right_absolute = getValue($element.attr('data-tooltip-right-abs'));

            var min_width = getValue($element.attr('data-tooltip-width'));
            if (min_width < 0) min_width = 0;

            var height = $tooltip.height();

            if (top_offset != 0) {
                var top = parseInt($tooltip.css("top"));
                $tooltip.css("top", (top + top_offset) + "px");
            } else if (top_absolute != 0) {
                $tooltip.css("top", top_absolute + "px");
            } else if (bottom_absolute != 0) {
                $tooltip.css("top", "");
                $tooltip.css("bottom", bottom_absolute + "px");
            }

            if (left_offset != 0) {
                var left = parseInt($tooltip.css("left"));
                $tooltip.css("left", (left + left_offset) + "px");
            } else if (left_absolute != 0) {
                $tooltip.css("left", left_absolute + "px");
            } else if (right_absolute != 0) {
                $tooltip.css("left", "");
                $tooltip.css("right", right_absolute + "px");
            }


            if ($tooltip.width() < min_width) {
                var width_offset = Math.round(($tooltip.width() - min_width) / 2);
                $tooltip.css("min-width", min_width + "px");
                var left = parseInt($tooltip.css("left"));
                $tooltip.css("left", (left + width_offset) + "px");
            }

            var height_offset = height - $tooltip.height();
            if (height_offset != 0 && (top_offset != 0 || left_offset != 0) ) {
                var top = parseInt($tooltip.css("top"));
                $tooltip.css("top", (top + height_offset) + "px");
            }

            $element.on('hidden.bs.tooltip',  clear);
        }
    }

    $('[data-toggle="tooltip"]').off('shown.bs.tooltip').on('shown.bs.tooltip', tooltipFix);
}

$(document).ready(function() {
    window.tooltipAdjustments();
});
