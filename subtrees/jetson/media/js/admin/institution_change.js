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
        ).autocomplete("/" + window.settings.LANGUAGE_CODE + "/helper/institution_lookup/", {
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
        ).autocomplete("/" + window.settings.LANGUAGE_CODE + "/helper/country_lookup/", {
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
            onAfterRemoved: (function (row) {
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
                updateInlineLabel(row);
                self.AutocompleteManager.reinit(row);
                
                var iIndex = row.attr("id").match(/\d+$/)[0];
                self.URLManager.addEvents(iIndex);
                self.PhoneManager.addEvents(iIndex);
                self.EmailManager.addEvents(iIndex);
                self.IMManager.addEvents(iIndex);
                self.GMapManager.init(iIndex);
            })
        });
    });
})(jQuery);

