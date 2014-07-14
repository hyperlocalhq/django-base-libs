(function($, undefined) {

    self.EventTimesManager = {
        
        fillInContactData : true,
        
        init: function() {
            var oSelf = self.EventTimesManager;
            
            $('input[id^=id_event_times][id$=is_all_day]').change(function() {
                oSelf.showHideAllday(this);
            }).each(function() {
                oSelf.showHideAllday(this);
            });
            
            $('.event_end').each(function(i) {
                var hasValue = false
                $('select', this).each(function() {
                    if ($(this).val()) hasValue = true;
                });
                if (hasValue) {
                    $(this).parent().find('input.toggle_event_end').attr('checked', true);
                } else {
                    $(this).hide();
                }
            });
            $('.toggle_event_end').change(function() {
                var $oEndDateField = $(this).parents('.ctrlHolder').next('.event_end');
                if ($(this).attr('checked')) {
                    $oEndDateField.slideDown();
                    
                    $(this).parents(".ctrlHolder").find(
                        'input[id^=id_event_times][id$=is_all_day]'
                    ).attr("checked", true).change();
                    
                } else {
                    $oEndDateField.slideUp();
                }
            });
        },
        
        showHideAllday: function(checkbox) {
            if ($(checkbox).attr("checked")) {
                $(checkbox).parents('.event_time').find(
                    'select[id$=start_hh], select[id$=start_ii], select[id$=end_hh], select[id$=end_ii]'
                ).val('').parents(".ctrlHolder").slideUp();
            } else {
                $(checkbox).parents('.event_time').find(
                    'select[id$=start_hh], select[id$=start_ii], select[id$=end_hh], select[id$=end_ii]'
                ).parents(".ctrlHolder").slideDown();
            }
        },
        
        destruct: function() {
            self.EventTimesManager = null;
        }
    };
    
    $(document).ready(function(){
        self.EventTimesManager.init();
    });
    
    $(window).unload(function() {
        self.EventTimesManager.destruct();
    });
    
}(jQuery));
