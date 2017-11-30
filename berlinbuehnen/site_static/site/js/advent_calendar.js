/**
* @Author: Daniel Lehmann
* @Date:   2017/11/29
* @Email:  code@dreammedia.info
* @Last modified by:   Daniel Lehmann
* @Last modified time: 2017/11/30
* @copyright Daniel Lehmann (code@dreammedia.info)
*/

$(document).ready(function() {

    function AdventCalendar() {

        var me = this;
        me.$present = $('.advent-calendar .present');
        me.$past = $('.advent-calendar .past');
        me.$gift_door = $('img', me.$present).not('.gift-image');
        me.$layers = $('.advent-calendar .gift');
        me.$body = $('body');

        me.$present.click(function() {me.openDoor($(this));});
        $('.advent-calendar .gift-close').click(function() {me.closeLayer();});

        me.$past.click(function() {

            if (window.ga) {
                window.ga('send', {
                    hitType: 'event',
                    eventCategory: 'Advent Calendar',
                    eventAction: 'reopen',
                    eventLabel: 'Past Day'
                });
            }

            me.openLayer($(this));
        });
    }

    AdventCalendar.prototype.openDoor = function($door) {

        var me = this;

        if (me.$gift_door.hasClass('opening')) return;

        var now = new Date();
        var formated_date = now.getDate()+"."+(now.getMonth()+1)+"."+now.getFullYear();

        if (me.$gift_door.hasClass('open')) {

            me.openLayer($door);

            if (window.ga) {
                window.ga('send', {
                    hitType: 'event',
                    eventCategory: 'Advent Calendar',
                    eventAction: 'reopen',
                    eventLabel: 'Day ' + formated_date
                });
            }

        } else {

            me.$gift_door.addClass('opening');
            $door.next().addClass("opening");
            //me.$body.addClass("gift-layer");
            window.setTimeout(function() {me.openLayer($door);}, 1600);

            if (window.ga) {
                window.ga('send', {
                    hitType: 'event',
                    eventCategory: 'Advent Calendar',
                    eventAction: 'open',
                    eventLabel: 'Day ' + formated_date
                });
            }

        }
    }

    AdventCalendar.prototype.openLayer = function($door) {

        var me = this;

        if (me.$gift_door.hasClass('opening')) {
            me.$gift_door.addClass('open');
            me.$gift_door.removeClass('opening')
        }

        $door.next().addClass("open");
        $door.next().removeClass("opening");
        me.$body.addClass("gift-layer");
    }

    AdventCalendar.prototype.closeLayer = function() {

        var me = this;

        me.$layers.removeClass("open");
        me.$body.removeClass("gift-layer");
    }

    new AdventCalendar();
});
