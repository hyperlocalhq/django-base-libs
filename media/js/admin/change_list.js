$(document).ready(function() {
    $('a.content_object').click(function() {
        window.open(
            $j(this).attr("href"),
            '_blank',
            'scrollbars=1,location=1,resizable=1,status=1'
        );
        return false;
    });
});
