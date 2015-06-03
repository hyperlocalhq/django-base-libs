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

var GMapManager = {
    markers: {}, // {iIndex: oMarker, ..}
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            GMapManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var oF = new Function("GMapManager.recognizeLocation("+iIndex+")");
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-street_address").blur(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-street_address2").blur(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-city").blur(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-country_hidden").change(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-state").blur(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-postal_code").blur(oF);
        $j('<input type="button" value="' + gettext("Relocate on map") + '" />').appendTo(
            $j("#gmap_" + iIndex).parents('.column')
        ).click(oF);
        
        var oF = new Function("GMapManager.adjustGeoposition("+iIndex+")");
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-latitude").blur(oF).change(oF);
        $j("#" + CONTACT_ID_PREFIX + iIndex + "-longitude").blur(oF).change(oF);
        $j("#gmap_" + iIndex).load(oF);
    },
    recognizeLocation: function(iIndex) {
        var oGMapIframe = $j("#gmap_" + iIndex).get(0);
        if (oGMapIframe) {
            var oGMapWindow = oGMapIframe.contentWindow;
            oGMapWindow.recognizeLocation(
                GMapManager.getAddress4search(iIndex),
                new Function(
                    "oResults",
                    "GMapManager.autocompleteAddress("+iIndex+", oResults)"
                )
            );
        }
    },
    getAddress4search: function(iIndex) {
        var aFullAddress = new Array();
        aFullAddress.push((document.getElementById(CONTACT_ID_PREFIX + iIndex + "-street_address").value||"")
            + " " + (document.getElementById(CONTACT_ID_PREFIX + iIndex + "-street_address2").value||""));
        aFullAddress.push(document.getElementById(CONTACT_ID_PREFIX + iIndex + "-city").value||"");
        aFullAddress.push(document.getElementById(CONTACT_ID_PREFIX + iIndex + "-country").value||"");
        aFullAddress.push(document.getElementById(CONTACT_ID_PREFIX + iIndex + "-state").value||"");
        aFullAddress.push(document.getElementById(CONTACT_ID_PREFIX + iIndex + "-postal_code").value||"");
        return aFullAddress.join(", ");
    },
    getFullAddress: function(iIndex) {
        var aComponents = new Array("country", "state", "city", "street_address", "postal_code");
        var aFullAddress = new Array();
        var sTemp = "";
        for (iPos in  aComponents) {
            sTemp = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-" + aComponents[iPos]).value;
            if (sTemp) {
                aFullAddress.push(sTemp);
            }
        }
        return aFullAddress.join(", ");
    },
    adjustGeoposition: function(iIndex) {
        var oLat = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-latitude");
        var oLng = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-longitude");
        if (oLat.value!="" && oLng.value!="") {
            GMapManager.markGeoposition(iIndex, oLat.value, oLng.value);
        }
    },
    markGeoposition: function(iIndex, iLat, iLong) {
        var oSelf = GMapManager;
        var oGMapIframe = $j("#gmap_" + iIndex).get(0);
        if (oGMapIframe) {
            var oGMapWindow = oGMapIframe.contentWindow;
            var oPoint = new oGMapWindow.google.maps.LatLng(iLat, iLong);
            oGMapWindow.oMap.setCenter(oPoint, 15);
            if (oSelf.markers[iIndex]) {
                oMarker = oSelf.markers[iIndex];
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
                    new Function("iLat", "iLng","oParams","GMapManager.correctGeoposition("+iIndex+", iLat, iLng, oParams)"),
                    {bNoSuggest: true}
                );
                oSelf.markers[iIndex] = oMarker;
            }
            return oMarker;
        }
    },
    correctGeoposition: function(iIndex, iLat, iLng, oParams) {
        var bSuggesting = false;
        iLat = Math.round(iLat * 1000000) / 1000000;
        iLng = Math.round(iLng * 1000000) / 1000000;

        var oLat = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-latitude");
        var oLng = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-longitude");
        
        if (oParams.bNoSuggest) {
            oLat.value = iLat;
            oLng.value = iLng;
        } else {
            // Set or suggest latitude
            if (!oLat.value) {
                oLat.value = iLat;
            } else if (oLat.value != iLat) {
                var oSuggestions = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-latitude_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("div", oLat.parentNode, null, "id", CONTACT_ID_PREFIX + iIndex + "-latitude_suggestions");
                    oSuggestions = oLat.parentNode.insertBefore(oSuggestions, oLat.nextSibling.nextSibling);
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, iLat, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField('+iIndex+', "' + CONTACT_ID_PREFIX + iIndex + '-latitude"); GMapManager.adjustGeoposition('+iIndex+'); window.cancelEvent(event);'));
                bSuggesting = true;
            }
    
            // Set or suggest longitude
            if (!oLng.value) {
                oLng.value = iLng;
            } else if (oLng.value != iLng) {
                var oSuggestions = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-longitude_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("div", oLng.parentNode, null, "id", CONTACT_ID_PREFIX + iIndex + "-longitude_suggestions");
                    oSuggestions = oLng.parentNode.insertBefore(oSuggestions, oLng.nextSibling.nextSibling);
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, iLng, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField('+iIndex+', "' + CONTACT_ID_PREFIX + iIndex + '-longitude"); GMapManager.adjustGeoposition('+iIndex+'); window.cancelEvent(event);'));
                bSuggesting = true;

            }
        }
        return bSuggesting;
    },
    autocompleteAddress: function(iIndex, oResults) {
        oDefaultResult = oResults[0]
        if (!oDefaultResult) {
            return;
        }
        var oPoint = oDefaultResult.geometry.location;
        var bSuggesting = GMapManager.correctGeoposition(
            iIndex,
            oPoint.lat(),
            oPoint.lng(),
            {}
        );
        var aAddressComponents = oDefaultResult.address_components;
        GMapManager.extractFromXAL(iIndex, aAddressComponents);

        if (!bSuggesting) {
            GMapManager.markGeoposition(
                iIndex,
                oPoint.lat(),
                oPoint.lng()
            );
        }
    },
    updateField: function(iIndex, sFieldId) {
        oField = document.getElementById(sFieldId);
        oSuggestion = document.getElementById(sFieldId + "_suggestions").firstChild;
        oField.value = oSuggestion.firstChild.data;
        oSuggestion.parentNode.removeChild(oSuggestion);
    },
    extractFromXAL: function(iIndex, aAddressComponents) {
        var i, iLen=aAddressComponents.length;
        var sStreetName, sStreetNumber;
        for (i=0; i<iLen; i++) {
            oObj = aAddressComponents[i];
            switch (oObj.types[0]) {
                case "locality":
                    document.getElementById(CONTACT_ID_PREFIX + iIndex + "-city").value = oObj.long_name;
                    break;
                case "sublocality":
                    var oDistrict = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-district"); 
                    if (!oDistrict.value) {
                        oDistrict.value = oObj.long_name;
                    } else if (oDistrict.value != oObj.long_name) {
                        var oSuggestions = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-district_suggestions");
                        if (!oSuggestions) {
                            oSuggestions = quickElement("span", oDistrict.parentNode, null, "id", CONTACT_ID_PREFIX + iIndex + "-district_suggestions");
                        }
                        if (oSuggestions.firstChild) {
                            oSuggestions.removeChild(oSuggestions.firstChild);
                        }
                        oA = quickElement("a", oSuggestions, oObj.long_name, "href", "#");
                        addEvent(oA, "click", new Function("event", 'GMapManager.updateField('+iIndex+', "' + CONTACT_ID_PREFIX + iIndex + '-district"); window.cancelEvent(event);'));
                    }
                    break;
                case "street_number":
                    sStreetNumber = oObj.long_name;
                    break;
                case "route":
                    sStreetName = oObj.long_name;
                    break;
                case "postal_code":
                    document.getElementById(CONTACT_ID_PREFIX + iIndex + "-postal_code").value = oObj.long_name;
                    break;
                case "country":
                    document.getElementById(CONTACT_ID_PREFIX + iIndex + "-country").value = oObj.short_name;
                    break;
            }
        }
        if (sStreetName) {
            var sStreetAddress = sStreetName;
            if (sStreetNumber) {
                sStreetAddress += " " + sStreetNumber;
            }
            
            var oStreetAddress = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-street_address"); 
            if (!oStreetAddress.value) {
                oStreetAddress.value = sStreetAddress;
            } else if (oStreetAddress.value != sStreetAddress) {
                var oSuggestions = document.getElementById(CONTACT_ID_PREFIX + iIndex + "-street_address_suggestions");
                if (!oSuggestions) {
                    oSuggestions = quickElement("span", oStreetAddress.parentNode, null, "id", CONTACT_ID_PREFIX + iIndex + "-street_address_suggestions");
                }
                if (oSuggestions.firstChild) {
                    oSuggestions.removeChild(oSuggestions.firstChild);
                }
                oA = quickElement("a", oSuggestions, sStreetAddress, "href", "#");
                addEvent(oA, "click", new Function("event", 'GMapManager.updateField('+iIndex+', "' + CONTACT_ID_PREFIX + iIndex + '-street_address"); window.cancelEvent(event);'));
            }
        }
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
                "/admin/institutions/institution/" + sValue + "/json/",
                new Function("sData", "ContactPrepopulationManager.prepopulate("+iIndex+", sData)")
            );
        }
    },
    prepopulate: function (iIndex, sData) {
        eval("oData =" + sData);
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
        GMapManager.init();
        
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
            //deleteCssClass: "delete-handler",
            //emptyCssClass: "empty-form",
            onAfterRemoved: (function (row) {
                row = jQuery(row);
                updateInlineLabel(row);
                deleteTinyMCE(row);
            }),
            onAfterAdded: (function(row) {
                grappelli.reinitDateTimeFields(row);
                grappelli.updateSelectFilter(row);
                row.grp_collapsible();
                row.find("fieldset.collapse").grp_collapsible();
                
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
                self.GMapManager.addEvents(iIndex);
                self.ContactPrepopulationManager.addEvents(iIndex);
                
                self.AutocompleteManager.reinit(row);
            })
        });
    });
})(jQuery);
