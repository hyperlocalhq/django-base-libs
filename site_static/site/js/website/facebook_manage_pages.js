(function($, undefined) {
    // initialize the library with the API key
    FB.init({
        apiKey: settings.FACEBOOK_APP_ID,
        status: true,
        cookie: true,
        xfbml: false,
        oauth: true
    });
    
    var oScriptsRe = /<script\b[^>]*>([\s\S]*?)<\/script>/gm;
    function execute_scripts(responseText, textStatus, XMLHttpRequest) {
        var sScripts = "";
        responseText.replace(
            oScriptsRe,
            function($0, $1) {
                sScripts += $1;
                return $0;
            }
        );
        eval(sScripts);
    }
    
    $('.facebook_connect_page').live("click", function() {
        var $oForm = $(this).parents('form');
        var $oFormContainer = $oForm.parent();
        $oFormContainer.load("/" + settings.lang + "/facebook/pages/ #" + $oFormContainer.attr("id") + ">*", {
            institution: $oForm.find('[name=institution]').val(),
            page: $oForm.find('[name=page]').val(),
            action: "connect"
        });
    });
    
    $('.facebook_disconnect_page').live("click", function() {
        var $oForm = $(this).parents('form');
        var $oFormContainer = $oForm.parent();
        close_popup();
        var sTitle = gettext('Disconnection');
        var iW = 552;
        iH = "auto";
        var bAutoHeight = (iH == "auto");
        var $oButtons = $('<div class="buttons"></div>');
        $('<input type="button" class="button_bad" />').val(
            gettext("No").toUpperCase()
        ).click(close_popup).appendTo($oButtons);
        $('<input type="button" class="button_good" />').val(
            gettext("Yes").toUpperCase()
        ).click(function() {
            close_popup();
            $oFormContainer.load("/" + settings.lang + "/facebook/pages/ #" + $oFormContainer.attr("id") + ">*", {
                institution: $oForm.find('[name=institution]').val(),
                action: "disconnect"
            });
        }).appendTo($oButtons);
        var $sPopupHTML = $(
            '<div><p>' + gettext('Are you sure you want to unlink your institution with facebook page?') + '</p></div>'
        ).append($oButtons).append($('<div style="clear:both"></div>'));
        var $oPopup = window._popup_win = $($sPopupHTML).dialog({
            title: sTitle,
            width: iW,
            height: iH,
            position: ["center", 70],
            resizable: false
        });
        var $oContainer = $oPopup.parent().parent();
        $oContainer.addClass("ui-warning-dialog");
        if (bAutoHeight) {
            $oContainer.css("height", "auto");
        }
        $oContainer.css("overflow", "visible");
        return false;
    });
}(jQuery));

