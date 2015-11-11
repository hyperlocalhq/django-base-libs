(function($, undefined) {

    var gDaysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
        
    self.OpeningHoursManager = {
        init: function() {
            var oSelf = self.OpeningHoursManager;
    
            /* show breaks event */        
            $("#id_show_breaks").change(function() {
                /*
                change the class of <div class="field_info">...
                to class of <div class="field_info breaks_shown">...
                when checked vice versa
                */
                if ($(this).attr("checked"))
                    $(".field_info").addClass("breaks_shown");
                else
                    $(".field_info").removeClass("breaks_shown");
            
                for (i=0; i<7; i++) {
                    oSelf.toggleOpeningHours(gDaysOfWeek[i]);
                }
            });
            
            /* is_closed event */
            for (i=0; i<7; i++) {
                $("#id_" + gDaysOfWeek[i] + "_is_closed").change(function() {
                    var sDay = $(this).attr("id").match(/id_(.+)_is_closed$/)[1];
                    
                    /*
                    change the class of the parent div of "id_xxx_is_closed"
                    from <div class="left">... to <div class="left is_closed">...
                    when checked vice versa. Tobi needs that for styling...
                    */
                    if ($(this).attr("checked")) 
                        $(this).parent().parent().addClass("is_closed");
                    else
                        $(this).parent().parent().removeClass("is_closed");
                    
                    oSelf.toggleOpeningHours(sDay);
                });
            }
            
            /* apply opening hours to all days */
            $("#id_apply_all_days").click(function() {
                var sMon = gDaysOfWeek[0];
                var sMonOpen0 = $("#id_" + sMon + "_open0").val();
                var sMonOpen1 = $("#id_" + sMon + "_open1").val();
                var sMonClose0 = $("#id_" + sMon + "_close0").val();
                var sMonClose1 = $("#id_" + sMon + "_close1").val();
                var bMonClosed = $("#id_" + sMon + "_is_closed").get(0).checked;
                for (i=1; i<7; i++) {
                    var sDay = gDaysOfWeek[i];
                    $("#id_" + sDay + "_open0").val(sMonOpen0);
                    $("#id_" + sDay + "_close0").val(sMonClose0);
                    $("#id_" + sDay + "_open1").val(sMonOpen1);
                    $("#id_" + sDay + "_close1").val(sMonClose1);
                    var $oIsClosed = $("#id_" + sDay + "_is_closed");
                    $oIsClosed.attr("checked", bMonClosed);
                    $oIsClosed.change();
                }
                return false;
            });
    
            /* init show-hide opening hours */
            for (i=0; i<7; i++) {
                var sDay = gDaysOfWeek[i];
                oSelf.toggleOpeningHours(sDay);
                if ($("#id_" + sDay + "_is_closed").attr("checked")) 
                    $("#id_" + sDay + "_is_closed").parent().parent().addClass("is_closed");
                else
                    $("#id_" + sDay + "_is_closed").parent().parent().removeClass("is_closed");
            }
            
            /* init show breaks */
            if ($("#id_show_breaks").attr("checked"))
                $(".field_info").addClass("breaks_shown");
            else
                $(".field_info").removeClass("breaks_shown");
        },
        
        destruct: function() {
            self.OpeningHoursManager = null;
        },
        
        /* toggleOpeningHours */
        toggleOpeningHours: function(sDay) {
            var $oOpen0 = $("#id_" + sDay + "_open0");
            var $oClose0 = $("#id_" + sDay + "_close0");
            var $oOpen1 = $("#id_" + sDay + "_open1");
            var $oClose1 = $("#id_" + sDay + "_close1");
            if ($("#id_" + sDay + "_is_closed").attr("checked")) {
                $oOpen0.val("").parent().addClass("invisible"); //hide();
                $oClose0.val("").parent().addClass("invisible"); //hide();
                $oOpen1.val("").parents(".ctrlHolder").hide();
                $oClose1.val("");
                $("#id_" + sDay + "_errors").hide();
                $("#id_" + sDay + "_break_errors").hide();
            } else {
                $oOpen0.parent().removeClass("invisible"); //show();
                $oClose0.parent().removeClass("invisible"); //show();
                $("#id_" + sDay + "_errors").show();
                if ($("#id_show_breaks").attr("checked")) {
                    $oOpen1.parents(".ctrlHolder").show();
                    $("#id_" + sDay + "_break_errors").show();
                } else {
                    $oOpen1.val("").parents(".ctrlHolder").hide();
                    $oClose1.val("");
                    $("#id_" + sDay + "_break_errors").hide();
                }
            }
        }
    };

    $(document).ready(function(){
        self.OpeningHoursManager.init();
    });
    
    $(window).unload(function() {
        self.OpeningHoursManager.destruct();
    });

}(jQuery));
