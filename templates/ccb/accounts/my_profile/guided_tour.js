{% load i18n base_tags infoblocks %}

$( document ).ready(function() {

    if ($('body').hasClass('is-xs')) return;

    if (sessionStorage.getItem('guided_tour')) return;
    sessionStorage.setItem('guided_tour', 'done');

        console.log("guided_tour ya");

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
            id = "guided_tour_"+id;
            $(this).attr('id', id);
        }

    })

    var $navi = $('.header .menu.tabs .navi ul');
    var $menu = $('<div id="guided_tour_navigation" style="width:31px; height:39px; position:absolute; left:40px; top:40px;"></div>');
    var $search = $('<div id="guided_tour_search" style="width:34px; height:36px; position:absolute; left:110px; top:40px;"></div>');
    $('body').append($menu);
    $('body').append($search);

    $navi.css('-webkit-transition', 'none');
    $navi.css('transition', 'none');

    var cleanUp = function() {
        $menu.remove();
        $search.remove();
        moveNaviTo(0);

        $('a', $navi).css('color', '');
        $navi.css('-webkit-transition', '');
        $navi.css('transition', '');
    }

    var prepareStep = function(step) {

        $('a', $navi).css('color', '');

        var $step = $(step);
        var id = $step.attr('id');

        if (id == 'guided_tour_navigation' || id == 'guided_tour_search') moveNaviTo(0);
        else {

            var $point = $('#'+id);
            $('a', $point).css('color', 'black');

            var position = $point.position();
            var point_width = $point.width();
            var navi_width = $navi.parent().width();

            if (position.left+point_width > navi_width) {
                moveNaviTo("-" + (position.left+point_width - navi_width));
            }
        }
    }

    var moveNaviTo = function(left) {

        var $navi = $('.header .menu.tabs .navi ul');
        $navi.css('left', left+'px');
    }


    var steps = [
        {
            element: document.querySelector('#guided_tour_profile'),
            intro: '{% infoblock "guided_tour_profile" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_portfolio'),
            intro: '{% infoblock "guided_tour_portfolio" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_events'),
            intro: '{% infoblock "guided_tour_events" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_jobs'),
            intro: '{% infoblock "guided_tour_jobs" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_bulletins'),
            intro: '{% infoblock "guided_tour_bulletins" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_blog'),
            intro: '{% infoblock "guided_tour_blog" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_navigation'),
            intro: '{% infoblock "guided_tour_navigation" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_search'),
            intro: '{% infoblock "guided_tour_search" using "blocks/addslashes.html" %}'
        },
        {
            element: document.querySelector('#guided_tour_institutions'),
            intro: '{% infoblock "guided_tour_institutions" using "blocks/addslashes.html" %}'
        },
    ];

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
            doneLabel: "{% trans 'Ok, Understood' %}",
            nextLabel: "{% trans 'Ok, Understood' %}",
            prevLabel: "{% trans 'back' %}",
            skipLabel: "{% trans 'close'  %}",
            hidePrev: true,
            hideNext: true,
            showStepNumbers: false,
            exitOnOverlayClick: false

        });

        intro.onbeforechange(prepareStep);
        intro.onafterchange(prepareStep);
        intro.onexit(cleanUp);
        intro.start();

    }

});
