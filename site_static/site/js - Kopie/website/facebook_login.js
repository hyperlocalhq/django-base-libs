(function($, undefined) {
    // initialize the library with the API key
    FB.init({
        apiKey: settings.FACEBOOK_APP_ID,
        status: true,
        cookie: true,
        xfbml: false,
        oauth: true
    });
    
    // fetch the status on load
    function goto_next($oButton) {
        var sGoToNext = "";
        var $oGoToNext = $oButton.parents("form").find("[name=goto_next]");
        if ($oGoToNext.length) {
            sGoToNext = $oGoToNext.val();
        }
        return sGoToNext
    }
    
    var bLoggedIn = false;
    var $oFacebookLoginForm = null;
    
    $('.facebook_login').live('click', function() {
        $oFacebookLoginForm = $(this).parents("form");            
        if (bLoggedIn) {
            $oFacebookLoginForm.find("[name=access_token]").val(FB.getAccessToken());
            $oFacebookLoginForm.find("[name=uid]").val(FB.getUserID());
            $oFacebookLoginForm.submit();
        } else {
            FB.login(handleSessionResponse, {
                scope: settings.FACEBOOK_APP_REQUIRED_PERMISSIONS
            });
        }
        return false;
    });
    
    function loginStatusReady(response) {
        bLoggedIn = !!response.session;
    }
    
    // handle a session response from any of the auth related calls
    function handleSessionResponse(response) {
        // if we dont have a session, just hide the user info
        if (!response.authResponse) {
            return;
        }
        $oFacebookLoginForm.find("[name=access_token]").val(FB.getAccessToken());
        $oFacebookLoginForm.find("[name=uid]").val(FB.getUserID());
        $oFacebookLoginForm.submit();
    }
    
    FB.getLoginStatus(loginStatusReady);
    FB.Event.subscribe('auth.statusChange', loginStatusReady);
    
}(jQuery));
