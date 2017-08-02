(function($, undefined) {

    self.close_popup = function() {
        if (window._popup_win) {
            var $oPopup = window._popup_win;
            $oPopup.dialog("destroy");
            $oPopup.parent().remove();
            window._popup_win = null;
        }
        return false;
    }
    
    self.open_popup = function(sTitle, iW, iH, sUrl, bWarning, oData, oEvents) {
        var sInProgress = '<div class="popup_in_progress"><img alt="" width="16" height="16" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Loading. Please wait.") + '</span></div>';
        var sReloading = '<div class="popup_in_progress"><img alt="" width="16" height="16" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Reloading the page...") + '</span></div>';
        var sRedirecting = '<div class="popup_in_progress"><img alt="" width="16" height="16" src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" /><span>' + gettext("Redirecting...") + '</span></div>';
        close_popup();
        function process_data(sData, sTextStatus) {
            var $oPopup = window._popup_win;
            var $oContainer = $oPopup.parent().parent();
            sData = sData.replace(/[\s\S]+<body.+?>/, "");
            sData = sData.replace(/<\/body>[\s\S]+/, "");
            
            $oData = $("<div>").html(sData);
            
            $oPopup.html(
                $oData.find("#popup_content").html()
                + '<div style="clear: both;"></div>'
            );
            if (!sTitle) {
                $oContainer.find(".ui-dialog-title").html(
                    $oData.find("#popup_title").html()
                );
            }
            $oPopup.find("input[name=cancel]").click(close_popup);
            $oPopup.find("form").submit(function() {
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
                oEvents = oEvents || {};
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
                    $oPopup.html(sInProgress);
                    $.post(sUrl, oValues, function(sData, sStatus) {
                        if (!sData) {
                            if (oOnAfterSubmit) {
                                oOnAfterSubmit();
                            }
                            close_popup();
                        } else if(sData=="reload") {
                            // "reload" forces the reload of a page
                            $oPopup.html(sReloading);
                            document.location.href = document.location.pathname;
                        } else if(sData.indexOf("redirect") == 0) {
                            // "redirect=/path/" forces redirection to /path/
                            $oPopup.html(sRedirecting);
                            document.location.href = sData.replace(/^redirect=/, "");
                        } else {
                            process_data(sData);
                        }
                    }, "html");
                }
                return false;
            });
        }
        sTitle = sTitle || "";
        iW = parseInt(iW || 584) + 20;
        var bAutoHeight = (iH == "auto");
        var $oPopup = window._popup_win = $('<div>' + sInProgress + '</div>').dialog({
            title: sTitle,
            width: iW,
            height: iH,
            position: ["center", 70],
            resizable: false,
            modal: true
        });
        var $oContainer = $oPopup.parent().parent();
        if (bWarning) {
            $oContainer.addClass("ui-warning-dialog");
        } else {
            $oContainer.removeClass("ui-warning-dialog");
        }
        if (bAutoHeight) {
            $oContainer.css("height", "auto");
        }
        $oContainer.css("overflow", "visible");
        sUrl = sUrl || "";
        if (oData) {
            $.post(sUrl, oData, process_data);
        } else {
            $.get(sUrl, process_data);
        }
    }

}(jQuery));
