(function($, undefined) {

    self.ContactManager = {
        init: function() {
            var oSelf = self.ContactManager;
            /* javascript-based additional contact managing */
            var iContactCount = 0;
            for (i=0; i<6; i++) {
                $oF = $("#id_p" + i + "_first_name");
                if ($oF.val()) {
                    $oF.parents(".dyn_additional_contact:first").show();
                    iContactCount++;
                } else {
                    break;
                }
            }
            var $oLi = $('<li class="dyn_contact_managing">').appendTo($(".dyn_additional_contact:first").parent());
            $(
                '<a href="#Remove-Contact" id="dyn_contact_remover">'+ gettext("Remove contact") +'</a> '
            ).css(
                "display", iContactCount>1? "inline": "none"
            ).click(oSelf.remove_contact).appendTo($oLi);
            $(document.createTextNode(" ")).appendTo($oLi);
            $(
                '<a href="#Add-Contact" id="dyn_contact_adder">'+ gettext("Add contact") +'</a>'
            ).css(
                "display", iContactCount<5? "inline": "none"
            ).click(oSelf.add_contact).appendTo($oLi);
            
            /* organizing institution is selected from autocomplete field */
            $("#id_institution").blur(oSelf.completeInstitutionContact);
            
            $("#id_first_name,#id_last_name").keyup(oSelf.prepopulate_username);
        },
        prepopulate_username: function() {
            var sFirstName = $("#id_first_name").val();
            var sLastName = $("#id_last_name").val();
            $("#id_username").val(
                URLify(
                    sFirstName
                    + (sFirstName && sLastName? "_": "")
                    + sLastName,
                    40
                )
            );
        },
        add_contact: function() {
            var oSelf = self.ContactManager;
            var iIndex = $(".dyn_additional_contact:visible").length;
            $(".dyn_additional_contact:eq(" + iIndex + ")").slideDown("normal");
            if (iIndex >= 1) {
                $("#dyn_contact_remover").css("display", "inline");
                $("#dyn_contact_adder").addClass("separated");
            } 
            if (iIndex >= 4) {
                $("#dyn_contact_adder").css("display", "none");
            }
            return false;
        },
        remove_contact: function() {
            var oSelf = self.ContactManager;
            var iIndex = $(".dyn_additional_contact:visible").length - 1;
            if (iIndex >= 1) {
                $(".dyn_additional_contact:eq(" + iIndex + ")").slideUp("normal").find('p.error').remove();
                if (iIndex == 1) {
                    $("#dyn_contact_remover").css("display", "none");
                    $("#dyn_contact_adder").removeClass("separated");
                } 
                if (oSelf.iEmailCount < 4) {
                    $("#dyn_contact_adder").css("display", "inline");
                }
            }
            return false;
        },
        completeInstitutionContact: function() {
            var oSelf = self.ContactManager;
            if ($(this).val()) {
                $j.get(
                    "/helper/accounts/" + settings.URL_ID_INSTITUTION + "_attrs/" + $("#id_institution").val() + "/",
                    oSelf.fillInInstitutionContactData
                );
                return false;
            }
        },
        fillInInstitutionContactData: function(sData) {
            var oSelf = self.ContactManager;
            eval("var oData = " + sData);
            
            // fill in data
            if (oData.location_type) {
                $("#id_location_type").val(oData.location_type.id);
            }
            $("#id_street_address").val(oData.street_address);
            if (oData.street_address2) { 
                $("#id_street_address2").val(oData.street_address2);
            }
            $("#id_postal_code").val(oData.postal_code);
            $("#id_city").val(oData.city);		
            $("#id_country").val(oData.country);
            
            for (i=0; i<3; i++) {
                if (oData["url" + i + "_link"]) {
                    $("#id_url" + i + "_link").val(oData["url" + i + "_link"]);
                }
                if (oData["im" + i + "_address"]) {
                    $("#id_im" + i + "_type").val(oData["im" + i + "_type"]);
                    $("#id_im" + i + "_link").val(oData["im" + i + "_address"]);
                }
            }
            if (oData.phone_number) {
                $("#id_phone_country").val(oData.phone_country);
                $("#id_phone_area").val(oData.phone_area);
                $("#id_phone_number").val(oData.phone_number);
            }
            if (oData.fax_number) {
                $("#id_fax_country").val(oData.fax_country);
                $("#id_fax_area").val(oData.fax_area);
                $("#id_fax_number").val(oData.fax_number);
            }
            if (oData.mobile_number) {
                $("#id_mobile_country").val(oData.mobile_country);
                $("#id_mobile_area").val(oData.mobile_area);
                $("#id_mobile_number").val(oData.mobile_number);
            }
            
        },
        destruct: function() {
            self.ContactManager = null;
        }
    };
    
    self.MainDataManager = {
        init: function() {
            $(
                "#id_privacy_policy,#id_terms_of_use"
            ).siblings("label").children("a").click(open_new_window);
        },
        destruct: function() {
            self.MainDataManager = null;
        }
    };
    
    $(document).ready(function(){
        self.MainDataManager.init();
        self.ContactManager.init();
    });
    
    $(window).unload(function() {
        self.MainDataManager.destruct();
        self.ContactManager.destruct();
    });
    
}(jQuery));
