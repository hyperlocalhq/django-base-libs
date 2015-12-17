/**
 * Provides functionality and styles for the event list.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function EventList($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$elements = $('.col-xs-12', $main);
        me.$body = $('body');
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt(200);});
        me.styleIt();
    }
    
    EventList.prototype.styleIt = function(delay) {
     
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $content = $('.content', $element);
            var $website = $('.website', $element);
            
            if ($website.length) {
            
                var $p = $('p', $content);
                
                var margin = 5;
                
                $p.css('margin-bottom', ($website.height() + margin) + 'px');
                $website.css('top', ($p.position().top + $p.height()) + margin + 'px');
                
            }
            
        });
    }
    
    $('.event-list').each(function() {
        new EventList($(this)); 
    });    
    
})();