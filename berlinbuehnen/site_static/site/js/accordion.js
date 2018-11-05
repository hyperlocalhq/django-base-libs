/**
 * Initiates all accordions.
 * Add the class "open" to each accordion item which should be open at the beginning.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the accordion which contains the $('.accordion-item') objects.
     *
     * @param   $main   the jQuery object of the accordion wrapper
     */
    function Accordion($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.autoclose = $main.hasClass('accordion-autoclose');
        me.$items = $('.accordion-item', $main);
        me.last_width = -1;
        
        me.$items.each(function() {
            
            var $item = $(this);
            var $head = $('.accordion-item-head', $item);
            var $content = $('.accordion-item-content', $item);
            
            var $content_wrapper = $('<div class="accordion-item-content-wrapper" style="overflow:hidden; -webkit-transition: height 0.4s ease-out 0s; transition: height 0.4s ease-out 0s;"/>');
            $content_wrapper.append($content);
            $item.append($content_wrapper);
            
            $content.css('height', 'auto');
            $content.css('display', 'block');
            
            $head.data('me', me);
            $head.data('content', $content_wrapper);
            $head.click(me.click);
            
            $('img', $content).load(function() {me.initHeights();});
        });
        
        me.onResize();
        $(window).resize(function() {me.onResize();});
        me.$main.data('accordion', me);
    }
    
    /**
     * Initialises the accordion content heights.
     */
    Accordion.prototype.initHeights = function() {
        
        if (this.me) var me = this.me;
        
        me.$items.each(function() {
            
            var $item = $(this);
            var $head = $('.accordion-item-head', $item);
            var $content_wrapper = $('.accordion-item-content-wrapper', $item);
            
            $item.css('display', 'block');
            $content_wrapper.css('height', 'auto');
            var height = $content_wrapper.height();
            
            if ($head.hasClass('open')) $content_wrapper.height(height);
            else $content_wrapper.height(1);
            
            $content_wrapper.data('height', height);        
            
            if (height == 0) $item.css('display', 'none');
        });
    }
    
    /**
     * An accordion head got clicked.
     */
    Accordion.prototype.click = function() {
        
        var $head = $(this);
        var me = $head.data('me');
        var $content = $head.data('content');
        var open = $head.hasClass('open');
        
        if (open) {
            
            $content.height(1);
            $head.removeClass('open');
            
        } else {
            
            if (me.autoclose) {
                $('.accordion-item-head', me.$main).removeClass('open');
                $('.accordion-item-content', me.$main).parent().height(1);
            }
        
            $content.height($content.data('height'));
            $head.addClass('open');
        }
    }
    
    /**
     * The window got resized.
     */
    Accordion.prototype.onResize = function() {
        
        if (this.me) var me = this.me;
        
        var new_width = me.$main.width();
        
        if (new_width != me.last_width) {
            me.last_width = new_width;
            me.initHeights();            
        }
    }
    
    function init() {
        
        $('.accordion').each(function() {
            new Accordion($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();