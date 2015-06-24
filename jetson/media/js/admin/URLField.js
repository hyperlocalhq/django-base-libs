(function($, undefined) {
    $(function() {
        $(".vURLField").blur(function() {
            $(this).next(".dyn_url_link").remove();
            var sLink = $(this).val();
            if (sLink) {
                $('<a href="' + sLink + '" class="dyn_url_link open-link" title="' + gettext("Open Link") + '"><span>' + gettext("Open Link") + '</span></a>').insertAfter($(this)).click(function() {
                    window.open($(this).attr("href"), '_blank', 'scrollbars=1,location=1,resizable=1,status=1');
                    return false;
                });
            }
        }).blur();
    });
}(jQuery));
