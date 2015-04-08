/**
 * Initiates the date slider.
 * The main wrapper has to have the selected date in the "data-date" attribute as timestamp,
 * today as timestamp in "data-today" and all weekday strings, comma seperated in "data-days" 
 * and all month strings, comma seperated in "data-months".
 *
 * The main wrapper has to have a transparent image included with the class "date-slider-links"
 * and an unique usemap attribute.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the date slider.
     * The object has to have the selected date in the "data-date" attribute as timestamp
     * today as timestamp in "data-today" and all weekday strings, comma seperated in "data-days" 
     * and all month strings, comma seperated in "data-months".
     *
     * The object has to have a transparent image included with the class "date-slider-links"
     * and an unique usemap attribute.
     *
     * @param   $main   the jQuery object of the gallery wrapper
     */
    function DateSlider($main) {
        
        var me = this;
        this.me = me;
        
        me.day_limit = 366;
        
        me.$main = $main;
        me.$links = $('.date-slider-links', $main);
        me.date = new Date(me.$main.attr('data-date') * 1000);
        me.today = new Date(me.$main.attr('data-today') * 1000);
        me.days = me.$main.attr('data-days').split(",");
        me.months = me.$main.attr('data-months').split(",");
        me.href = me.$main.attr('data-path');
        
        me.usemap = me.$links.attr('usemap').substr(1);
        me.last_width = -1;
        
        me.date = new Date(me.date.getFullYear(), me.date.getMonth(), me.date.getDate());
        me.max_date = new Date(me.today.getFullYear(), me.today.getMonth(), me.today.getDate() + me.day_limit);
        me.today = new Date(me.today.getFullYear(), me.today.getMonth(), me.today.getDate());
        me.first_date = new Date(me.date.getTime());
        
        me.slider_interval = null;
        me.slider_left = 0;
        me.slider_width = 0;
        me.slider_x = 0;
        
        
        var $content = $('<div><div class="date-slider-month"/><div class="date-slider-days"/></div><div class="date-slider-prev"></div><div class="date-slider-next"></div><div class="date-slider-field"><hr/><div class="date-slider-field-button"/></div>');
        me.$main.append($content);
        
        me.$prev = $('.date-slider-prev', me.$main);
        me.$next = $('.date-slider-next', me.$main);
        me.$slider = $('.date-slider-field', me.$main);
        me.$slider_button = $('.date-slider-field-button', me.$main);
        
        me.$month = $('.date-slider-month', me.$main);
        me.$days = $('.date-slider-days', me.$main);
        
        
        me.max_days = me.getMaxDays();
        me.first_date.setDate(me.first_date.getDate() - Math.floor(me.max_days/2));
        
        
        me.$prev.click(function() {me.onPrev();});
        me.$next.click(function() {me.onNext();});
        
        me.$slider.mousedown(function() {me.onSliderStart();});
        $(window).mouseup(function() {me.onSliderEnd();});
        me.$slider.mousemove(function(event) {me.onSliderMove(event);});
        
        me.onResize();
        $(window).resize(function() {me.onResize();});
    }
    
    /**
     * Writes the calender fields.
     */
    DateSlider.prototype.writeCalender = function() {
        
        if (this.me) var me = this.me;
        
        href = me.href;
        
        
        
        if (me.first_date.getTime() < me.today.getTime()) me.first_date = new Date(me.today.getTime());
        var last_date = new Date(me.first_date.getFullYear(), me.first_date.getMonth(), me.first_date.getDate() + me.max_days);
        if (last_date.getTime() > me.max_date.getTime()) {
            me.first_date = new Date(me.max_date.getTime());
            me.first_date.setDate(me.first_date.getDate() - me.max_days);
        }
        
        
        
        me.$month.html(me.months[me.first_date.getMonth()]);
        
        me.$links.detach();
        
        
        var $map = $('<map name="' + me.usemap + '"/>');
        var active = me.date.getTime();
        var date = new Date(me.first_date.getTime());
        
        var html = [];
        for (var i=0; i < me.max_days; i++) {
            
            var left = i*42;
            
            html.push('<div id="'+me.usemap+'item_'+i+'" class="date-slider-item'+(date.getTime() == active ? " active" : "" )+'" style="left:'+left+'px">');
            html.push('<div class="date-slider-day">'+date.getDate()+'</div>');
            html.push('<div class="date-slider-weekday">'+me.days[date.getDay()]+'</div>');
            html.push('</div>');
            
            var year = date.getFullYear();
            var month = date.getMonth()+1;
            var day = date.getDate();
            if (month < 10) month = "0"+month;
            if (day < 10) day = "0"+day;
            var date_string = year+'-'+month+'-'+day;
            
            var $area = $('<area id="'+me.usemap+'_'+i+'" shape="poly" coords="'+(left+16)+',0,'+(left+54)+',0,'+(left+38)+',40,'+(left+38)+',65,'+left+',65,'+left+',40" href="'+href+'?date='+date_string+'" />');
            $area.mouseenter(function() {me.onMouseEnterDate($(this));});
            $area.mouseleave(function() {me.onMouseLeaveDate($(this));});
            $map.append($area);
            
            date.setDate(date.getDate()+1);
        }
        
        me.$days.html(html.join(''));
        me.$days.append(me.$links);
        me.$days.append($map);
        
        me.setNavi();
    }
    
    /**
     * Returns the maximum amount of visible day items.
     *
     * @return  int
     */
    DateSlider.prototype.getMaxDays = function() {
        
        if (this.me) var me = this.me;
        
        var max_width = me.$days.width() - 54;
        
        return Math.floor(max_width/42) + 1;
    }
    
    /**
     * Handles the mouse enter styling of the date divs.
     *
     * @param   $area   the jQuery object of the involved map area
     */
    DateSlider.prototype.onMouseEnterDate = function($area) {
        
        if (this.me) var me = this.me;
        
        var id = $area.attr('id').split("_");
        var index = id[id.length-1];
        
        $('#'+me.usemap+'item_'+index, me.$main).addClass('over');
    }
    
    
    /**
     * Handles the mouse leave styling of the date divs.
     *
     * @param   $area   the jQuery object of the involved map area
     */
    DateSlider.prototype.onMouseLeaveDate = function($area) {
        
        if (this.me) var me = this.me;
        
        var id = $area.attr('id').split("_");
        var index = id[id.length-1];
        
        $('#'+me.usemap+'item_'+index, me.$main).removeClass('over');
    }
    
    /**
     * Shows the next days.
     */
    DateSlider.prototype.onNext = function() {
        
        if (this.me) var me = this.me;
       
        me.first_date.setDate(me.first_date.getDate() + me.max_days);
        
        me.writeCalender();
    }
    
    /**
     * Shows the previous days.
     */
    DateSlider.prototype.onPrev = function() {
        
        if (this.me) var me = this.me;
             
        me.first_date.setDate(me.first_date.getDate() - me.max_days);
        
        me.writeCalender();
    }
    
    /**
     * Slider is pressed.
     */
    DateSlider.prototype.onSliderStart = function() {
        
        if (this.me) var me = this.me;
        
        if (me.slider_interval) {
            window.clearInterval(me.slider_interval);
            me.slider_interval = null;
        }
        
        me.calculateSliderDate();
        me.slider_interval = window.setInterval(function() {me.calculateSliderDate();}, 25);
    }
    
    /**
     * Slider is released.
     */
    DateSlider.prototype.onSliderEnd = function() {
        
        if (this.me) var me = this.me;
        
        if (me.slider_interval) {
            me.calculateSliderDate();
            window.clearInterval(me.slider_interval);
            me.slider_interval = null;
        }
    }
    
    /**
     * Mouse is moved in the slider area.
     *
     * @param   event   the mouse event
     */
    DateSlider.prototype.onSliderMove = function(event) {
        
        if (this.me) var me = this.me;
        
        me.slider_x = event.pageX - me.slider_left;
    }
    
    /**
     * Calculates the date accordingly to the slider position.
     */
    DateSlider.prototype.calculateSliderDate = function() {
        
        if (this.me) var me = this.me;
        
       
        
        var position = me.slider_x;
        if (position > me.slider_width - 10) position = me.slider_width - 10;
        position -= 10;
        position /= me.slider_width - 20;
        
        var days = Math.round((me.day_limit - me.max_days) * position);
        me.first_date = new Date(me.today.getTime());
        me.first_date.setDate(me.first_date.getDate() + days);
        
        me.writeCalender();
    }
    
    /**
     * Checks visibility and position of navigation elements.
     */
    DateSlider.prototype.setNavi = function() {
        
        if (this.me) var me = this.me;
        
        if (me.first_date.getTime() == me.today.getTime()) me.$prev.css("display", "none");
        else me.$prev.css("display", "block");
        
        var last_date = new Date(me.first_date.getTime());
        last_date.setDate(last_date.getDate() + me.max_days);
        
        
        if (last_date.getTime() == me.max_date.getTime()) me.$next.css("display", "none");
        else me.$next.css("display", "block");
        
        
        var days = Math.round((me.first_date.getTime() - me.today.getTime()) / 1000 / 60 / 60 / 24);
        var position = days / (me.day_limit - me.max_days);
        var left = Math.round((me.slider_width - 20) * position);
        me.$slider_button.css("left", left+"px");
    }
    
    /**
     * Setting styles depending on the width and margin.
     */
    DateSlider.prototype.setStyles = function() {
        
        if (this.me) var me = this.me;
        
        var main_width = me.$main.width();
        var slider_margin = Math.round(($(window).width() - main_width) / 2);
        if (slider_margin > 70) slider_margin = 70;
        
        if (main_width < 400) {
            me.$main.addClass("medium");
        } else {
            me.$main.removeClass("medium");
        }
        
        if (main_width < 300) {
            me.$main.addClass("small");
        } else {
            me.$main.removeClass("small");
        }
        
        if (slider_margin < 35) {
            me.$main.addClass("small-margin");
            slider_margin -= 35;
        } else {
            me.$main.removeClass("small-margin");
            slider_margin -= 35;
        }
        
        if (slider_margin < 0) {
            slider_margin *= -1;
            me.$prev.css('left', slider_margin + "px");
            me.$next.css('right', slider_margin + "px");
        } else {
            me.$prev.css('left', "-" + slider_margin + "px");
            me.$next.css('right', "-" + slider_margin + "px");
        }
        
    }
    
    /**
     * The window got resized.
     */
    DateSlider.prototype.onResize = function() {
        
        if (this.me) var me = this.me;
        
        var new_width = me.$main.width();
        
        if (new_width != me.last_width) {
            
            me.last_width = new_width;
            
            me.slider_width = me.$slider.width();
            me.slider_left = me.$slider.offset().left;
            
            me.$days.html('');
            me.max_days = me.getMaxDays();
            me.writeCalender();
        }
        
        me.setStyles();
    }
    
    function init() {
        
        $('.date-slider').each(function() {
            new DateSlider($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();