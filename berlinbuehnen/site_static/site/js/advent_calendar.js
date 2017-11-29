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

        me.$present.click(function() {me.openLayer();});
        $('.gift-close', me.$layer).click(function() {me.closeLayer();});
    }

    AdventCalendar.prototype.openLayer = function() {

        var me = this;

        me.$gift_door.addClass('open');

        me.$layer.addClass("open");
        me.$body.addClass("gift-layer");
    }

    AdventCalendar.prototype.closeLayer = function() {

        var me = this;

        me.$layer.removeClass("open");
        me.$body.removeClass("gift-layer");
    }

    new AdventCalendar();
});
