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
    
    var $oFacebookLoginForm = null;
    $('#facebook_connect').live("click", function() {
        $oFacebookLoginForm = $(this).parents("form");            
        FB.login(function(response) {
            if (!response.authResponse) {
                return;
            }
            $oFacebookLoginForm.find("[name=access_token]").val(FB.getAccessToken());
            $oFacebookLoginForm.find("[name=uid]").val(FB.getUserID());
            $oFacebookLoginForm.submit();
        }, {
            scope: settings.FACEBOOK_APP_REQUIRED_PERMISSIONS
        });
        return false;
    });
    
    $('.facebook_disconnect').live("click", function() {
        var uid = $(this).parent().find('[name="uid"]').val();
        close_popup();
        var sTitle = gettext('Disconnection');
        var iW = 552;
        iH = "auto";
        var bAutoHeight = (iH == "auto");
        var $oButtons = $('<div class="buttonHolder"></div>');
        $('<input type="button" class="secondaryAction" />').val(
            gettext("No").toUpperCase()
        ).click(close_popup).appendTo($oButtons);
        $('<input type="button" class="primaryAction" />').val(
            gettext("Yes").toUpperCase()
        ).click(function() {
            close_popup();
            FB.api(
                {
                    method: 'Auth.revokeAuthorization',
                    params: {uid: uid}
                },
                function(response) {
                    $('#fb_connect_form').load(
                        location.href + " #fb_connect_form form",
                        {
                            a: "disconnect",
                            uid: uid,
                        }, reload_pages
                    );
                }
            );
        }).appendTo($oButtons);
        var $sPopupHTML = $(
            '<div><p>' + gettext('Are you sure you remember your password at CreativeCityBerlin and want to disconnect from facebook account?') + '</p></div>'
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
    $('.facebook_connect_page').live("click", function() {
        var $oForm = $(this).parents('form');
        var $oFormContainer = $oForm.parent();
        $oFormContainer.load("/" + settings.LANGUAGE_CODE + "/facebook/pages/ #" + $oFormContainer.attr("id") + ">*", {
            institution: $oForm.find('[name=institution]').val(),
            page: $oForm.find('[name=page]').val(),
            a: "connect"
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
            $oFormContainer.load("/" + settings.LANGUAGE_CODE + "/facebook/pages/ #" + $oFormContainer.attr("id") + ">*", {
                institution: $oForm.find('[name=institution]').val(),
                a: "disconnect"
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
    
    function reload_pages() {
        if ($("#dyn_profiles").children("li").length > 2) {
            $('#manage_pages').html(
                '<div style="text-align:center"><img alt="" src="' + settings.STATIC_URL + 'site/img/website/indicator.gif" /></div>'
            ).load("/" + settings.LANGUAGE_CODE + "/facebook/pages/ #content>*");
        }
    }
    
    $(document).ready(reload_pages);
    
}(jQuery));

