$j = jQuery;

var CONTACT_ID_PREFIX = "id_institutionalcontact_set-";

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

var InstitutionLookupManager = {
    init: function() {
        InstitutionLookupManager.addEvents();
    },
    addEvents: function() {
        var oOld = $j("#id_parent");
        oOld.find("option").each(function() {
            $j(this).html($j.trim($j(this).html()));
        });
        var sHiddenId = oOld.attr("id") + "_hidden";
        var sVal = oOld.val();
        $j('<input type="text" />').attr({
            id: oOld.attr("id"),
            maxlength: 255,
            size: 30
        }).replaceAll(oOld).after(
            $j('<input type="hidden" />').attr({
                id: sHiddenId,
                name: oOld.attr("name")
            }).val(sVal).change(oOld[0].onchange)
        ).autocomplete("/helper/institution_lookup/", {
            onItemSelect: new Function(
                "oEl",
                "InstitutionLookupManager.onItemSelect('"+sHiddenId+"', oEl)"
            )
        }).addClass("vTextField").val(
            sVal?
                oOld[0].options[oOld[0].selectedIndex].innerHTML:
                ""
        ).change(function() {
            if (!$j(this).val()) {
                $j("#" + sHiddenId).val("").change();
            }
        });
    },
    onItemSelect: function(sHiddenId, oEl) {
        if(oEl == null) {
            return;
        }
        if(!!oEl.extra) {
            $j("#" + sHiddenId).val(oEl.extra[0]).change();
        }
    }
};

var CountryLookupManager = {
    init: function() {
        var iContactQuantity = parseInt($j("#" + CONTACT_ID_PREFIX + "TOTAL_FORMS").val());
        for (iIndex=0; iIndex<iContactQuantity; iIndex++) {
            CountryLookupManager.addEvents(iIndex);
        }
    },
    addEvents: function(iIndex) {
        var oOld = $j("#" + CONTACT_ID_PREFIX + iIndex + "-country");
        oOld.find("option").each(function() {
            $j(this).html($j.trim($j(this).html()));
        });
        var sHiddenId = oOld.attr("id") + "_hidden";
        var sVal = oOld.val();
        $j('<input type="text" />').attr({
            id: oOld.attr("id"),
            maxlength: 255,
            size: 30
        }).replaceAll(oOld).after(
            $j('<input type="hidden" />').attr({
                id: sHiddenId,
                name: oOld.attr("name")
            }).val(sVal)
        ).autocomplete("/helper/country_lookup/", {
            onItemSelect: new Function(
                "oEl",
                "CountryLookupManager.onItemSelect('"+sHiddenId+"', oEl)"
            )
        }).addClass("vTextField").val(
            sVal?
                oOld[0].options[oOld[0].selectedIndex].innerHTML:
                ""
        ).change(function() {
            if (!$j(this).val()) {
                $j("#" + sHiddenId).val("").change();
            }
        });
    },
    onItemSelect: function(sHiddenId, oEl) {
        if(oEl == null) {
            return;
        }
        if(!!oEl.extra) {
            $j("#" + sHiddenId).val(oEl.extra[0]).change();
        }
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
                        var oA = quickElement("a", oSuggestions, oObj.long_name, "href", "#");
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

var OpeningHoursManager = {
    aDays: new Array("mon", "tue", "wed", "thu", "fri", "sat", "sun"),
    init: function() {
        var bExpanded = false;
        var aDays = OpeningHoursManager.aDays;
        var bModifyDefaults = false;
        for (var iPos in aDays) {
            if (document.getElementById("id_" + aDays[iPos] + "_open").value) {
                bModifyDefaults = true;
                break;
            }
        }
        if (bModifyDefaults) {
            for (var iPos in aDays) {
                if (!document.getElementById("id_" + aDays[iPos] + "_open").value) {
                    document.getElementById("id_closed_on_" + aDays[iPos]).checked = true;
                    OpeningHoursManager.modifyDay(aDays[iPos]);
                } else if (document.getElementById("id_" + aDays[iPos] + "_break_close").value && !bExpanded) {
                    document.getElementById("id_show_break_times").checked = true;
                    bExpanded = true;
                    OpeningHoursManager.modifyBreakTimes();
                }
            }
        }
    },
    applyTimesToAllDays: function () {
        var oDayToCopy = null;
        var aDays = OpeningHoursManager.aDays;
        for (var iPos in aDays) {
            var oCheckbox = document.getElementById("id_closed_on_" + aDays[iPos]);
            if (!oCheckbox.checked) {
                if (!oDayToCopy) {
                    oDayToCopy = {
                        "open": document.getElementById("id_" + aDays[iPos] + "_open").value,
                        "break_close":  document.getElementById("id_" + aDays[iPos] + "_break_close").value,
                        "break_open":  document.getElementById("id_" + aDays[iPos] + "_break_open").value,
                        "close":  document.getElementById("id_" + aDays[iPos] + "_close").value
                    };
                } else {
                    document.getElementById("id_" + aDays[iPos] + "_open").value = oDayToCopy.open;
                    document.getElementById("id_" + aDays[iPos] + "_break_close").value = oDayToCopy.break_close;
                    document.getElementById("id_" + aDays[iPos] + "_break_open").value = oDayToCopy.break_open;
                    document.getElementById("id_" + aDays[iPos] + "_close").value = oDayToCopy.close;
                }
            }
        }
    },
    modifyDay: function (sDay) {
        var oCheckbox = document.getElementById("id_closed_on_" + sDay);
        document.getElementById("id_" + sDay + "_open").disabled =
            document.getElementById("id_" + sDay + "_break_close").disabled =
                document.getElementById("id_" + sDay + "_break_open").disabled =
                    document.getElementById("id_" + sDay + "_close").disabled =
                        oCheckbox.checked;
        if (oCheckbox.checked) {
            document.getElementById("id_" + sDay + "_open").value =
                document.getElementById("id_" + sDay + "_break_close").value =
                    document.getElementById("id_" + sDay + "_break_open").value =
                        document.getElementById("id_" + sDay + "_close").value =
                            "";
        }
    },
    modifyBreakTimes: function () {
        var oCheckbox = document.getElementById("id_show_break_times");
        document.getElementById("break_start_row").style.display =
            document.getElementById("break_end_row").style.display =
                (oCheckbox.checked? "table-row": "none");
    }
};

(function($) {
    $(document).ready(function() {
        URLManager.init();
        PhoneManager.init();
        EmailManager.init();
        IMManager.init();
        OpeningHoursManager.init();
        GMapManager.init();
            
        var updateInlineLabel = function(row) {
            $("#institutionalcontact_set-group div.items div.module").find("h3:first").each(function(i) {
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
            $(".vTimeField").timepicker();
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
        django.jQuery("#institutionalcontact_set-group").grp_inline({
            prefix: "institutionalcontact_set",
            deleteCssClass: "delete-handler",
            emptyCssClass: "empty-form",
            onAfterRemoved: (function (row) {
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
                updateInlineLabel(row);
                self.AutocompleteManager.reinit(row);
                
                var iIndex = row.attr("id").match(/\d+$/)[0];
                self.URLManager.addEvents(iIndex);
                self.PhoneManager.addEvents(iIndex);
                self.EmailManager.addEvents(iIndex);
                self.IMManager.addEvents(iIndex);
                self.GMapManager.addEvents(iIndex);
            })
        });
    });
})(jQuery);

