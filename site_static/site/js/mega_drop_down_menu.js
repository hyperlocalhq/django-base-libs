/* global settings:false */

$(window).load(function() {
    var MAPPER = {
        // de
        'menu-museen': 'mega_museums',
        'menu-ausstellungen': 'mega_exhibitions',
        'menu-veranstaltungen': 'mega_events',
        'menu-fuhrungen': 'mega_workshops',
        'menu-planen-organisieren': 'mega_plan_your_visit',
        // en
        'menu-museums': 'mega_museums',
        'menu-exhibitions': 'mega_exhibitions',
        'menu-events': 'mega_events',
        'menu-guided-tours': 'mega_workshops',
        'menu-plan-your-visit': 'mega_plan_your_visit'
    };
    var loaded = false;
    var $top_nav = $('#top_nav');
    var $mega = $('#mega_drop_down_menu');
    $mega.load('/' + settings.lang + '/helper/menu/', function() {
        loaded = true;
        $top_nav.hover(function() {
            if (window.innerWidth > 767) {
                if ($('.navbar-wrapper').is('.on')) {
                    $mega.css('position', 'fixed');
                } else {
                    $mega.css('position', 'absolute');
                }
                $mega.removeClass('hide');
            }
        }, function() {
            $mega.addClass('hide');
        });
        $('ul.nav>li', $top_nav).hover(function() {
            if (window.innerWidth > 767) {
                $('.mega_drop_down', $mega).addClass('hide');
                var cssClasses = $(this).attr('class') || '';
                var m = cssClasses.match(/\bmenu-\S+/);
                if (m) {
                    $('#' + MAPPER[m[0]]).removeClass('hide');
                }
            }
        });
        /*
        $.each(MAPPER, function(key, value) {
            $('.' + key + ' a').hover(function() {
                $('.mega_drop_down', $mega).addClass('hide');
                $('#' + value).removeClass('hide');
            }, function(){
                // $('#' + value).addClass('hide');
            });
        });
        */
    });
});