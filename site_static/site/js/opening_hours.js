/**
 * Handles the functionality of the opening hours input page.
 *
 * @author Daniel Lehmann
 */


(function() {

    function OpeningHours($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$break_button = $('#id_show_breaks', me.$main);
        me.$closed_buttons = $('.closed', me.$main);
        
        me.days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
        me.types = ["_open0", "_close0", "_open1", "_close1"];
        
        me.$break_button.change(function() {me.toggle();});
        me.$closed_buttons.change(function() {me.toggle();});
        $('#apply_to_all_days', me.$main).click(function() {me.applyToAllDays(); return false;});
        
        me.toggle();
    }
    
    OpeningHours.prototype.toggle = function() {
     
        var me = this.me;
        
        var show_breaks = me.$break_button.prop('checked');
        
        me.$closed_buttons.each(function() {
         
            var $button = $(this);
            var checked = $button.prop('checked');
            
            var day = "";
            for (var i=0, length=me.days.length; i<length; i++) {
                if ($button.hasClass(me.days[i])) {
                    day = me.days[i];
                    break;
                }
            }
            
            var $inputs = $('.closed_'+day, me.$main);
            var $break = $('.break.closed_'+day, me.$main);
        
            if (!checked) {
                $inputs.css('display', '');   
                if (!show_breaks) $break.css('display', 'none');
            } else {
                $inputs.css('display', 'none');   
            }
        });
    }
    
    OpeningHours.prototype.applyToAllDays = function() {
        
        var me = this.me;
        
        var values = [];
        var closed = $('#id_mon_is_closed', me.$main).prop('checked');
        
        for (var i=0, length=me.types.length; i<length; i++) {
            values[i] = $("#id_mon"+me.types[i], me.$main).get(0).value;   
        }
        
        for (var d=1, length=me.days.length; d<length; d++) {
            for (var i=0, t_length=me.types.length; i<t_length; i++) {
                $("#id_"+me.days[d]+me.types[i], me.$main).get(0).value = values[i];
            }
            $("#id_"+me.days[d]+"_is_closed", me.$main).prop('checked', closed);
        }
        
        me.toggle();
    }
    
    $('.fieldset.opening-hours').each(function() {
        new OpeningHours($(this)); 
    });

}());
