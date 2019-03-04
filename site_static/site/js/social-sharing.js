$(function() {
    // link selector and pop-up window size
    var config = {
        link: "a.social-sharing",
        width: 626,
        height: 436
    };
    // add handler links
    $(config.link).on('click', function() {
        // popup position
        var px = Math.floor(((screen.availWidth || 1024) - config.width) / 2),
            py = Math.floor(((screen.availHeight || 700) - config.height) / 2);
        // open popup
        var popup = window.open($(this).attr('href'), "social",
            "width="+config.width+",height="+config.height+
            ",left="+px+",top="+py+
            ",location=0,menubar=0,toolbar=0,status=0,scrollbars=1,resizable=1");
        if (popup) {
            popup.focus();
            return false;
        }
        return true;
    });
});