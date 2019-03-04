/**
 * Provides functionality and styles for the navigation grid.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function NaviGrid($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$elements = $('.content', me.$main);
        me.$all_small_text = $('.col-xs-6 h2', me.$main);
        me.$all_big_text = $('.col-xs-12 h2', me.$main);
        me.$body = $('body');
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt();});
        me.styleIt();
        
    }
    
    NaviGrid.prototype.styleIt = function(delay) {
        
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        if (me.$body.hasClass('is-xs')) {
            var factor = me.$main.width() / 610;
            me.$all_small_text.css('font-size', (factor * 1.87) + "em");
            me.$all_big_text.css('font-size', (factor * 2.8) + "em");
        } else {
            me.$all_small_text.css('font-size', '');
            me.$all_big_text.css('font-size', '');
        }
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $text = $('h2', $element);
            var $over = $('p', $element);
            
            var text_height = Math.round($text.height() / 2);
            var offset = text_height * 0.2;
            $text.css('margin-top', "-" + Math.round(text_height + offset) + "px");
            $over.css('margin-top', Math.round(text_height+10 - offset) + "px");
            
        });
    }
    
    $('.navi-grid').each(function() {
        new NaviGrid($(this)); 
    });
    
})();