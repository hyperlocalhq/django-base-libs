(function($, undefined) {
    
    self.URLManager = {
        init: function() {
            URLManager.addEvents();
        },
        addEvents: function() {
            var iLen=3;
            for (var iPos=0; iPos<iLen; iPos++) {
                var oCheckbox = document.getElementById("id_is_url" + iPos + "_default");
                var oRadio = $('<input type="radio" />').attr({
                    name: "url_types",
                    id:"id_url_types_" + iPos,
                    checked: oCheckbox.checked
                }).appendTo($(oCheckbox.parentNode));
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
    
    self.PhoneManager = {
        init: function() {
            PhoneManager.addEvents();
        },
        addEvents: function() {
            var iLen=3;
            for (var iPos=0; iPos<iLen; iPos++) {
                var oCheckbox = document.getElementById("id_is_phone" + iPos + "_default");
                var oRadio = $('<input type="radio" />').attr({
                    name: "phone_types",
                    id: "id_phone_types_" + iPos,
                    checked: oCheckbox.checked
                }).appendTo($(oCheckbox.parentNode));
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
    
    self.EmailManager = {
        init: function() {
            EmailManager.addEvents();
        },
        addEvents: function() {
            var iLen=3;
            for (var iPos=0; iPos<iLen; iPos++) {
                var oCheckbox = document.getElementById("id_is_email" + iPos + "_default");
                var oRadio = $('<input type="radio" />').attr({
                    name: "email_types",
                    id: "id_email_types_" + iPos,
                    checked: oCheckbox.checked
                }).appendTo($(oCheckbox.parentNode));
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
    
    self.IMManager = {
        init: function() {
            IMManager.addEvents();
        },
        addEvents: function() {
            var iLen=3;
            for (var iPos=0; iPos<iLen; iPos++) {
                var oCheckbox = document.getElementById("id_is_im" + iPos + "_default");
                var oRadio = $('<input type="radio" />').attr({
                    name: "im_types",
                    id: "id_im_types_" + iPos,
                    checked: oCheckbox.checked
                }).appendTo($(oCheckbox.parentNode));
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
    
    self.OpeningHoursManager = {
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
        applyTimesToAllDays: function() {
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
        modifyDay: function(sDay) {
            var oCheckbox = document.getElementById("id_closed_on_" + sDay);
            document.getElementById("id_" + sDay + "_open").disabled =
                oCheckbox.checked;
            document.getElementById("id_" + sDay + "_break_close").disabled =
                oCheckbox.checked;
            document.getElementById("id_" + sDay + "_break_open").disabled =
                oCheckbox.checked;
            document.getElementById("id_" + sDay + "_close").disabled =
                oCheckbox.checked;
            if (oCheckbox.checked) {
                document.getElementById("id_" + sDay + "_open").value = "";
                document.getElementById("id_" + sDay + "_break_close").value = "";
                document.getElementById("id_" + sDay + "_break_open").value = "";
                document.getElementById("id_" + sDay + "_close").value = "";
            }
        },
        modifyBreakTimes: function() {
            var oCheckbox = document.getElementById("id_show_break_times");
            document.getElementById("break_start_row").style.display =
                (oCheckbox.checked? "table-row": "none");
            document.getElementById("break_end_row").style.display =
                (oCheckbox.checked? "table-row": "none");
        }
    }
    
    self.ContactPrepopulationManager = {
        aTextFields: [
            "venue_title",
    
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
            /*
            $("#id_venue_hidden").change(
                function() {
                    ContactPrepopulationManager.get_contact_details(
                        $(this).val()
                    );
                }
            );
            */
            $("#id_venue").change( 
                function() { 
                    ContactPrepopulationManager.get_contact_details( 
                        $(this).val() 
                    ); 
                } 
            );         
        },
        get_contact_details: function(sValue) {
            if (sValue) {
                $.get(
                    '/' + settings.lang + '/admin/institutions/institution/' + sValue + '/json/',
                    ContactPrepopulationManager.prepopulate,
                    "json"
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
                $("#id_country_text").val(oData["country_name"]);
                $("#id_country").val(oData["country"].iso2_code);
            }
            self.URLManager.checkAppropriateRadio();
            self.PhoneManager.checkAppropriateRadio();
            self.EmailManager.checkAppropriateRadio();
            self.IMManager.checkAppropriateRadio();
            self.GMapManager.adjustGeoposition();
        }
    };
    
    self.TimeRangeManager = {
        // TODO: recreate management for multiple event times 
        calendars: [],
        calendarInputs: [],
        clockInputs: [],
        calendarDivName1: 'calendarbox_mod', // name of calendar <div> that gets toggled
        calendarDivName2: 'calendarin_mod',  // name of <div> that contains calendar
        calendarLinkName: 'calendarlink_mod',// name of the link that is used to toggle
        clockDivName: 'clockbox_mod',        // name of clock <div> that gets toggled
        clockLinkName: 'clocklink_mod',      // name of the link that is used to toggle
        init: function() {
            var oSelf = self.TimeRangeManager;
            $("#eventtime_set-group").find("div.is_all_day :checkbox").each(function(iIndex, oEl) {
                var $oEl = $(oEl);
                if ($oEl.attr("checked")) {
                    $oEl.closest("fieldset").find(".start_time,.end_time").hide();
                } else {
                    $oEl.closest("fieldset").find(".start_time,.end_time").show();
                }
                oSelf.addCalendar([
                    $("#id_eventtime_set-" + iIndex + "-start_yyyy").get(0),
                    $("#id_eventtime_set-" + iIndex + "-start_mm").get(0),
                    $("#id_eventtime_set-" + iIndex + "-start_dd").get(0)
                ]);
                oSelf.addClock([
                    $("#id_eventtime_set-" + iIndex + "-start_hh").get(0),
                    $("#id_eventtime_set-" + iIndex + "-start_ii").get(0)
                ]);
                oSelf.addCalendar([
                    $("#id_eventtime_set-" + iIndex + "-end_yyyy").get(0),
                    $("#id_eventtime_set-" + iIndex + "-end_mm").get(0),
                    $("#id_eventtime_set-" + iIndex + "-end_dd").get(0)
                ]);
                oSelf.addClock([
                    $("#id_eventtime_set-" + iIndex + "-end_hh").get(0),
                    $("#id_eventtime_set-" + iIndex + "-end_ii").get(0)
                ]);
            }).click(oSelf.toggleAllDay);
        },
        reinit: function(row) {
            var oSelf = self.TimeRangeManager;
            oSelf.addCalendar([
                row.find("select[id$=start_yyyy]").get(0),
                row.find("select[id$=start_mm]").get(0),
                row.find("select[id$=start_dd]").get(0)
            ]);
            oSelf.addClock([
                row.find("select[id$=start_hh]").get(0),
                row.find("select[id$=start_ii]").get(0)
            ]);
            oSelf.addCalendar([
                row.find("select[id$=end_yyyy]").get(0),
                row.find("select[id$=end_mm]").get(0),
                row.find("select[id$=end_dd]").get(0)
            ]);
            oSelf.addClock([
                row.find("select[id$=end_hh]").get(0),
                row.find("select[id$=end_ii]").get(0)
            ]);
        },
        toggleAllDay: function() {
            var oSelf = self.TimeRangeManager;
            var $oEl = $(this);
            if ($oEl.attr("checked")) {
                $oEl.closest("fieldset").find(".start_time,.end_time").hide();
            } else {
                $oEl.closest("fieldset").find(".start_time,.end_time").show();
            }
        },
        // Add clock widget to a given field
        addClock: function(inps) {
            (function($) {
                if ($(inps[0]).hasClass("hasTimepicker")) {
                    return
                }
                var $oTimefield = $('<input type="text" />').appendTo(
                    $(inps[1]).parent()
                ).css({'width': '25px', 'visibility': 'hidden'});
                var hh = $(inps[0]).val();
                var ii = $(inps[1]).val();
                if (hh && ii) {
                    $oTimefield.val(hh + ":" + ("0" + ii).replace(/0(\d\d)/, "$1"));
                }
                $oTimefield.change(function() {
                    var sTime = $(this).val();
                    if (sTime) {
                        var aTime = sTime.split(":");
                        $(inps[0]).val(parseInt(aTime[0], 10));
                        $(inps[1]).val(parseInt(aTime[1], 10));
                    } else {
                        $(inps[0]).val("");
                        $(inps[1]).val("");
                    }
                }).grp_timepicker();
                $(inps[0]).add($(inps[1])).change(function() {
                    var hh = $(inps[0]).val();
                    var ii = $(inps[1]).val();
                    if (hh && ii) {
                        $oTimefield.val(hh + ":" + ("0" + ii).replace(/0(\d\d)/, "$1"));
                    } else {
                        $oTimefield.val("");
                    }
                }).addClass("hasTimepicker");
            }(django.jQuery));
        },
        // Add calendar widget to a given field.
        addCalendar: function(inps) {
            (function($) {
                if ($(inps[0]).hasClass("hasDatepicker")) {
                    return
                }
                var $oDatefield = $('<input type="text" />').appendTo(
                    $(inps[0]).parent()
                ).css({'width': '30px', 'visibility': 'hidden'});
                var yyyy = $(inps[0]).val();
                var mm = $(inps[1]).val();
                var dd = $(inps[2]).val();
                if (yyyy && mm && dd) {
                    $oDatefield.val(yyyy + "-" + mm + "-" + dd);
                }
                $oDatefield.datepicker({
                    showOn: 'button',
                    buttonImageOnly: false,
                    buttonText: '',
                    dateFormat: "yy-mm-dd"
                }).change(function() {
                    var sDate = $(this).val();
                    if (sDate) {
                        var aDate = sDate.split("-");
                        $(inps[0]).val(parseInt(aDate[0], 10));
                        $(inps[1]).val(parseInt(aDate[1], 10));
                        $(inps[2]).val(parseInt(aDate[2], 10));
                    } else {
                        $(inps[0]).val("");
                        $(inps[1]).val("");
                        $(inps[2]).val("");
                    }
                });
                $(inps[0]).add($(inps[1])).add($(inps[2])).change(function() {
                    var yyyy = $(inps[0]).val();
                    var mm = $(inps[1]).val();
                    var dd = $(inps[2]).val();
                    if (yyyy && mm && dd) {
                        $oDatefield.val(yyyy + "-" + mm + "-" + dd);
                    } else {
                        $oDatefield.val("");
                    }
                }).addClass("hasDatepicker");
            }(django.jQuery));
        },
    };
    
    /*
    self.AutocompleteManager = {
        init: function() {
            var oSelf = self.AutocompleteManager;
            $("input.autocomplete").click(function(){
                $(this).select();
            }).blur(function(){
                var oField = $(this);
                var oSelect = $("#" + oField.attr("id").replace(/_text$/, ""));
                if (!oField.val()) {
                    oSelect.val("");
                }
            });
        },
        result: function(oEvent, aData, sFormatted) {
            var oField = $(this);
            var oSelect = $("#" + oField.attr("id").replace(/_text$/, ""));
            if (aData)
                oSelect.val(aData[1]);
            else 
                oSelect.val("");
            oSelect.change();
            oSelect.blur();
        },
        
        formatItem: function(aRow) {
            var sHtml = '<span class="ac_title">' + aRow[0] + '</span>';
            if (aRow[2]) {
                sHtml += '<br /><span class="ac_description">' + aRow[2] + '</span>';
            }
            return sHtml;
        },
        
        destruct: function() {
            self.AutocompleteManager = null;
        }
    }
    
    $(document).ready(function() {
        self.AutocompleteManager.init();
    });
    
    $(window).unload(function() {
        self.AutocompleteManager.destruct();
    });
    */
    
    $(document).ready(function() {
        self.URLManager.init();
        self.PhoneManager.init();
        self.EmailManager.init();
        self.IMManager.init();
        self.ContactPrepopulationManager.init();
        self.OpeningHoursManager.init();
        self.TimeRangeManager.init();
    });
}(jQuery));
