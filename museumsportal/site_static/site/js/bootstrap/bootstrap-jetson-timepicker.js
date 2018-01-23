/* 
 * bootstrap-jetson-timepicker.js 
 *
 * Copyright 2013 Thomas Helbig and Aidas Bendoraitis 
 * 
 */
 
(function($){
    function get_template(settings) {
        var template = '<div id="popup">'
            + '<div class="inner clearfix">'
                + '<div id="picker" class="clearfix">'
                    + '<header class="clearfix">'
                        + '<time>HH:MM</time>'
                    + '</header>'
                    + '<ul class="body clearfix">'
                        + '<li>'
                            + '<table class="hours">'
                                + '<thead>'
                                    + '<tr>'
                                        + '<th colspan="6">' + settings.str_hours + '</th>'
                                    + '</tr>'
                                + '</thead>'
                                + '<tbody>'
                                    + '<tr>'
                                        + '<td><span class="h-0">00</span></td>'
                                        + '<td><span class="h-1">01</span></td>'
                                        + '<td><span class="h-2">02</span></td>'
                                        + '<td><span class="h-3">03</span></td>'
                                        + '<td><span class="h-4">04</span></td>'
                                        + '<td><span class="h-5">05</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="h-6">06</span></td>'
                                        + '<td><span class="h-7">07</span></td>'
                                        + '<td><span class="h-8">08</span></td>'
                                        + '<td><span class="h-9">09</span></td>'
                                        + '<td><span class="h-10">10</span></td>'
                                        + '<td><span class="h-11">11</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="h-12">12</span></td>'
                                        + '<td><span class="h-13">13</span></td>'
                                        + '<td><span class="h-14">14</span></td>'
                                        + '<td><span class="h-15">15</span></td>'
                                        + '<td><span class="h-16">16</span></td>'
                                        + '<td><span class="h-17">17</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="h-18">18</span></td>'
                                        + '<td><span class="h-19">19</span></td>'
                                        + '<td><span class="h-20">20</span></td>'
                                        + '<td><span class="h-21">21</span></td>'
                                        + '<td><span class="h-22">22</span></td>'
                                        + '<td><span class="h-23">23</span></td>'
                                    + '</tr>'
                                + '</tbody>'
                            + '</table>'
                        + '</li>'
                        + '<li>'
                            + '<table class="minutes">'
                                + '<thead>'
                                    + '<tr>'
                                        + '<th colspan="3">' + settings.str_minutes + '</th>'
                                    + '</tr>'
                                + '</thead>'
                                + '<tbody>'
                                    + '<tr>'
                                        + '<td><span class="m-0">00</span></td>'
                                        + '<td><span class="m-5">05</span></td>'
                                        + '<td><span class="m-10">10</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="m-15">15</span></td>'
                                        + '<td><span class="m-20">20</span></td>'
                                        + '<td><span class="m-25">25</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="m-30">30</span></td>'
                                        + '<td><span class="m-35">35</span></td>'
                                        + '<td><span class="m-40">40</span></td>'
                                    + '</tr>'
                                    + '<tr>'
                                        + '<td><span class="m-45">45</span></td>'
                                        + '<td><span class="m-50">50</span></td>'
                                        + '<td><span class="m-55">55</span></td>'
                                    + '</tr>'
                                + '</tbody>'
                            + '</table>'
                        + '</li>'
                    + '</ul>'
                    + '<footer class="clearfix">'
                        + '<button class="cancel right">' + settings.str_close + '</button>'
                        + '<button class="done btn-primary">' + settings.str_confirm + '</button>'
                    + '</footer>'
                + '</div>'
            + '</div>'
        + '</div>';
        return template;
    }
        
    $.fn.extend({ 
         
        //pass the options variable to the function
        timepicker: function(options) {
            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                default_time: "09:00",
                str_hours: "Hours",
                str_minutes: "Minutes",
                str_confirm: "Confirm",
                str_close: "Close"
            }
            var settings = $.extend({}, defaults, options);
            
            return this.each(function() {
                var $input = $(this);
                if ($input.data('timepicker-applied')) {
                    return;
                }
                $(this).parent().addClass('input-append');
                $('<span class="input-group-btn"><button class="btn btn-lg btn-icon btn-info pick-time" type="button"><span class="icon icon-clock"></span></button></span>').insertAfter(this).find('button').click(function() {
                    $('body').append(get_template(settings));
                    $("#popup").delay(100).queue(function () {
                        $(this).addClass("on");
                        $(this).dequeue();
                    });
                    var $picker = $('#picker');
                    var time = ($input.val() || settings.default_time).split(":");
                    var hours = parseInt(time[0], 10);
                    var minutes = Math.round(parseInt(time[1], 10) / 5) * 5;
                    if (minutes > 55) {
                        minutes = 55;
                    }
                    var $sel_hours = $('.h-' + hours, $picker).addClass('active');
                    var $sel_minutes = $('.m-' + minutes, $picker).addClass('active');
                    $('time', $picker).text($sel_hours.text() + ':' + $sel_minutes.text());
                    $('table.hours td>span', $picker).mousedown(function() {
                        $sel_hours.removeClass('active');
                        $sel_hours = $(this).addClass('active');
                        $('time', $picker).text($sel_hours.text() + ':' + $sel_minutes.text());
                    });
                    $('table.minutes td>span', $picker).mousedown(function() {
                        $sel_minutes.removeClass('active');
                        $sel_minutes = $(this).addClass('active');
                        $('time', $picker).text($sel_hours.text() + ':' + $sel_minutes.text());
                    });
                    $('button.cancel', $picker).click(function() {
                        $("#popup").removeClass("on").delay(250).queue(function () {
                            $(this).remove();
                            $(this).dequeue();
                        });
                    });
                    $('button.done', $picker).click(function() {
                        $input.val($sel_hours.text() + ':' + $sel_minutes.text());
                        $input.focus();
                        $("#popup").removeClass("on").delay(250).queue(function () {
                            $(this).remove();
                            $(this).dequeue();
                        });
                    });
                    return false;
                });
                $input.data('timepicker-applied', true);
            });
        }
    });
})(jQuery);
