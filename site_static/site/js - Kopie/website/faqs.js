(function($, undefined) {
    $(document).ready(function() {
        if (location.hash) {
            var $oQuestion = $("#" + location.hash.replace(/#/, ""));
            $oQuestion.find(".openlist").click();
            setTimeout(function() {
                $oQuestion.autoscroll();
            }, 1000);
            
        }
    });
}(jQuery));
