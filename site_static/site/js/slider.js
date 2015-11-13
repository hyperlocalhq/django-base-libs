/**
 * Provides functionality and styling for sliders.
 *
 * Define the speed of the animation by providing a "data-speed" attribute in milliseconds inside the main slider tag.
 * Define a timer for the animation by providing a "data-timer" attribute in milliseconds inside the main slider tag.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function Slider($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$wrapper = $('.wrapper', me.$main);
        me.$elements = $('.slide', me.$main);
        me.$body = $('body');
        me.$window = $(window);
        me.is_header = me.$main.parents('.header').length;
        
        if (!me.$wrapper.length) me.$wrapper = me.$main;
        
        me.speed = (me.$main.attr('data-speed')) ? parseInt(me.$main.attr('data-speed')) : 300;
        me.timer = (me.$main.attr('data-timer')) ? parseInt(me.$main.attr('data-timer')) : false;
        
        me.current_element = 0;
        me.previous_element = 0;
        me.timeout = null;
        me.elements_amount = me.$elements.length;
        me.loop = false; // does slider loop
        me.margin = 0; // the margin/padding between the elements
        me.disabled = false; // disable slider (prev/next slider moves)
        me.animating = false; // is slider currently animating movements
        me.$prev = null;
        me.$next = null;
        
        me.$window.resize(function() {me.styleIt(false, 200);});
        $(document).ready(function() {me.styleIt();});
        $('img', me.$main).load(function() {me.styleIt();});
        me.styleIt();
        
        me.$main.on("swiperight", function() {me.timer = false; me.prev();});
        me.$main.on("swipeleft", function() {me.timer = false; me.next();});
    }
    
    /**
     * Set the style values of the elements.
     * Calls the sub-style functions of the specific types of sliders.
     * Sets the left positions of the elements depending on the value of me.current_element.
     *
     * @param   animate     animate changes
     * @param   delay       start styling after delay in ms
     */
    Slider.prototype.styleIt = function(animate, delay) {
        
        var me = this.me;
        
        if (me.timeout) {
            clearTimeout(me.timeout);
            me.timeout = null;
        }
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        if (me.$main.hasClass('portfolio')) {
            me.stylePortfolio();
        } else if (me.$main.hasClass('fullside')) {
            me.styleFullside();
        }
        
        if (!animate) {
            
            me.$elements.each(function() {
           
                var $element = $(this);
                $element.css('left', $element.data('left') + "px");
            
            });
            
            me.checkNextPrev();
            
        } else {
            
            me.animating = true;
            
            var counter = me.$elements.length;
            
            me.$elements.each(function() {
                
                var $element = $(this);
                
                $element.animate({
                    left: $element.data('left')
                }, me.speed, function() {
                    
                    counter--;
                    if (me.timeout) {
                        clearTimeout(me.timeout);
                        me.timeout = null;
                    }
                    
                    
                    if (counter <= 0) {
                        
                        me.checkNextPrev();
                        me.animating = false;
                        
                        if (me.timer) {
                            me.timeout = setTimeout(function() {me.next();}, me.timer);    
                        }
                    }
                    
                });
            });
        }
        
        if (me.timer) {
            me.timeout = setTimeout(function() {me.next();}, me.timer);    
        }
    }
    
    /**
     * Styles the portfolio slider.
     * Calculates the left positions of the elements.
     */
    Slider.prototype.stylePortfolio = function() {
        
        var me = this.me;   
        
        me.margin = 5;
        
        if (me.$body.hasClass('is-xs')) {
            
            me.$elements.css('width', '');
            $('h2', me.$main).css('margin-top', '');
            
            if (me.$prev) {
                me.$prev.css('display', '');
                me.$next.css('display', '');
            }
            
            me.disabled = true;
            
        } else {
            
            me.$elements.each(function() {
               
                var $element = $(this);
                var $img = $('img', $element);
                var $text = $('h2', $element);
                
                $element.width($img.width()+10);
                $text.css('margin-top', "-" + Math.round($text.height()/2) + "px");
                $element.data('old-left', $element.position().left);
            });
            
            var $current_element = $(me.$elements.get(me.current_element));
            var wrapper_width = me.$wrapper.width();
            var elements_length = me.$elements.length;
            
            
            // checking if second or second last element are already visible in the slider and move to next element
            if (me.previous_element == 0 && me.previous_element != me.current_element && me.current_element < elements_length-2 && $current_element.position().left + $current_element.width() <= wrapper_width) {
                me.current_element++;
                $current_element = $(me.$elements.get(me.current_element));
            } else if (me.previous_element == elements_length-1 && me.previous_element != me.current_element && me.current_element > 0 && $current_element.position().left >= 0) {
                me.current_element--;
                $current_element = $(me.$elements.get(me.current_element));
            }
            
            
            me.$elements.css('left', '');
            var current = me.current_element;
            
            // setting left position of center element
            var left = Math.round((wrapper_width - $current_element.width()) / 2);
            
            // finding left position of outer most left element
            for (var i=0; i<current; i++) {
                var $element = $(me.$elements.get(i));
                left -= $element.width();
            }
            
            // if outer most left position is still inside slider width
            if (left > me.margin*(-1)) left = me.margin*(-1);                
            else {
                
                // calculating right position of outer most right element
                var right = left;
                for (var i=0, length = elements_length; i < length; i++) {
                    var $element = $(me.$elements.get(i));
                    right += $element.width();
                }
                
                // if outer most right is still inside slider width
                if (right < wrapper_width + me.margin) {
                    
                    // calculating left position of outer most right element
                    var $element = $(me.$elements.get(elements_length-1));
                    left = wrapper_width - $element.width() + me.margin;
                    
                    // finding left position of outer most left element
                    for (var i=0; i<current; i++) {
                        var $element = $(me.$elements.get(i));
                        left -= $element.width();
                    }
                    
                    // if outer most left is still inside slider width
                    if (left > me.margin*(-1)) left = me.margin*(-1);
                }
            }
            
            
            
            var width = 0;
            me.$elements.each(function() {
               
                var $element = $(this);
               
                $element.data('left', left);
                $element.css('left', $element.data('old-left') + "px");
                left += $element.width();
                width += $element.width();
            });
            
            
            if (!me.$prev) {
                
                me.$prev = $('<div class="fawesome fa-left-bold prev"><span class="sr-only">previous</span></div>');
                me.$next = $('<div class="fawesome fa-right-bold next"><span class="sr-only">next</span></div>');
                
                me.$main.append(me.$prev);
                me.$main.append(me.$next);
                
                me.$prev.click(function(e) {me.timer = false; me.prev(e); return false;});
                me.$next.click(function(e) {me.timer = false; me.next(e); return false;});
                
            }
            
            
            if (width <= me.$wrapper.width()) { 
                
                me.$prev.css('display', 'none');
                me.$next.css('display', 'none');
                
            } else {
                
                me.$prev.css('display', 'block');
                me.$next.css('display', 'block');
                
                var margin = Math.round((me.$body.width() - me.$wrapper.width()) / 2 - 1);
                if (margin > 50) margin = 50;
                if (me.is_header && margin > 30) margin = 30;
                if (margin < 15) margin = 15;
                
                me.$prev.css('left', '-'+margin+'px');
                me.$next.css('right', '-'+margin+'px');
                
                var right = me.$next.offset().left + me.$next.width();
                if (me.$window.width() < right) {
                    margin -= right - me.$window.width();
                    if (margin < 15) margin = 15;
                    me.$prev.css('left', '-'+margin+'px');
                    me.$next.css('right', '-'+margin+'px');
                }
            }
            
            
            me.disabled = false;
            me.checkNextPrev();
        }
    }
    
    
    /**
     * Styles the full side slider.
     * Calculates the left positions of the elements.
     */
    Slider.prototype.styleFullside = function() {
        
        var me = this.me;
        
        me.loop = true;
        var min_height_xs = 270;
        
        var $current_element = $(me.$elements.get(me.current_element));
        
        
        var $images = $('img', me.$main);
        $images.css('width', '').css('height', '');
        if (me.$body.hasClass('is-xs')) {
            $images.each(function() {
                var $image = $(this);
                if ($image.height() < min_height_xs) {
                    $image.css('width', 'auto').height(min_height_xs);
                }
            });
        }
        
        me.$main.css('height', '');
        me.$main.height($current_element.height());
        
        
        if (me.$elements.length > 1 && me.$elements.length < 3) {
            me.$main.append(me.$elements.clone(true));
            me.$elements = $('.slide', me.$main);
        }
        
        
        var top = 0;
        me.$elements.each(function() {
            
            var $element = $(this);
            var $image = $('img', $element);
            var $text = $('.container', $element);
            
            $element.css('top', top + 'px');
            $image.css('top', Math.round(($element.height() - $image.height()) / 2) + 'px');
            $image.css('left', Math.round(($element.width() - $image.width()) / 2) + 'px');
            $text.css('margin-top', '-' + Math.round($text.height() / 2) + 'px');
            $text.css('left', Math.round(($element.width() - $text.width()) / 2) + 'px');
            
            top -= $element.height();
        });
        
        
        
        var left = 0;
        for (var i=me.previous_element-1; i>=0; i--) {
            var $element = $(me.$elements.get(i));
            left -= $element.width();
        }
        
        var start = left;
        me.$elements.each(function() {
            var $element = $(this);
            $element.css('left', left+'px');
            $element.data('left', left);
            left += $element.width();
        });
        var end = left;
        
        
        
        if (me.previous_element != me.current_element) {
            
            if (me.previous_element == 0 && me.current_element != 1) {
            
                var $element = $(me.$elements.get(me.$elements.length-1));
                $element.css('left', (start - $element.width()) + 'px');
                $element.data('left', start);
                
                var $element = $(me.$elements.get(0));
                $element.data('left', start + $element.width());
            
            } else if (me.current_element == 0 && me.previous_element != 1) {
            
                var $element = $(me.$elements.get(0));
                $element.css('left', end + 'px');
                $element.data('left', end - $element.width());
                
                var $element = $(me.$elements.get(me.$elements.length-1));
                $element.data('left', end - $element.width()*2);
            
            } else if (me.previous_element < me.current_element) {
            
                var $element = $(me.$elements.get(me.previous_element));
                $element.data('left', $element.width() * (-1));
            
                var $element = $(me.$elements.get(me.current_element));
                $element.data('left', 0);
                
            } else if (me.previous_element > me.current_element) {
            
                var $element = $(me.$elements.get(me.previous_element));
                $element.data('left', $element.width());
            
                var $element = $(me.$elements.get(me.current_element));
                $element.data('left', 0);
                
            }
        }
        
        me.previous_element = me.current_element;
    }
    
    /**
     * Sets the next element to be the me.current_element.
     */
    Slider.prototype.next = function(event) {
        
        if (typeof event != "undefined") event.stopImmediatePropagation();
        
        var me = this.me;
        
        if (me.animating) return;
        if (me.$elements.length <= 1) return;
        if (me.disabled || (me.$next && me.$next.hasClass('disabled'))) return;
        
        me.previous_element = me.current_element;
        me.current_element++;
        if (me.current_element >= me.$elements.length) {
            if (!me.loop) me.current_element = me.$elements.length - 1;   
            else me.current_element = 0;
        }
        
        me.styleIt(true);
        
        return false;
    }
    
    /**
     * Sets the previous element to be the me.current_element.
     */
    Slider.prototype.prev = function(event) {
        
        var me = this.me;
        
        if (me.animating) return;
        if (me.$elements.length <= 1) return;
        if (me.disabled || (me.$prev && me.$prev.hasClass('disabled'))) return;
        
        me.previous_element = me.current_element;
        me.current_element--;
        if (me.current_element < 0) {
            if (!me.loop) me.current_element = 0;
            else me.current_element = me.$elements.length - 1;
        }
        
        me.styleIt(true);
    }
    
    /**
     * Checks if the next/prev buttons should be enabled/disabled.
     * Adds or removes the class "disabled".
     */
    Slider.prototype.checkNextPrev = function() {
            
        var me = this.me;
        
        if (!me.loop && me.$prev) {
            
            var $first = $(me.$elements.get(0));
            var $last = $(me.$elements.get(me.$elements.length-1));
            
            if ($first.position().left >= me.margin*(-1)) me.$prev.addClass('disabled');
            else me.$prev.removeClass('disabled');
            
            if ($last.position().left + $last.width() <= me.$wrapper.width() + me.margin) me.$next.addClass('disabled');
            else me.$next.removeClass('disabled');
            
        }
    }
    
    $('.slider').each(function() {
        new Slider($(this)); 
    });
    
})();