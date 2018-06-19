$j = jQuery;

var URLManager = {
    init: function() {
        URLManager.addEvents();
    },
    addEvents: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_url" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "url_types",
                id:"id_url_types_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("URLManager.toggleSelection(" + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_url" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_url_types_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_url" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var PhoneManager = {
    init: function() {
        PhoneManager.addEvents();
    },
    addEvents: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_phone" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "phone_types",
                id: "id_phone_types_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("PhoneManager.toggleSelection(" + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_phone" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_phone_types_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_phone" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var EmailManager = {
    init: function() {
        EmailManager.addEvents();
    },
    addEvents: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_email" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "email_types",
                id: "id_email_types_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("EmailManager.toggleSelection(" + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_email" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_email_types_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_email" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var IMManager = {
    init: function() {
        IMManager.addEvents();
    },
    addEvents: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_im" + iPos + "_default");
            var oRadio = $j('<input type="radio" />').attr({
                name: "im_types",
                id: "id_im_types_" + iPos,
                checked: oCheckbox.checked
            }).appendTo($j(oCheckbox.parentNode));
            oRadio.click(new Function("IMManager.toggleSelection(" + iPos + ")"));
            oCheckbox.style.display = "none";
        }
    },
    checkAppropriateRadio: function() {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_im" + iPos + "_default");
            if (oCheckbox.checked) {
                var oRadio = document.getElementById("id_im_types_" + iPos);
                oRadio.checked = true;
                break;
            }
        }
    },
    toggleSelection: function(iPosSel) {
        try {
        var iLen=3;
        for (var iPos=0; iPos<iLen; iPos++) {
            var oCheckbox = document.getElementById("id_is_im" + iPos + "_default");
            oCheckbox.checked = Boolean(iPos == iPosSel);
        }
        } catch (exc) {}
    }
};

var ContactPrepopulationManager = {
    aTextFields: [
        "street_address",
        "street_address2",
        "street_address3",
        "postal_code",
        "city",
        "state",
        "neighborhood",
        "district",

        "latitude",
        "longitude",
        "altitude",

        "email0_address",
        "email1_address",
        "email2_address",

        "phone0_country",
        "phone0_area",
        "phone0_number",
        "phone1_country",
        "phone1_area",
        "phone1_number",
        "phone2_country",
        "phone2_area",
        "phone2_number",

        "url0_link",
        "url1_link",
        "url2_link",

        "im0_address",
        "im1_address",
        "im2_address"
    ],
    aSelectFields: [
        "email0_type",
        "email1_type",
        "email2_type",
        
        "phone0_type",
        "phone1_type",
        "phone2_type",
        
        "url0_type",
        "url1_type",
        "url2_type",
        
        "im0_type",
        "im1_type",
        "im2_type"
    ],
    aBoolFields: [
        "is_phone0_default",
        "is_phone0_on_hold",
        "is_phone1_default",
        "is_phone1_on_hold",
        "is_phone2_default",
        "is_phone2_on_hold",
        
        "is_email0_default",
        "is_email0_on_hold",
        "is_email1_default",
        "is_email1_on_hold",
        "is_email2_default",
        "is_email2_on_hold",
        
        "is_url0_default",
        "is_url0_on_hold",
        "is_url1_default",
        "is_url1_on_hold",
        "is_url2_default",
        "is_url2_on_hold",
        
        "is_im0_default",
        "is_im0_on_hold",
        "is_im1_default",
        "is_im1_on_hold",
        "is_im2_default",
        "is_im2_on_hold"
    ],
    init: function() {
        ContactPrepopulationManager.addEvents();
    },
    addEvents: function() {
        $j("#id_offering_institution").change( 
            function() {
                ContactPrepopulationManager.get_contact_details(
                    $j(this).val() 
                ); 
            } 
        );         
    },
    get_contact_details: function(sValue) {
        if (sValue) {
            $j.get(
                '/' + settings.lang + '/admin/institutions/institution/' + sValue + '/json/',
                ContactPrepopulationManager.prepopulate,
                'json'
            );
        }
    },
    prepopulate: function (oData) {
        var aFields = ContactPrepopulationManager.aTextFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById("id_" + aFields[iPos]);
            if (!(oNode.value) && oData[aFields[iPos]] && oData[aFields[iPos]]!="None") {
                oNode.value = oData[aFields[iPos]];
            }
        }
        aFields = ContactPrepopulationManager.aBoolFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById("id_" + aFields[iPos]);
            oNode.checked = oData[aFields[iPos]];
        }
        aFields = ContactPrepopulationManager.aSelectFields;
        for (iPos=0, iLen=aFields.length; iPos < iLen; iPos++) {
            oNode = document.getElementById("id_" + aFields[iPos]);
            oNode.value = oData[aFields[iPos] + "_id"];
        }
        if (oData["country_name"] && oData["country"]) {
            $j("#id_country").val(oData["country_name"]);
            $j("#id_country_hidden").val(oData["country"]);
        }
        URLManager.checkAppropriateRadio();
        PhoneManager.checkAppropriateRadio();
        EmailManager.checkAppropriateRadio();
        IMManager.checkAppropriateRadio();
        self.GMapManager.adjustGeoposition(0);
    }
};


$j(document).ready(function() {
    URLManager.init();
    PhoneManager.init();
    EmailManager.init();
    IMManager.init();
    ContactPrepopulationManager.init();
});
