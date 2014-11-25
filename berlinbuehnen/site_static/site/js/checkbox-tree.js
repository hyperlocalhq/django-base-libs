/*global self:false, jQuery:false */

(function($, undefined) {
    $(function() {
        $('.tree').each(function() {
            var $tree = $(this);
            $(':checkbox', $tree).bind('activate', function() {
                var $li = $(this).closest('li');
                if ($(this).attr('checked')) {
                    $li.find('ul').show();
                    $li.parents('ul').show();
                } else {
                    $li.find('ul').hide().find(':checked').attr('checked', null);
                }
            }).trigger('activate').click(function() {
                $(this).trigger('activate');
            });
        })
    });
}(jQuery));
