(function($) {
    $(document).ready(function() {
        function setCkEditor(sId) {
            CKEDITOR.replace(sId);
        }
        function unsetCkEditor(sId) {
            var ckInstance = CKEDITOR.instances[sId];
            if (ckInstance) {
                ckInstance.destroy();
            }
        }
    
        function initRTE() {
            toggleMarkup = function() {
                sMarkupType = $(this).val();
                // get the corrsponding textarea fields id
                var token = $(this).attr("id").match(/(.*?)_markup_type/g);
                var sId = RegExp.$1;
                if (sMarkupType == 'hw') {
                    setCkEditor(sId);
                } else {
                    unsetCkEditor(sId);
                }
            };
            $('.markupType').each(toggleMarkup).change(toggleMarkup);
        }
        window.setTimeout(initRTE,500);
    });
}(django.jQuery));
