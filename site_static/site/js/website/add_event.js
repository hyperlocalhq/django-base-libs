(function($, undefined) {

    self.EventMainDataManager = {
        
        fillInContactData : true,
        
        init: function() {
            var oSelf = self.EventMainDataManager;
            
            $("#id_venue").blur(oSelf.completeVenueContact);
            if ($("#id_venue").val()) {
                $("#id_venue").blur();
            }
            
            /* link to manual input of venue data */
            $("#id_venue_not_listed").click(function() {
                oSelf.manageVenueBlocks("noVenueSelected");
                $("#id_venue").val("");
                $("#id_venue_text").val("");
                return false;
            });
            
            /* link back to selection */
            $("#id_venue_select").click(function() {
                oSelf.manageVenueBlocks("selectVenue");
                $("#id_block_venue_name_input input").val("");
                $("#id_block_venue_address_input input").val("");
                $("#id_block_venue_contact_input input").val("");		        
                return false;
            });
            
            /* link to "choose a different venue" */
            $("#id_venue_change").click(function() {
                oSelf.manageVenueBlocks("selectVenue");
                $("#id_venue_text").click();
                return false;
            });
            
            /* organizer_ind radio buttons events */
            $("#id_organizer_ind_0").change(function() {
                oSelf.manageOrgInstBlocks("orgInstNotRelevant");
                $("#id_organizing_institution").val("");
                $("#id_organizing_institution_text").val("");
                $("#id_block_org_inst_data_input input").val("");
                return false;
            });
            $("#id_organizer_ind_1").change(function() {
                oSelf.manageOrgInstBlocks("selectOrgInst");
                return false;
            });
            $("#id_organizer_ind_2").change(function() {
                oSelf.manageOrgInstBlocks("orgInstNotRelevant");
                $("#id_organizing_institution").val("");
                $("#id_organizing_institution_text").val("");
                $("#id_block_org_inst_data_input input").val("");
                return false;
            });
            
            /* organizing institution is selected from autocomplete field */
            $("#id_organizing_institution").blur(oSelf.completeOrgInstContact);
            if ($("#id_organizing_institution").val()) {
                $("#id_organizing_institution").blur();
            }
            
            /* link to manual input of organizing institution data */
            $("#id_org_inst_not_listed").click(function() {
                oSelf.manageOrgInstBlocks("noOrgInstSelected");
                $("#id_organizing_institution").val("");
                $("#id_organizing_institution_text").val("");
                return false;
            });
            
            /* link back to selection */
            $("#id_org_inst_select").click(function() {
                oSelf.manageOrgInstBlocks("selectOrgInst");
                $("#id_block_org_inst_data_input input").val("");
                return false;
            });
            
            /* link to "choose a different organizing institution" */
            $("#id_org_inst_change").click(function() {
                oSelf.manageOrgInstBlocks("selectOrgInst");
                $("#id_organizing_institution_text").click();
                return false;
            });
    
            /* initial situation */    	
            if ($("#id_venue_title").val() != "") {
                oSelf.manageVenueBlocks("noVenueSelected");
            } else { 
                if ($("#id_venue").val() != "") {
                    oSelf.manageVenueBlocks("venueSelected");
                    oSelf.fillInContactData = false;
                } else {
                    oSelf.manageVenueBlocks("selectVenue");
                }
            }
    
            if ($("input[name='organizer_ind']:checked").val()!=1) {
                oSelf.manageOrgInstBlocks("orgInstNotRelevant");
            } else { 
                if ($("#id_organizer_title").val() != "") {
                    oSelf.manageOrgInstBlocks("noOrgInstSelected");
                } else { 
                    if ($("#id_organizing_institution").val() != "") {
                        oSelf.manageOrgInstBlocks("orgInstSelected");
                    } else {
                        oSelf.manageOrgInstBlocks("selectOrgInst");
                    }
                }
            }
        },
        
        manageVenueBlocks: function(sCase) {
            switch (sCase) {
                case "selectVenue":
                    $("#id_block_venue_select").show();
                    $("#id_block_venue_name_input").hide();
                    $("#id_block_venue_address_input").hide();
                    $("#id_block_venue_address_display").hide();
                    $("#id_block_venue_contact_input").hide();
                    break;
                case "noVenueSelected":
                    $("#id_block_venue_select").hide();
                    $("#id_block_venue_name_input").show();
                    $("#id_block_venue_address_input").show();
                    $("#id_block_venue_address_display").hide();
                    $("#id_block_venue_contact_input").show();
                    break;
                case "venueSelected":
                    $("#id_block_venue_select").hide();
                    $("#id_block_venue_name_input").hide();
                    $("#id_block_venue_address_input").hide();
                    $("#id_block_venue_address_display").show();
                    $("#id_block_venue_contact_input").show();
                    break;
                default: 
                    document.write("No case is selected!!!! case='" + sCase + "'");
                    break; 
            }
        },
        
        manageOrgInstBlocks: function(sCase) {
            switch (sCase) {
                case "orgInstNotRelevant":
                    $("#id_block_org_inst_select").hide();
                    $("#id_block_org_inst_address_display").hide();
                    $("#id_block_org_inst_data_input").hide();
                    break;	  			
                case "selectOrgInst":
                    $("#id_block_org_inst_select").show();
                    $("#id_block_org_inst_address_display").hide();
                    $("#id_block_org_inst_data_input").hide();
                    break;
                case "noOrgInstSelected":
                    $("#id_block_org_inst_select").hide();
                    $("#id_block_org_inst_address_display").hide();
                    $("#id_block_org_inst_data_input").show();
                    break;
                case "orgInstSelected":
                    $("#id_block_org_inst_select").hide();
                    $("#id_block_org_inst_address_display").show();
                    $("#id_block_org_inst_data_input").hide();
                    break;		        
                default: 
                    document.write("No case is selected!!!! case='" + sCase + "'");
                    break; 
            }
        },
             
        completeVenueContact: function() {
            var oSelf = self.EventMainDataManager;
            if ($(this).val()) {
                $.get(
                    "/helper/"+ settings.URL_ID_EVENT +"/"+ settings.URL_ID_INSTITUTION +"_attrs/" + $("#id_venue").val() + "/",
                    new Function("oData", "self.EventMainDataManager.fillInVenueContactData(oData)"),
                    "json"
                );
                return false;
            }
        },
        
        completeOrgInstContact: function() {
            var oSelf = self.EventMainDataManager;
            if ($(this).val()) {
                $.get(
                    "/helper/"+ settings.URL_ID_EVENT +"/"+ settings.URL_ID_INSTITUTION +"_attrs/" + $("#id_organizing_institution").val() + "/",
                    new Function("oData", "self.EventMainDataManager.fillInOrgInstContactData(oData)"),
                    "json"
                );
                return false;
            }
        },
            
        fillInVenueContactData: function(oData) {
            var oSelf = self.EventMainDataManager;
            
            // show correct blocks
            oSelf.manageVenueBlocks("venueSelected");
    
            // fill in data
            oSelf.setText($("#id_venue_address_title"), oData.title);
            oSelf.setText($("#id_venue_address_street_address"), oData.street_address);
            if (oData.street_address2) 
                oSelf.setText($("#id_venue_address_street_address2"), oData.street_address2);
            else
                $("#id_venue_address_street_address2").hide();
            oSelf.setText($("#id_venue_address_postal_code"), oData.postal_code);
            oSelf.setText($("#id_venue_address_city"), oData.city);		
            oSelf.setText($("#id_venue_address_country"), oData.country_name);

            $("#id_latitude").val(oData.latitude);
            $("#id_longitude").val(oData.longitude);
            if (self.GMapManager) {
                self.GMapManager.adjustGeoposition();
            }
            
            /*
            updating the address, email and url data not at the initial call!
            we need that for form validation (otherwise, any entered data would be
            overwritten
            */
            if (oSelf.fillInContactData) {
                
                $("#id_email0_address").val(oData.email0_address);
                $("#id_url0_link").val(oData.url0_link);
                
                if (oData["phone_number"]) {
                    $("#id_phone_country").val(oData["phone_country"]);
                    $("#id_phone_area").val(oData["phone_area"]);
                    $("#id_phone_number").val(oData["phone_number"]);
                }

                if (oData["fax_number"]) {
                    $("#id_fax_country").val(oData["fax_country"]);
                    $("#id_fax_area").val(oData["fax_area"]);
                    $("#id_fax_number").val(oData["fax_number"]);
                }
            }
        },
        
        fillInOrgInstContactData: function(oData) {
            var oSelf = self.EventMainDataManager;
            
            // show correct blocks
            oSelf.manageOrgInstBlocks("orgInstSelected");
            
            oSelf.setText($("#id_org_inst_address_title"), oData.title);
            oSelf.setText($("#id_org_inst_address_street_address"), oData.street_address);
            
            if (oData.street_address2) 
                oSelf.setText($("#id_org_inst_address_street_address2"), oData.street_address2);
            else
                $("#id_org_inst_address_street_address2").hide();
    
            oSelf.setText($("#id_org_inst_address_postal_code"), oData.postal_code);
            oSelf.setText($("#id_org_inst_address_city"), oData.city);		
            oSelf.setText($("#id_org_inst_address_country"), oData.country_name);
            
            if (oData.url0_link != "")
                oSelf.setText($("#id_org_inst_url0_link"), oData.url0_link);
            else {
                oSelf.setText($("#id_org_inst_url0_link"), "");
                $("#id_org_inst_url0_link_container").hide();
            }
    
            if (oData["phone_number"]) {
                oSelf.setText(
                    $("#id_org_inst_phone"), 
                    "+ " + oData["phone_country"] + " (" + 
                    oData["phone_area"] + ") " +
                    oData["phone_number"]
                );
            } else {
                oSelf.setText($("#id_org_inst_phone"), "");
                $("#id_org_inst_phone_container").hide();
            }
            
            if (oData["fax_number"]) {
                $("#id_org_inst_fax").show();
                oSelf.setText(
                    $("#id_org_inst_fax"), 
                    "+ " + oData["fax_country"] + " (" +
                    oData["fax_area"] + ") " +
                    oData["fax_number"]
                );
            } else {
                oSelf.setText($("#id_org_inst_fax"), "");
                $("#id_org_inst_fax_container").hide();
            }
        },
        
        setText: function($oElement, sNewText) {
            $oElement.children(":first").html(sNewText);
        },
        
        destruct: function() {
            self.EventMainDataManager = null;
        }
    };
    
    self.EventFeeManager = {
        iFeeCount: 6,
        init: function() {
            var oSelf = self.EventFeeManager;
            for (i=1; i<6; i++) {
                var oF = $("#id_fee" + i + "_amount");
                if (!oF.val()) {
                    $("#id_fee" + i + "_label_en").parent().hide();
                    $("#id_fee" + i + "_label_de").parent().hide();
                    oF.parent().hide();
                    oSelf.iFeeCount--;
                }
            }
            /* javascript-based fee managing */
            var $oLi = $('<li class="dyn_contact_managing">').appendTo($("#id_fee0_label").parents("ul:first"));
            $(
                '<a href="#Remove-Fee" id="fee_remover">' + gettext("Remove Fee") + '</a>'
            ).css(
                "display", oSelf.iFeeCount>1? "inline": "none"
            ).click(oSelf.remove_fee).appendTo($oLi);
            $(document.createTextNode(" ")).appendTo($oLi);
            $(
                '<a href="#Add-Fee" id="fee_adder">' + gettext("Add Fee") + '</a>'
            ).css(
                "display", oSelf.iFeeCount<6? "inline": "none"
            ).click(oSelf.add_fee).appendTo($oLi);
        },
        
        destruct: function() {
            self.EventFeeManager = null;
        },
        
        /* add_fee */
        add_fee: function() {
            var oSelf = self.EventFeeManager;
        
            $("#id_fee" + oSelf.iFeeCount + "_label_en").parent().show();
            $("#id_fee" + oSelf.iFeeCount + "_label_de").parent().show();
            $("#id_fee" + oSelf.iFeeCount + "_amount").parent().show();
            oSelf.iFeeCount++;
            if (oSelf.iFeeCount > 1) {
                $("#fee_remover").css("display", "inline");
                $("#fee_adder").addClass("separated");
            }                                              
            if (oSelf.iFeeCount >= 6) {
                $("#fee_adder").hide();
            }
            return false;
        },
        
        /* remove_fee */
        remove_fee: function() {
            var oSelf = self.EventFeeManager;
            oSelf.iFeeCount--;
            $("#id_fee" + oSelf.iFeeCount + "_label_en").val("").parent().hide().find('p.error').remove();
            $("#id_fee" + oSelf.iFeeCount + "_label_de").val("").parent().hide().find('p.error').remove();
            $("#id_fee" + oSelf.iFeeCount + "_amount").val("").parent().hide().find('p.error').remove();
            if (oSelf.iFeeCount <= 1) {
                $("#fee_remover").hide();
                $("#fee_adder").removeClass("separated");
            } 
            if (oSelf.iFeeCount < 6) {
                $("#fee_adder").css("display", "inline");
            } 
            return false;
        }
    };
    
    $(document).ready(function(){
        self.EventMainDataManager.init();
        self.EventFeeManager.init();
    });
    
    $(window).unload(function() {
        self.EventMainDataManager.destruct();
        self.EventFeeManager.destruct();
    });
    
}(jQuery));
