/**
 * Handles the functionality of the event times input page.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function EventTimes($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$is_all_day = $('.is-all-day', me.$main);
        
        me.$is_all_day.off().change(function() {me.toggle();});
        me.toggle();
    }
    
    EventTimes.prototype.toggle = function() {
     
        var me = this.me;
        
        me.$is_all_day.each(function() {
            
            var $button = $(this);
            var $item = $button.closest('.entry');
            
            if ($button.prop('checked')) {
                $('.hours', $item).css('display', 'none');                
            } else {
                $('.hours', $item).css('display', '');  
            }
            
        });
    }
    
    $('.fieldset.event-times').each(function() {
        new EventTimes($(this)); 
    });
    
    
    window.addToFormInit(function() {
    
        $('.fieldset.event-times').each(function() {
            new EventTimes($(this)); 
        });    
    });
    
})();