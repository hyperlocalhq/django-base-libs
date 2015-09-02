(function($) {
    $(document).ready(function() {
        function setTinyMce(sId) {
            tinyMCE.execCommand("mceAddControl", true, sId);
        }
        function unsetTinyMce(sId) {
            tinyMCE.execCommand("mceRemoveControl", true, sId);
        }
    
        function initRTE() {
            toggleMarkup = function() {
                sMarkupType = $(this).val();
                // get the corrsponding textarea fields id
                var token = $(this).attr("id").match(/(.*?)_markup_type/g);
                var sId = RegExp.$1;
                if (sMarkupType == 'hw') {
                    setTinyMce(sId);
                } else {
                    unsetTinyMce(sId);
                }
            };
            $('.markupType').each(toggleMarkup).change(toggleMarkup);
        }
        window.setTimeout(initRTE,500);
    });
}(django.jQuery));
