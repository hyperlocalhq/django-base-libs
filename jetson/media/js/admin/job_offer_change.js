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

var GMapManager = {
    marker: null,
    init: function() {
        GMapManager.addEvents();
    },
    addEvents: function() {
        $j("#id_street_address").blur(
            new Function("GMapManager.recognizeLocation()")
        );
        $j("#id_street_address2").blur(
            new Function("GMapManager.recognizeLocation()")
        );
        $j("#id_city").blur(
            new Function("GMapManager.recognizeLocation()")
        );
        $j("#id_country_hidden").change(
            new Function("GMapManager.recognizeLocation()")
        );
        $j("#id_state").blur(
            new Function("GMapManager.recognizeLocation()")
        );
        $j("#id_postal_code").blur(
            new Function("GMapManager.recognizeLocation()")
        );
        $j('<input type="button" value="' + gettext("Relocate on map") + '" />').appendTo(
            $j("#gmap").parents('.row')
        ).click(new Function("self.GMapManager.recognizeLocation()"));

        
        
        
        $j("#id_latitude").blur(
            new Function("GMapManager.adjustGeoposition()")
        );
        $j("#id_longitude").blur(
            new Function("GMapManager.adjustGeoposition()")
        );
        $j("#id_latitude").change(
            new Function("GMapManager.adjustGeoposition()")
        );
        $j("#id_longitude").change(
            new Function("GMapManager.adjustGeoposition()")
        );
        $j("#gmap").load(
            new Function("GMapManager.adjustGeoposition()")
        );
    },
    recognizeLocation: function() {
        var oGMapIframe = $j("#gmap").get(0);
        if (oGMapIframe) {
            var oGMapWindow = oGMapIframe.contentWindow;
            oGMapWindow.recognizeLocation(
                GMapManager.getAddress4search(),
                GMapManager.autocompleteAddress
            );
        }
    },
    getAddress4search: function() {
        var aFullAddress = new Array();
        aFullAddress.push((document.getElementById("id_street_address").value||"")
            + " " + (document.getElementById("id_street_address2").value||""));
        aFullAddress.push(document.getElementById("id_city").value||"");
        aFullAddress.push(document.getElementById("id_country").value||"");
        aFullAddress.push(document.getElementById("id_state").value||"");
        aFullAddress.push(document.getElementById("id_postal_code").value||"");
        return aFullAddress.join(", ");
    },
    getFullAddress: function() {
        var aComponents = new Array("country", "state", "city", "street_address", "postal_code");
        var aFullAddress = new Array();
        var sTemp = "";
        for (iPos in  aComponents) {
            sTemp = document.getElementById("id_" + aComponents[iPos]).value;
            if (sTemp) {
                aFullAddress.push(sTemp);
            }
        }
        return aFullAddress.join(", ");
    },
    adjustGeoposition: function() {
        var oGMapIframe = $j("#gmap").get(0);
        if (oGMapIframe) {
            var oGMapWindow = oGMapIframe.contentWindow;
            var oLat = document.getElementById("id_latitude");
            var oLng = document.getElementById("id_longitude");
            GMapManager.markGeoposition(oLat.value, oLng.value);
        }
    },
    markGeoposition: function(iLat, iLong) {
        var oSelf = GMapManager;
        var oGMapIframe = $j("#gmap").get(0);
        if (oGMapIframe) {
            var oGMapWindow = oGMapIframe.contentWindow;
            if (parseFloat(iLat)==NaN || parseFloat(iLat)==NaN) {
                if (oSelf.marker) {
                    oSelf.marker.setMap(null);
                    oSelf.marker = null;
                    return;
                }
            }
            var oPoint = new oGMapWindow.google.maps.LatLng(iLat, iLong);
            oGMapWindow.oMap.setCenter(oPoint, 15);
            if (oSelf.marker) {
                oMarker = oSelf.marker;
                oMarker.setPosition(oPoint);
            } else {
                var oImage = new oGMapWindow.google.maps.MarkerImage(
                    oGMapWindow.sGMapImagePath + "marker.png",
                    // marker size
                    new oGMapWindow.google.maps.Size(20, 34),
                    // origin
                    new oGMapWindow.google.maps.Point(0, 0),
                    // anchor
                    new oGMapWindow.google.maps.Point(9, 34)
                );
                var oShadow = new oGMapWindow.google.maps.MarkerImage(
                    "http://www.google.com/mapfiles/shadow50.png",
                    // The shadow image is larger in the horizontal dimension
                    // while the position and offset are the same as for the main image.
                    new oGMapWindow.google.maps.Size(37, 34),
                    new oGMapWindow.google.maps.Point(0, 0),
                    new oGMapWindow.google.maps.Point(8, 34)
                );
                
                var oMarker = new oGMapWindow.google.maps.Marker({
                    position: oPoint,
                    map: oGMapWindow.oMap,
                    shadow: oShadow,
                    icon: oImage
                });
                oGMapWindow.setMarkerDraggable(
                    oMarker,
                    new Function("iLat", "iLng","oParams","GMapManager.correctGeoposition(iLat, iLng, oParams)"),
                    {bNoSuggest: true}
                );
                oSelf.marker = oMarker;
            }
            return oMarker;
        }
    },
    correctGeoposition: function(iLat, iLng, oParams) {
        var bSuggesting = false;
        iLat = Math.round(iLat * 1000000) / 1000000;
        iLng = Math.round(iLng * 1000000) / 1000000;

        var oLat = document.getElementById("id_latitude");
        var oLng = document.getElementById("id_longitude");
        
        if (oParams.bNoSuggest) {
            oLat.value = iLat;
            oLng.value = iLng;
        } else {
            // Set or suggest latitude
            if (!oLat.value) {
                oLat.value = iLat;
            } else if (oLat.value != iLat) {
                var oSuggestions = document.getElementById("id_latitude_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("span", oLat.parentNode, null, "id", "id_latitude_suggestions");
                    oSuggestions = oLat.parentNode.insertBefore(oSuggestions, oLat.nextSibling.nextSibling);
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, iLat, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField("id_latitude"); GMapManager.adjustGeoposition(); window.cancelEvent(event);'));
                bSuggesting = true;
            }
    
            // Set or suggest longitude
            if (!oLng.value) {
                oLng.value = iLng;
            } else if (oLng.value != iLng) {
                var oSuggestions = document.getElementById("id_longitude_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("span", oLng.parentNode, null, "id", "id_longitude_suggestions");
                    oSuggestions = oLng.parentNode.insertBefore(oSuggestions, oLng.nextSibling.nextSibling);
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, iLng, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField("id_longitude"); GMapManager.adjustGeoposition(); window.cancelEvent(event);'));
                bSuggesting = true;

            }
        }
        return bSuggesting;
    },
    autocompleteAddress: function(oResults) {
        oDefaultResult = oResults[0]
        if (!oDefaultResult) {
            return;
        }
        var oPoint = oDefaultResult.geometry.location;
        var bSuggesting = GMapManager.correctGeoposition(
            oPoint.lat(),
            oPoint.lng(),
            {}
        );
        var aAddressComponents = oDefaultResult.address_components;
        GMapManager.extractFromXAL(aAddressComponents);

        if (!bSuggesting) {
            GMapManager.markGeoposition(
                oPoint.lat(),
                oPoint.lng()
            );
        }
    },
    updateField: function(sFieldId) {
        oField = document.getElementById(sFieldId);
        oSuggestion = document.getElementById(sFieldId + "_suggestions").firstChild;
        oField.value = oSuggestion.firstChild.data;
        oSuggestion.parentNode.removeChild(oSuggestion);
    },
    extractFromXAL: function(aAddressComponents) {
        var i, iLen=aAddressComponents.length;
        var sStreetName, sStreetNumber;
        for (i=0; i<iLen; i++) {
            oObj = aAddressComponents[i];
            switch (oObj.types[0]) {
                case "locality":
                    document.getElementById("id_city").value = oObj.long_name;
                    break;
                case "sublocality":
                    var oDistrict = document.getElementById("id_district"); 
                    if (!oDistrict.value) {
                        oDistrict.value = oObj.long_name;
                    } else if (oDistrict.value != oObj.long_name) {
                        var oSuggestions = document.getElementById("id_district_suggestions");
                        if (!oSuggestions) {
                            oSuggestions = quickElement("span", oDistrict.parentNode, null, "id", "id_district_suggestions");
                        }
                        if (oSuggestions.firstChild) {
                            oSuggestions.removeChild(oSuggestions.firstChild);
                        }
                        oA = quickElement("a", oSuggestions, oObj.long_name, "href", "#");
                        addEvent(oA, "click", new Function("event", 'GMapManager.updateField("id_district"); window.cancelEvent(event);'));
                    }
                    break;
                case "street_number":
                    sStreetNumber = oObj.long_name;
                    break;
                case "route":
                    sStreetName = oObj.long_name;
                    break;
                case "postal_code":
                    document.getElementById("id_postal_code").value = oObj.long_name;
                    break;
                case "country":
                    document.getElementById("id_country").value = oObj.short_name;
                    break;
            }
        }
        if (sStreetName) {
            var sStreetAddress = sStreetName;
            if (sStreetNumber) {
                sStreetAddress += " " + sStreetNumber;
            }
            
            var oStreetAddress = document.getElementById("id_street_address"); 
            if (!oStreetAddress.value) {
                oStreetAddress.value = sStreetAddress;
            } else if (oStreetAddress.value != sStreetAddress) {
                var oSuggestions = document.getElementById("id_street_address_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("span", oStreetAddress.parentNode, null, "id", "id_street_address_suggestions");
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, sStreetAddress, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField("id_street_address"); window.cancelEvent(event);'));
            }
        }
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
                "/admin/institutions/institution/" + sValue + "/json/",
                ContactPrepopulationManager.prepopulate
            );
        }
    },
    prepopulate: function (sData) {
        eval("oData =" + sData);
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
        GMapManager.adjustGeoposition();
    }
};

$j(document).ready(function() {
    URLManager.init();
    PhoneManager.init();
    EmailManager.init();
    IMManager.init();
    ContactPrepopulationManager.init();
    GMapManager.init();
});
