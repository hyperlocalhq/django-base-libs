$j = jQuery;

var CONTACT_ID_PREFIX = "id_individualcontact_set-";

var URLManager = {
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            URLManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_url" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "url_types_" + iIndex,
                id:"id_url_types_" + iIndex + "_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("URLManager.toggleSelection("+iIndex+", " + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    toggleSelection: function(iIndex, iPosSel) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_url" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
    }
};

var PhoneManager = {
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            PhoneManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_phone" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "phone_types_" + iIndex,
                id: "id_phone_types_" + iIndex + "_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("PhoneManager.toggleSelection("+iIndex+", " + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_phone" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_phone_types_" + iIndex + "_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iIndex, iPosSel) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_phone" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
    }
};

var EmailManager = {
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            EmailManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_email" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "email_types_" + iIndex,
                id: "id_email_types_" + iIndex + "_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("EmailManager.toggleSelection("+iIndex+", " + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_email" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_email_types_" + iIndex + "_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iIndex, iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_email" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var IMManager = {
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            IMManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_im" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "im_types_" + iIndex,
                id: "id_im_types_" + iIndex + "_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("IMManager.toggleSelection("+iIndex+", " + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function(iIndex) {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_im" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_im_types_" + iIndex + "_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iIndex, iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-is_im" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var ContactPrepopulationManager = {
    aTextFields: [
        "location_title",

        "street_address", "street_address2", "street_address3", "postal_code", "city", "state", "neighborhood", "district",

        "latitude", "longitude", "altitude",

        "email0_address", "email1_address", "email2_address",

        "phone0_country", "phone0_area", "phone0_number",
        "phone1_country", "phone1_area", "phone1_number",
        "phone2_country", "phone2_area", "phone2_number",

        "url0_link", "url1_link", "url2_link",

        "im0_address", "im1_address", "im2_address"
    ],
    aSelectFields: [
        "email0_type",  "email1_type", "email2_type",
        
        "phone0_type", "phone1_type", "phone2_type",
        
        "url0_type", "url1_type", "url2_type",
        
        "im0_type", "im1_type", "im2_type"
    ],
    aBoolFields: [
        "is_shipping_address", "is_billing_address",
        
        "is_phone0_default", "is_phone0_on_hold", "is_phone1_default", "is_phone1_on_hold", "is_phone2_default", "is_phone2_on_hold",
        
        "is_email0_default", "is_email0_on_hold", "is_email1_default", "is_email1_on_hold", "is_email2_default", "is_email2_on_hold",
        
        "is_url0_default", "is_url0_on_hold", "is_url1_default", "is_url1_on_hold", "is_url2_default", "is_url2_on_hold",
        
        "is_im0_default", "is_im0_on_hold", "is_im1_default", "is_im1_on_hold", "is_im2_default", "is_im2_on_hold"
    ],
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            ContactPrepopulationManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-institution").change(
            function() {
                ContactPrepopulationManager.get_contact_details(
                    iIndex,
                    $j(this).val()
                )
            }
        );
    },
    get_contact_details: function(iIndex, sValue) {
        if (sValue) {
            $j.get(
                '/' + settings.lang + '/admin/institutions/institution/' + sValue + '/json/',
                new Function("oData", "ContactPrepopulationManager.prepopulate("+iIndex+", oData)"),
                'json'
            );
        }
    },
    prepopulate: function (iIndex, oData) {
        var aFields = ContactPrepopulationManager.aTextFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-" + aFields[iPos]);
            if (!(oNode.value) && oData[aFields[iPos]] && oData[aFields[iPos]]!="None") {
                oNode.value = oData[aFields[iPos]];
            }
        }
        aFields = ContactPrepopulationManager.aBoolFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-" + aFields[iPos]);
            oNode.checked = oData[aFields[iPos]];
        }
        aFields = ContactPrepopulationManager.aSelectFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-" + aFields[iPos]);
            oNode.value = oData[aFields[iPos] + "_id"];
        }
        if (oData["country_name"] && oData["country"]) {
            $j("#" + CONTACT_ID_PREFIX + iIndex + "-country_text").val(oData["country_name"]);
            $j("#" + CONTACT_ID_PREFIX + iIndex + "-country").val(oData["country"]);
        }
        PhoneManager.checkAppropriateRadio(iIndex);
        GMapManager.adjustGeoposition(iIndex);
    }
};

(function($) {
    $(document).ready(function() {
        URLManager.init();
        PhoneManager.init();
        EmailManager.init();
        IMManager.init();
        ContactPrepopulationManager.init();

        var updateInlineLabel = function(row) {
            $("#individualcontact_set-group div.items div.module").find("h3:first").each(function(i) {
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + (++i)));
            });
        }
        var reinitDateTimeFields = function(row) {
            row.find(".vDateField").datepicker({
                //appendText: '(mm/dd/yyyy)',
                showOn: 'button',
                buttonImageOnly: false,
                buttonText: '',
                dateFormat: grappelli.getFormat('date')
            });
            //$(".vTimeField").timepicker();
        }
        var updateSelectFilter = function(row) {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter != "undefined"){
                row.find(".selectfilter").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], false, "/admin-media/");
                });
                row.find(".selectfilterstacked").each(function(index, value){
                  var namearr = value.name.split('-');
                  SelectFilter.init(value.id, namearr[namearr.length-1], true, "/admin-media/");
                });
            }
        }
        var reinitTinyMCE = function(row) {
            row.find("textarea.vLargeTextField").each(function() {
                tinyMCE.execCommand('mceAddControl', false, this.id);
            });
        };
        var deleteTinyMCE = function(row) {
            row.find("textarea.vLargeTextField").each(function() {
                if (tinyMCE.getInstanceById(this.id)) {
                    tinyMCE.execCommand('mceRemoveControl', false, this.id);
                }
            });
        };
        
        // TODO. re-init ui-calendar
        django.jQuery("#individualcontact_set-group").grp_inline({
            prefix: "individualcontact_set",
            onAfterRemoved: (function (row) {
                row = jQuery(row);
                updateInlineLabel(row);
                deleteTinyMCE(row);
            }),
            onAfterAdded: (function(row) {
                grappelli.reinitDateTimeFields(row);
                grappelli.updateSelectFilter(row);
                row.grp_collapsible();
                row.find("fieldset.grp-collapse").grp_collapsible();
                
                // get the jQuery obj instead of django.jQuery
                row = jQuery(row);
                
                reinitTinyMCE(row);
                reinitDateTimeFields(row);
                updateSelectFilter(row);
                updateInlineLabel(row);
                
                var iIndex = row.attr("id").match(/\d+$/)[0];
                self.URLManager.addEvents(iIndex);
                self.PhoneManager.addEvents(iIndex);
                self.EmailManager.addEvents(iIndex);
                self.IMManager.addEvents(iIndex);
                self.GMapManager.init(iIndex);
                self.ContactPrepopulationManager.addEvents(iIndex);
                
                self.AutocompleteManager.reinit(row);
            })
        });
    });
})(jQuery);
