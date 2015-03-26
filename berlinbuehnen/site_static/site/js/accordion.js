/**
 * ...
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
        me.$main = $main;
        me.$items = $('.accordion-item', $main);
        
        me.$items.each(function() {
            
            var $item = $(this);
            var $head = $('.accordion-item-head', $item);
            var $content = $('.accordion-item-content', $item);
            
            var $content_wrapper = $('<div style="overflow:hidden; transition: height 0.4s ease-out 0s;"/>');
            $content_wrapper.append($content);
            $item.append($content_wrapper);
            
            $content.css('height', 'auto');
            $content.css('display', 'block');
            var height = $content_wrapper.height();
            
            if ($head.hasClass('open')) $content_wrapper.height(height);
            else $content_wrapper.height(1);
            
            $content_wrapper.data('height', height);
            
            $head.data('me', me);
            $head.data('content', $content_wrapper);
            $head.click(me.click);
        });
    }
    
    Accordion.prototype.click = function() {
        
        var $head = $(this);
        var me = $head.data('me');
        var $content = $head.data('content');
        var open = $head.hasClass('open');
        
        if (open) {
            
            $content.height(1);
            $head.removeClass('open');
            
        } else {
            
            $('.accordion-item-head', me.$main).removeClass('open');
            $('.accordion-item-content', me.$main).parent().height(1);
        
            $content.height($content.data('height'));
            $head.addClass('open');
        }
    }
    
    function init() {
        
        $('.accordion').each(function() {
            new Accordion($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();