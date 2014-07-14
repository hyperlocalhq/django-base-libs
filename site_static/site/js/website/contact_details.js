(function($, undefined) {
        
    self.ContactDetailsManager = {
        iEmailCount: 3,
        iURLCount: 3,
        iIMCount: 3,
        init: function() {
            var oSelf = self.ContactDetailsManager;
            for (i=1; i<3; i++) {
                var $oF = $("#id_email" + i);
                if (!$oF.length) {
                    return;
                }
                if (!$oF.val()) {
                    $oF.parents(".ctrlHolder").css("display", "none");
                    oSelf.iEmailCount--;
                }
                $oF = $("#id_url" + i + "_link");
                if (!$oF.val()) {
                    $oF.parents(".ctrlHolder").css("display", "none");
                    oSelf.iURLCount--;
                }
                $oF = $("#id_im" + i + "_address");
                if (!$oF.val()) {
                    $oF.parents(".ctrlHolder").css("display", "none");
                    oSelf.iIMCount--;
                }
            }
            /* javascript-based email managing */
            var $oLi = $('<p class="dyn_contact_managing">').appendTo($("#id_email0").parents(".ctrlHolders"));
            $(
                '<a href="#Remove-Email" id="email_remover">'+ gettext("Remove email") +'</a> '
            ).css(
                "display", oSelf.iEmailCount>1? "inline": "none"
            ).click(oSelf.remove_email).appendTo($oLi);
            $(document.createTextNode(" ")).appendTo($oLi);
            $(
                '<a href="#Add-Email" id="email_adder">'+ gettext("Add email") +'</a>'
            ).css(
                "display", oSelf.iEmailCount<3? "inline": "none"
            ).click(oSelf.add_email).appendTo($oLi);
            
            /* javascript-based url managing */
            var $oLi = $('<p class="dyn_contact_managing">').appendTo($("#id_url0_link").parents(".ctrlHolders"));
            $(
                '<a href="#Remove-URL"  id="url_remover">'+ gettext("Remove URL") +'</a>'
            ).css(
                "display", oSelf.iURLCount>1? "inline": "none"
            ).click(oSelf.remove_url).appendTo($oLi);
            $(document.createTextNode(" ")).appendTo($oLi);
            $(
                '<a href="#Add-URL"  id="url_adder">'+ gettext("Add URL") +'</a>'
            ).css(
                "display", oSelf.iURLCount<3? "inline": "none"
            ).click(oSelf.add_url).appendTo($oLi);
    
            /* javascript-based im managing */
            var $oLi = $('<p class="dyn_contact_managing">').appendTo($("#id_im0_address").parents(".ctrlHolders"));
            $(
                '<a href="#Remove-IM" id="im_remover">'+ gettext("Remove IM") +'</a>'
            ).css(
                "display", oSelf.iIMCount>1? "inline": "none"
            ).click(oSelf.remove_im).appendTo($oLi);
            $(document.createTextNode(" ")).appendTo($oLi);
            $(
                '<a href="#Add-IM" id="im_adder">'+ gettext("Add IM") +'</a> '
            ).css(
                "display", oSelf.iIMCount<3? "inline": "none"
            ).click(oSelf.add_im).appendTo($oLi);
        },
        add_email: function() {
            var oSelf = self.ContactDetailsManager;
            $("#id_email" + oSelf.iEmailCount).parents(".ctrlHolder").css("display", "block");
            oSelf.iEmailCount++;
            if (oSelf.iEmailCount > 1) {
                $("#email_remover").css("display", "inline");
                $("#email_adder").addClass("separated");
            } 
            if (oSelf.iEmailCount >= 3) {
                $("#email_adder").css("display", "none");
            }
            return false;
        },
        remove_email: function() {
            var oSelf = self.ContactDetailsManager;
            oSelf.iEmailCount--;
            $("#id_email" + oSelf.iEmailCount).val("").parents(".ctrlHolder").css("display", "none").find('p.error').remove();
            if (oSelf.iEmailCount <= 1) {
                $("#email_remover").css("display", "none");
                $("#email_adder").removeClass("separated");
            } 
            if (oSelf.iEmailCount < 3) {
                $("#email_adder").css("display", "inline");
            } 
            return false;
        },
        add_url: function() {
            var oSelf = self.ContactDetailsManager;
            $("#id_url" + oSelf.iURLCount + "_link").parents(".ctrlHolder").css("display", "block");
            oSelf.iURLCount++;
            if (oSelf.iURLCount > 1) {
                $("#url_remover").css("display", "inline");
                $("#url_adder").addClass("separated");
            }                                              
            if (oSelf.iURLCount >= 3) {
                $("#url_adder").css("display", "none");
            } 
            return false;
        },
        remove_url: function() {
            var oSelf = self.ContactDetailsManager;
            oSelf.iURLCount--;
            $("#id_url" + oSelf.iURLCount + "_link").val("").parents(".ctrlHolder").css("display", "none").find('p.error').remove();
            $("#id_url" + oSelf.iURLCount + "_type").val("");
            if (oSelf.iURLCount <= 1) {
                $("#url_remover").css("display", "none");
                $("#url_adder").removeClass("separated");
            } 
            if (oSelf.iURLCount < 3) {
                $("#url_adder").css("display", "inline");
            } 
            return false;
        },
        add_im: function() {
            var oSelf = self.ContactDetailsManager;
            $("#id_im" + oSelf.iIMCount + "_address").parents(".ctrlHolder").css("display", "block");
            $("#id_im" + oSelf.iIMCount + "_type").val("");
            oSelf.iIMCount++;
            if (oSelf.iIMCount > 1) {
                $("#im_remover").css("display", "inline");
                $("#im_adder").addClass("separated");
            } 
            if (oSelf.iIMCount >= 3) {
                $("#im_adder").css("display", "none");
            } 
            return false;
        },
        remove_im: function() {
            var oSelf = self.ContactDetailsManager;
            oSelf.iIMCount--;
            $("#id_im" + oSelf.iIMCount + "_address").val("").parents(".ctrlHolder").css("display", "none").find('p.error').remove();
            $("#id_im" + oSelf.iIMCount + "_type").val("");
            if (oSelf.iIMCount <= 1) {
                $("#im_remover").css("display", "none");
                $("#im_adder").removeClass("separated");
            } 
            if (oSelf.iIMCount < 3) {
                $("#im_adder").css("display", "inline");
            } 
            return false;
        },
        destruct: function() {
            self.ContactDetailsManager = null;
        }
    };
 
    $(document).ready(function(){
        self.ContactDetailsManager.init();
    });
    
    $(window).unload(function() {
        self.ContactDetailsManager.destruct();
    });

    
}(jQuery));
