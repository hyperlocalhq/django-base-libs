/**
* @Author: Daniel Lehmann
* @Date:   2017/11/29
* @Email:  code@dreammedia.info
* @Last modified by:   Daniel Lehmann
* @Last modified time: 2017/11/29
* @copyright Daniel Lehmann (code@dreammedia.info)
*/

$(document).ready(function() {

    function AdventCalendar() {

        var me = this;
        me.$present = $('.advent-calendar .present');
        me.$gift_door = $('img', me.$present).not('.gift-image');
        me.$layer = $('.advent-calendar .gift');
        me.$body = $('body');

        me.$present.click(function() {me.openDoor();});
        $('.gift-close', me.$layer).click(function() {me.closeLayer();});
    }

    AdventCalendar.prototype.openDoor = function() {

        var me = this;

        if (me.$gift_door.hasClass('opening')) return;
        if (me.$gift_door.hasClass('open')) me.openLayer();
        else {
            me.$gift_door.addClass('opening');
            me.$layer.addClass("opening");
            //me.$body.addClass("gift-layer");
            window.setTimeout(function() {me.openLayer();}, 1600);
        }
    }

    AdventCalendar.prototype.openLayer = function() {

        var me = this;

        me.$gift_door.addClass('open');
        me.$gift_door.removeClass('opening')

        me.$layer.addClass("open");
        me.$layer.removeClass("opening");
        me.$body.addClass("gift-layer");
    }

    AdventCalendar.prototype.closeLayer = function() {

        var me = this;

        me.$layer.removeClass("open");
        me.$body.removeClass("gift-layer");
    }

    new AdventCalendar();
});
