/**
 * Initiates the image slider.
 * The images have to have the same dimensions.
 
 * Add the "data-image-ratio" attribute to the main object to set the ratio of the shown images.
 * Otherwise the ratio is calculated by the loaded images which does not always work.
 * E.g.: data-image-ratio="680:370" - where the first value is the length and the second the height of the ratio.
 *
 * If the attribute "data-adjust-style" with a true value is set, the slider checks the size of the slider and 
 * its left/right margin and adds css classes to the main object. Adjust the function setStyles() for more changes.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the slider which contains the $('.slider-item') objects.
     *
     * @param   $main   the jQuery object of the gallery wrapper
     */
    function Slider($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$body = $('.slider-body', $main);
        me.$items = $('.slider-item', $main);
        me.initial_items_length = me.$items.length;
        me.last_width = -1;
        
        $('a', me.$items).attr('target', '_self');
        
        if (me.initial_items_length == 0) {
            $main.remove();
            return;
        }
        
        me.current_item = 0;
        me.max_items = 0;
        me.item_width;
        me.animating = false;
        
        me.$main.append('<div class="slider-prev fawesome back"></div><div class="slider-next fawesome more"></div>');
        me.$prev = $('.slider-prev', me.$main);
        me.$next = $('.slider-next', me.$main);
        
        me.adjust_style = me.$main.data('adjust-style');
        
        me.ratio_width = 0;
        me.ratio_height = 0;
        var ratio = me.$main.data("image-ratio");
        if (ratio) {
            ratio = ratio.split(':');
            if (ratio[0] && ratio[1]) {
                me.ratio_width = parseFloat(ratio[0]);
                me.ratio_height = parseFloat(ratio[1]);
            }
        }
        
        me.timer = null;
        me.timer_time = parseInt(me.$main.data('slider-timer'));
        
        
        me.onResize();
        $(window).resize(function() {me.onResize();});
        
        me.$prev.click(function() {me.prevItems();});
        me.$next.click(function() {me.nextItems();});
        me.$main.on('swiperight', function() {me.prevItems();});
        me.$main.on('swipeleft', function() {me.nextItems();});
        
        
        if (me.timer_time) {
            me.timer = window.setTimeout(function() {me.onTimer();}, me.timer_time);
            me.$main.mouseenter(function() {me.onTimerOver();});
            me.$main.mouseleave(function() {me.onTimerOut();});
            me.$main.click(function() {me.onTimerClicked();});
            me.$main.on('swipe', function() {me.onTimerClicked();});
        }
    }
    
    /**
     * Sets the height and gets the width of the slider.
     */
    Slider.prototype.calculateDimensions = function(test) {
        
        if (this.me) var me = this.me;
        
        var max_width = 0;
        var max_height = 0;
        
        var length = me.$items.length;
        for (var i=0; i < length; i++) {
            
            $item = $(me.$items.get(i));
            
            var test_width = $item.width();
            var test_height = $item.height();
            
            if (test_width > max_width) max_width = test_width;
            if (test_height > max_height) max_height = test_height;
        }
        
        if (me.ratio_width && me.ratio_height) {
            max_height = Math.round(max_width * me.ratio_height / me.ratio_width);
        }
        me.$body.height(max_height);
        me.item_width = max_width;
        
        var current_items = me.max_items
        me.max_items = Math.round(me.$body.width() / max_width);
        
        if (current_items != me.max_items) {
            
            me.$items.detach();
            
            // handling the case that there are to few items to have a slider
            while (me.$items.length > 1 && me.$items.length < me.max_items * 2) {
                for (var i=0; i < me.initial_items_length; i++) {
                    var $clone = $(me.$items.get(i)).clone();
                    me.$items = me.$items.add($clone);
                }
            }
            
            
            me.$main.off('swiperight');
            me.$main.off('swipeleft');
            
            if (me.initial_items_length <= me.max_items) {
                me.$prev.css('display', 'none');
                me.$next.css('display', 'none');
            } else {
                me.$prev.css('display', 'block');
                me.$next.css('display', 'block');
                me.$main.on('swiperight', function() {me.prevItems();});
                me.$main.on('swipeleft', function() {me.nextItems();});
            }
        }
    }
    
    /**
     * Setting styles depending on the width and margin.
     */
    Slider.prototype.setStyles = function() {
        
        if (this.me) var me = this.me;
        
        var main_width = me.$main.width();
        var slider_margin = Math.round(($(window).width() - main_width) / 2) - 10;
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
        
        if (slider_margin < 30) {
            me.$main.addClass("small-margin");
            slider_margin += 3;
        } else {
            me.$main.removeClass("small-margin");
        }
        
        me.$prev.css('left', "-" + slider_margin + "px");
        me.$next.css('right', "-" + slider_margin + "px");
        
    }
    
    /**
     * Returns an array including the indices of the currently visible items
     *
     * @return  array
     */
    Slider.prototype.getItems = function() {
        
        if (this.me) var me = this.me;
        
        var indices = new Array();
        for (i = 0; i < me.max_items; i++) {
            
            var index = me.current_item + i;
            if (index >= me.$items.length) {
                index -= me.$items.length;
            }
            
            indices.push(index);
        }
        
        return indices;
    }
    
    /**
     * Sets the currently visible items.
     */
    Slider.prototype.setItems = function() {
        
        if (this.me) var me = this.me;
        
        var indices = me.getItems();
        
        var left = $(me.$items.get(me.current_item)).position().left;
        for (var i=0; i < me.max_items; i++) {
            
            var $item = $(me.$items.get(indices[i]));
            $item.css('left', left+'px');
            me.$body.append($item);
            
            left += me.item_width;
            
            if (me.$items.length <= 1) break;
        }
    }
    
    /**
     * Slides to the next items.
     */
    Slider.prototype.nextItems = function() {
        
        if (this.me) var me = this.me;
        if (me.animating) return;
        
        
        var old_items = me.getItems();
        me.current_item += me.max_items;
        if (me.current_item >= me.$items.length) {
            me.current_item -= me.$items.length;
        }
        var new_items = me.getItems();
        
        
        var left = me.item_width * me.max_items;
        for (var i=0; i < me.max_items; i++) {
            
            var $item = $(me.$items.get(new_items[i]));
            $item.css('left', left+'px');
            me.$body.append($item);
            
            left += me.item_width;
        }
        
        me.calculateDimensions();
        me.slideItems(old_items, new_items);
    }
    
    /**
     * Slides to the previous items.
     */
    Slider.prototype.prevItems = function() {
        
        if (this.me) var me = this.me;
        if (me.animating) return;
        
        
        var old_items = me.getItems();
        me.current_item -= me.max_items;
        if (me.current_item < 0) {
            me.current_item += me.$items.length;
        }
        var new_items = me.getItems();
        
        
        var left = me.item_width * me.max_items * (-1);
        for (var i=0; i < me.max_items; i++) {
            
            var $item = $(me.$items.get(new_items[i]));
            $item.css('left', left+'px');
            me.$body.append($item);
            
            left += me.item_width;
        }
        
        me.calculateDimensions();
        me.slideItems(old_items, new_items);
    }
    
    /**
     * Slides the old items of the scrreen and the new on.
     * All slider items have to be already attached to the DOM.
     * The length of old_items and new_items has to be me.max_items.
     *
     * @param   old_items   the indices of the old items in an array
     * @param   new_items   the indices of the new items in an array
     */
    Slider.prototype.slideItems = function(old_items, new_items) {
        
        if (this.me) var me = this.me;
        if (me.animating) return;
        me.animating = true;
        
        var width = me.item_width * me.max_items;
        
        for (var i=0; i < me.max_items; i++) {
            
            var $old_item = $(me.$items.get(old_items[i]));
            var $new_item = $(me.$items.get(new_items[i]));
            
            var old_left = $old_item.position().left;
            var new_left = $new_item.position().left;
            var offset = (old_left < new_left) ? -width : width;
            
            $old_item.animate({left:old_left+offset}, 400, function() {
               $(this).detach(); 
               me.animating = false;
            });
            $new_item.animate({left:new_left+offset}, 400);
        }
    }
    
    /**
     * Slides to the next item.
     */
    Slider.prototype.onTimer = function() {
        
        if (this.me) var me = this.me;
        
        me.nextItems();
        
        me.timer = window.setTimeout(function() {me.onTimer();}, me.timer_time);
    }
    
    /**
     * Mouse is over the slider and the timer gets stoped.
     */
    Slider.prototype.onTimerOver = function() {
        
        if (this.me) var me = this.me;
        
        if (me.timer) {
            window.clearTimeout(me.timer);
            me.timer = null;
        }
    }
    
    /**
     * Mouse left the slider and the timer gets restarted.
     */
    Slider.prototype.onTimerOut = function() {
        
        if (this.me) var me = this.me;
        
        if (me.timer) {
            window.clearTimeout(me.timer);
            me.timer = null;
        }
        
        me.timer = window.setTimeout(function() {me.onTimer();}, me.timer_time);
    }
    
    /**
     * The slider got clicked and the timer gets stop indefinitely.
     */
    Slider.prototype.onTimerClicked = function() {
        
        if (this.me) var me = this.me;
        
        if (me.timer) {
            window.clearTimeout(me.timer);
            me.timer = null;
        }
        
        me.$main.off('mouseenter');
        me.$main.off('mouseleave');  
        me.$main.off('click');   
    }
    
    /**
     * The window got resized.
     */
    Slider.prototype.onResize = function() {
        
        if (this.me) var me = this.me;
        
        var new_width = me.$main.width();
        
        if (new_width != me.last_width) {
            me.last_width = new_width;
            me.calculateDimensions();
            me.setItems();
        }
        
        if (me.adjust_style) me.setStyles();
    }
    
    function init() {
        
        $('.slider').each(function() {
            new Slider($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();