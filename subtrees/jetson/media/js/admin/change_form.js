(function($) {
    $(document).ready(function() {
        $('a.viewsitelink').click(function() {
            window.open(
                $(this).attr("href"),
                '_blank',
                'scrollbars=1,location=1,resizable=1,status=1'
            );
            return false;
        });
    });
}(jQuery));
