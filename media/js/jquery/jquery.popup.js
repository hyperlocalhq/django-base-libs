(function($, undefined) {

    self.close_popup = function() {
        if (window._popup_win) {
            window._popup_win.dialog("destroy");
            window._popup_win = null;
        }
        return false;
    }
    
    self.open_popup = function(sTitle, iW, iH, sUrl, bWarning, oData, oEvents) {
        var sInProgress = '<div class="popup_in_progress"><img alt="" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Loading. Please wait.") + '</span></div>';
        var sReloading = '<div class="popup_in_progress"><img alt="" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Reloading the page...") + '</span></div>';
        var sRedirecting = '<div class="popup_in_progress"><img alt="" width="16" height="16" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Redirecting...") + '</span></div>';
        close_popup();
        oEvents = oEvents || {};
        var onLoad = oEvents['onload'];
        function attach_form_events(responseText, textStatus, XMLHttpRequest) {
            if (onLoad) {
                onLoad();
            }
            window._popup_win.find("input[name=cancel]").click(close_popup);
            window._popup_win.find("form").submit(function() {
                var sValues = "";
                var oValues = {};
                $(this).find(":input").each(function() {
                    var $oElem = $(this);
                    var sName = $oElem.attr("name");
                    var sValue = $oElem.val();
                    if (sName) {
                        if (!$oElem.is(":checkbox") || $oElem.attr("checked")) {
                            if (oValues[sName]) {
                                if (typeof(oValues[sName]) == "string") {
                                    oValues[sName] = [oValues[sName]];
                                }
                                oValues[sName].push(sValue);
                            } else {
                                oValues[sName] = sValue;
                            }
                        }
                    }
                });
                var oOnBeforeSubmit = oEvents['onbeforesubmit'];
                var oOnSubmit = oEvents['onsubmit'];
                var oOnAfterSubmit = oEvents['onaftersubmit'];
                if (oOnBeforeSubmit) {
                    oOnBeforeSubmit();
                }
                if (oOnSubmit) {
                    oOnSubmit();
                    if (oOnAfterSubmit) {
                        oOnAfterSubmit();
                    }
                } else {
                    window._popup_win.html(sInProgress);
                    $.post(sUrl, oValues, function(sData, sStatus){
                        if (!sData) {
                            if (oOnAfterSubmit) {
                                oOnAfterSubmit();
                            }
                            close_popup();
                        } else if(sData=="reload") {
                            // "reload" forces the reload of a page
                            window._popup_win.html(sReloading);
                            document.location.href = document.location.pathname;
                        } else if(sData.indexOf("redirect") == 0) {
                            // "redirect=/path/" forces redirection to /path/
                            window._popup_win.html(sRedirecting);
                            document.location.href = sData.replace(/^redirect=/, "");
                        } else {
                            window._popup_win.html(sData);
                            attach_form_events();
                        }
                    });
                }
                return false;
            });
        }
        sTitle = sTitle || "";
        iW = parseInt(iW) || 400;
        var bAutoHeight = (iH == "auto");
        if (iH == "auto" || !iH) {
            iH = 300;
        }
        var iX = (document.documentElement.clientWidth - iW) / 2;
        var iY = (document.documentElement.clientHeight - iH) / 2;
        var oPopup = window._popup_win = $('<div>' + sInProgress + '</div>').dialog({
            title: sTitle,
            width: iW,
            minWidth: iW,
            maxWidth: iW,
            height: iH,
            minHeight: iH,
            maxHeight: iH,
            position: [iX, iY]
        });
        var oContainer = oPopup.parent().parent();
        if (bWarning) {
            oContainer.addClass("ui-warning-dialog");
        }
        if (bAutoHeight) {
            oContainer.css("height", "auto");
        }
        oContainer.css("overflow", "visible");
        sUrl = sUrl || "";
        if (oData) {
            oPopup.load(sUrl, oData, attach_form_events);
        } else {
            oPopup.load(sUrl, attach_form_events);
        }
    }

}(jQuery));
