(function($, undefined) {
    function form_submit() {
        $("#delete_profile_form").unbind("submit").submit();
    }
    $(document).ready(function() {
        $("#delete_profile_form").submit(function() {
            close_popup();
            var sTitle = gettext('Delete Profile');
            var iW = 552;
            iH = "auto";
            var bAutoHeight = (iH == "auto");
            var $oButtons = $('<div class="buttons"></div>');
            $('<input type="button" class="button_bad" />').val(
                gettext("Cancel").toUpperCase()
            ).click(close_popup).appendTo($oButtons);
            $('<input type="button" class="button_good" />').val(
                gettext("Confirm").toUpperCase()
            ).click(form_submit).appendTo($oButtons);
            var $sPopupHTML = $('<div></div>').append($('#warning_message')).append($oButtons);
            var $oPopup = window._popup_win = $($sPopupHTML).dialog({
                title: sTitle,
                width: iW,
                height: iH,
                position: ["center", 70],
                resizable: false,
                modal: true
            });
            var $oContainer = $oPopup.parent().parent();
            $oContainer.addClass("ui-warning-dialog");
            if (bAutoHeight) {
                $oContainer.css("height", "auto");
            }
            $oContainer.css("overflow", "visible");
            return false;
        });
    });
}(jQuery));
