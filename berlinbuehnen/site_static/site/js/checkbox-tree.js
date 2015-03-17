/*global self:false, jQuery:false */

(function($, undefined) {
    $(function() {
        $('.tree').each(function() {
            var $tree = $(this);
            $(':checkbox', $tree).on('activate', function() {
                var $this = $(this);
                $form_group = $this.closest('.form-group');
                if ($this.attr('checked')) {
                    if ($form_group.is('.level-0')) {
                        $form_group.nextUntil('.form-group.level-0').show();
                    } else {
                        $form_group.prevAll('.form-group.level-0:first').find(':checkbox').attr('checked', 'checked').trigger('activate');
                    }
                } else {
                    if ($form_group.is('.level-0')) {
                        $form_group.nextUntil('.form-group.level-0').hide().find(':checkbox').attr('checked', null);
                    }
                }
            }).trigger('activate').click(function() {
                $(this).trigger('activate');
            });
        })
    });
}(jQuery));
