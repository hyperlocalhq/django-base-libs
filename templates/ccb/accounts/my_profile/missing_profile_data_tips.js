{% load i18n base_tags infoblocks %}

$( document ).ready(function() {

    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    if (getCookie('dont_show_tips_again') == 1) return;

    if (is_institution) {
        if (sessionStorage.getItem('missing_profile_data_tips_institution')) return;
        sessionStorage.setItem('missing_profile_data_tips_institution', 'done');
    } else {
        if (sessionStorage.getItem('missing_profile_data_tips_person')) return;
        sessionStorage.setItem('missing_profile_data_tips_person', 'done');
    }

    window.setTimeout(doMissingProfileDataTips, 1000);



});


function doMissingProfileDataTips() {

    $('.header .menu.tabs .navi li').each(function(index) {

        var id = "";
        switch (index) {
            case 1:
                id = "profile";
                break;
            case 2:
                id = "portfolio";
                break;
            case 3:
                id = "events";
                break;
            case 4:
                id = "jobs";
                break;
            case 5:
                id = "bulletins";
                break;
            case 6:
                id = "blog";
                break;
            case 7:
                id = "institutions";
                break;
            default:
                id = "";
        }

        if (id != "") {
            id = "tip_"+id;
            $(this).attr('id', id);
        }

    })

    $('.header .menu.tabs .navi nav').attr('id', 'navi_wrapper');
    var $navi = $('.header .menu.tabs .navi ul');

    var is_xs = ($('body').hasClass('is-xs'));
    var $add_buttons = (is_xs) ? $('.header .profile .buttons a') : $('.container .profile-image a.button');
    var $add_buttons_wrapper = $('<div id="tip_no_entry"></div>');
    $add_buttons.parent().append($add_buttons_wrapper);
    $add_buttons_wrapper.append($add_buttons);


    var image_id = (is_xs) ? '#profile-image-header' : '#profile-image-sidebar';


    var cleanUp = function() {
        moveNaviTo(0);
        $add_buttons_wrapper.parent().append($add_buttons);
        $add_buttons_wrapper.remove();
    }

    var prepareStep = function(step) {

        var $step = $(step);
        var id = $step.attr('id');

        moveNaviTo(0);
    }

    var moveNaviTo = function(left) {

        var $navi = $('.header .menu.tabs .navi ul');
        $navi.css('left', left+'px');
    }

    var createDontShowTipsAgain = function() {

        var $tooltip = $('.introjs-tooltip');
        $('.introjs-dontshowagain', $tooltip).remove();

        var $link = $('<a class="introjs-button introjs-dontshowagain" role="button" tabindex="0">{% trans "Do not show these tips again" %}</a>');

        $link.click(function() {

            var d = new Date();
            d.setTime(d.getTime() + (10*365*24*60*60*1000));
            var expires = "expires="+ d.toUTCString();
            document.cookie = "dont_show_tips_again=1;" + expires + ";path=/";

            intro.exit(true);
        });

        $tooltip.append($link);
    }


    var steps = [];
    if (show_tip_no_profile_image) steps.push(
        {
            position: (is_xs) ? "bottom" : "right",
            element: document.querySelector(image_id),
            intro: '{% infoblock "tip_no_profile_image" using "blocks/addslashes.html" %}'
        }
    );
    if (show_tip_no_creative_sector) steps.push(
        {
            position: (is_xs) ? "bottom" : "bottom",
            element: document.querySelector('#tip_no_creative_sector'),
            intro: '{% infoblock "tip_no_creative_sector" using "blocks/addslashes.html" %}'
        }
    );

    for (var i=0; i<steps.length; i++) {
        if (steps[i].intro == '') {
            steps.splice(i,1);
            i--;
        }
    }


    if (steps.length) {

        var intro = introJs();

        intro.setOptions({

            steps: steps,
            doneLabel: "{% trans 'Ok, got it' %}",
            nextLabel: "{% trans 'Ok, got it' %}",
            prevLabel: "{% trans 'back' %}",
            skipLabel: "{% trans 'close'  %}",
            hidePrev: true,
            hideNext: true,
            showBullets: !(!(steps.length > 1)),
            showStepNumbers: false,
            exitOnOverlayClick: true

        });

        intro.onbeforechange(prepareStep);
        intro.onafterchange(createDontShowTipsAgain);
        intro.onexit(cleanUp);
        intro.start();

    }

}
