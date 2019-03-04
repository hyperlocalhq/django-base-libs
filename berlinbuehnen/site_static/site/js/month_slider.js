/**
 * Initiates the month slider.
 * The main wrapper has to have today as timestamp in "data-today" and all month strings, comma seperated in "data-months".
 *
 * If the month slider has an id and it exists a grid with the id resampling the first part of the slider id up to "_" and adding "_list",
 * the content of the grid gets connected to the slider. The grid items would need to have their start date as timestamp in "data-start" 
 * and their end date in "data-end".
 * E.g.: the slider with the id "main_monthslider" would belong to the grid with the id "main_list".
 *
 * Elements with a class resampling the first part of the slider id up to "_" and adding "_clear" becoming a button for resetting the filter.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the month slider.
     * The object has to have today as timestamp in "data-today" and all month strings, comma seperated in "data-months".
     *
     * @param   $main   the jQuery object of the slider
     */
    function MonthSlider($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        var main_id = me.$main.attr('id');
        var connect_id = (main_id) ? main_id.split('_', 2) : '';
        me.connect_id = connect_id[0];
        
        me.$list = (me.connect_id) ? $('#'+me.connect_id+'_list') : '';  
        me.list = (me.$list) ? me.$list.data("list") : null;
        
        me.months = me.$main.attr('data-months').split(",");
        me.today = new Date(me.$main.attr('data-today') * 1000);
        me.start = new Date(me.today.getFullYear(), me.today.getMonth(), 1);
        me.end = new Date(me.today.getFullYear(), me.today.getMonth(), 1);
        me.current_start = new Date(me.today.getFullYear(), me.today.getMonth(), 1);
        me.active_months = [];
        me.active_years = [];
        
        me.$clear_toggle = $('.'+me.connect_id+'_clear.clear_toggle');
        
        if (me.$list) me.calculateRange();
        
        var html = '<a href="javascript:void(0);" class="month-slider-prev fawesome prev"></a><div class="month-slider-dates"></div><a href="javascript:void(0);" class="month-slider-next fawesome next"></a>';
        me.$main.append(html);
        
        me.$prev = $('.month-slider-prev', me.$main);
        me.$next = $('.month-slider-next', me.$main);
        me.$dates = $('.month-slider-dates', me.$main);
        
        me.onResize();
        me.$prev.click(function() {me.onPrev();});
        me.$next.click(function() {me.onNext();});
        
        $('.'+me.connect_id+'_clear').click(function() {me.onClearFilter();});
        
        $(window).resize(function() {me.onResize();});
        window.setTimeout(function() {me.onResize();}, 200);
    }
    
    MonthSlider.prototype.calculateRange = function() {
     
        var me = this.me;
        me.list = (me.$list) ? me.$list.data("list") : null;
        
        me.list.$items.each(function() {
           
            var $this = $(this);
            var start = new Date($this.attr('data-start') * 1000);
            var end = new Date($this.attr('data-end') * 1000);
            
            start = new Date(start.getFullYear(), start.getMonth(), 1);
            end = new Date(end.getFullYear(), end.getMonth(), 1);
            
            if (me.start.getTime() > start.getTime()) me.start = new Date(start.getTime());
            if (me.end.getTime() < end.getTime()) me.end = new Date(end.getTime());
            
            while (start.getTime() <= end.getTime()) {
                var month = 'month-slider-'+start.getFullYear()+'-'+start.getMonth();
                var year = 'month-slider-'+start.getFullYear();
                me.active_months[month] = true;
                me.active_years[year] = true;
                $this.addClass(month);
                $this.addClass(year);
                start = new Date(start.getFullYear(), start.getMonth()+1, 1);
            }
        });
        
        if (me.today.getTime() > me.start.getTime()) me.start = new Date(me.today.getTime());
        
    }
    
    MonthSlider.prototype.createDates = function() {
        
        var me = this.me;
        
        me.$dates.html('');
        
        var html = '';
        var current_html = '';
        var current_year = '';
        var date = new Date(me.current_start.getFullYear(), me.current_start.getMonth(), 1);
        
        
        
        while (me.$dates.width() < me.$main.width()) {
         
            current_html = html;
            
            var year = date.getFullYear();
            if (current_year != year) {
                current_year = year;   
                var id = 'month-slider-'+year;
                if (me.active_years[id]) {
                    html += '<a id="'+id+'" href="javascript:void(0);" class="month-slider-year">'+year+'</a>';
                } else {
                    html += '<span class="month-slider-year">'+year+'</span>';
                }
            }
            
            me.$dates.html(html);
            
            if (me.$dates.width() < me.$main.width()) {
                
                current_html = html;
                
                var month = date.getMonth();
                var id = 'month-slider-'+year+'-'+month;
                if (me.active_months[id]) {
                    html += '<a id="'+id+'" href="javascript:void(0);" class="month-slider-month">'+me.months[month]+'</a>';
                } else {
                    html += '<span class="month-slider-month">'+me.months[month]+'</span>';
                }
                
                me.$dates.html(html);
            }
            
            date = new Date(date.getFullYear(), date.getMonth()+1, 1);
            
            //console.log(me.$dates.width() + ' - ' + me.$main.width());
        }
        
        date = new Date(date.getFullYear(), date.getMonth()-1, 1);
        me.$dates.html(current_html);
        
        $('a', me.$dates).click(function() {me.onFilter($(this));});
        
        
        
        if (me.current_start.getTime() > me.start.getTime()) me.$prev.css('display', 'block');
        else me.$prev.css('display', 'none');
        
        if (date.getTime() > me.end.getTime()) me.$next.css('display', 'none');
        else me.$next.css('display', 'block');
    }
    
    MonthSlider.prototype.onFilter = function($link) {
        
        var me = this.me;
        me.list = (me.$list) ? me.$list.data("list") : null;
        
        if ($link.hasClass('active')) {
            
            $('a', me.$dates).removeClass('active');
            me.$clear_toggle.css('display', 'none');
            if (me.list) me.list.$items.css('display', 'block');
            
        } else {
        
            $('a', me.$dates).removeClass('active');
            $link.addClass('active');
            me.$clear_toggle.css('display', 'block');
            if (me.list) {
                var id = $link.attr('id');    
                me.list.$items.css('display', 'none');
                $('.'+id, me.$list).css('display', 'block');
            }
        }
        
        if (me.list) me.list.reinitByFilter();
    }
    
    MonthSlider.prototype.onClearFilter = function() {
        
        var me = this.me;
        me.list = (me.$list) ? me.$list.data("list") : null;
        
        $('a', me.$dates).removeClass('active');
        me.$clear_toggle.css('display', 'none');
        if (me.list) me.list.$items.css('display', 'block');
            
        if (me.list) me.list.reinitByFilter(); 
    }
    
    MonthSlider.prototype.onPrev = function() {
        
        var me = this.me;
        
        if (me.current_start.getTime() > me.start.getTime()) me.current_start = new Date(me.current_start.getFullYear(), me.current_start.getMonth()-1, 1);
        me.createDates();
    }
    
    MonthSlider.prototype.onNext = function() {
        
        var me = this.me;
        
        me.current_start = new Date(me.current_start.getFullYear(), me.current_start.getMonth()+1, 1);
        me.createDates();
    }
    
    MonthSlider.prototype.onResize = function() {
        
        var me = this.me;
        
        me.createDates();
        
        var main_width = me.$main.width();
        var slider_margin = Math.round(($(window).width() - main_width) / 2);
        
        var margin_class= "";
        if (slider_margin <= 45) margin_class = "medium";
        if (slider_margin <= 30) margin_class = "small";
        
        me.$main.removeClass("medium").removeClass("small").addClass(margin_class);
        
        //console.log(slider_margin);
    }
    
    function init() {
        
        $('.month-slider').each(function() {
            new MonthSlider($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();