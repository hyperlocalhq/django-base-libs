/**
 * Provides functionality to the pagination menu.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function Pagination($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$li = $('li', me.$main);
        me.$first = me.$li.first();
        me.$last = me.$li.last();
        me.$pages = $('li.page', me.$main);
        
        $(window).resize(function() {me.setWidth(100);});
        me.setWidth(200);
        me.setWidth();
    }
    
    Pagination.prototype.setWidth = function(delay) {
     
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.setWidth();}, delay);
            return;
        }
        
        me.$pages.removeClass('hidden');
        
        var first_top = me.$first.position().top;
        var last_top = me.$last.position().top;
        var $pages = $('li.page', me.$main).not('.hidden');
        
        while (first_top != last_top && $pages.length) {
            
            var active = 0;
            $pages.each(function(index) {
                if ($(this).hasClass('active')) {
                    active = index;
                    return false;
                }
            });
            
            if ($pages.length / 2 <= active) {
                $pages.first().addClass('hidden');   
            } else { 
                $pages.last().addClass('hidden');  
            }
            
            first_top = me.$first.position().top;
            last_top = me.$last.position().top;
            $pages = $('li.page', me.$main).not('.hidden');
            
        }
    }
    
    $('.pagination').each(function() {
        new Pagination($(this)); 
    });
    
    
})();