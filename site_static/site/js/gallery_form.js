(function($, undefined) {
    function reinit() {
        $('#photos').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #photos>*', function() {
                $('#photos').sortable({
                    placeholder: "ui-state-highlight",
                    update: function(event, ui) {
                        var tokens = []
                        $('.item', '#photos').each(function() {
                            if ($(this).data('token')) {
                                tokens[tokens.length] = $(this).data('token');
                            }
                        });
                        $.post(load_url, {ordering: tokens.join(',')});
                    },
                    forcePlaceholderSize: true,
                    create: function(){
                        var list = this;
                        resize = function(){
                            $(list).css("height","auto");
                            $(list).height($(list).height());
                        };
                        // $(list).height($(list).height());
                        $(list).find('img').load(resize).error(resize);
                    }                    
                })
                $('#photos').disableSelection().find('.edit').click(function() {
                    $('#edit_photo').load($(this).attr('href') + ' .content form', edit_photo_loaded);
                    $('#photos').parents('fieldset:first').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $('#photos').find('.crop').each(function() {
                    $(this).attr('href', $(this).attr('href').replace(/goto_next=.+$/gim, "goto_next=" + location.href));
                });
                $('#add_photo').click(function() {
                    $('#edit_photo').load($(this).attr('href') + ' .content form', edit_photo_loaded);
                    $('#photos').parents('fieldset:first').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $(window).trigger('scrollstop');
            });
        });
        $('#photos').parents('fieldset:first').show();
        $('.form-actions:last').show();
        
    }
    function edit_photo_loaded() {
        $('#button-id-cancel').click(function() {
            $('#edit_photo').html("");
            reinit();
        });
        $('#button-id-crop-photo').click(function() {
            location.href = $(this).data('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        });
        $('#button-id-delete-photo').click(function() {
            var delete_url = $(this).data('href');
            $('#deleteConfirmation').modal('show');
            $('#button-id-confirm-deletion').click(function() {
                $.post(delete_url, {}, function() {
                    $('#deleteConfirmation').modal('hide')
                    $('#edit_photo').html("");
                    reinit();
                })
                return false;
            });
        });
        $('#edit_photo form').attr('target', 'hidden_iframe');
        self.hidden_iframe_loaded = function(html) {
            var $form = $('<div>' + html + '</div>').find('form');
            if ($form.length) {
                $('#edit_photo').html('').append($form);
                edit_photo_loaded();
            } else {
                $('#edit_photo').html('');
                reinit();
            }
        }
    }    
    
    $(function() {
        reinit();
    });
})(jQuery);
