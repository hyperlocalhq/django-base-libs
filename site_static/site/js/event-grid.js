/**
 * Provides styles for the event grid/row.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function EventGrid($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$elements = $('.content', me.$main);
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt();});
        me.styleIt();       
        me.styleIt(300);
    }
    
    EventGrid.prototype.styleIt = function(delay) {
        
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $headline = $('h2', $element);
            var $paragraph = $('p', $element);
            
            var headline_height = Math.round($headline.height());
            var paragraph_height = Math.round($paragraph.height());
            var text_height = ((headline_height + paragraph_height + 10) / 2) * (-1);
            
            $headline.css('margin-top', text_height + "px");
            $paragraph.css('margin-top', (text_height + headline_height + 10) + "px");
            
        });
    }
    
    $('.event-grid').each(function() {
        new EventGrid($(this)); 
    });    
    
})();