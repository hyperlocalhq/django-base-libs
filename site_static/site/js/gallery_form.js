(function($, undefined) {
    function reinit() {
        $('#photos').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #photos>*', function() {
                $('#photos').sortable({
                    placeholder: "ui-state-highlight",
                    update: function(event, ui) {
                        var tokens = []
                        $('.img_and_desc', '#photos').each(function() {
                            tokens[tokens.length] = $(this).data('token');
                        });
                        $.post(load_url, {ordering: tokens.join(',')});
                    }
                })
                $('#photos').disableSelection().find('.edit_photo').click(function() {
                    $('#edit_photo').load($(this).attr('href') + ' .content form', function() {
                        $('#id_goto_next').val(location.href);
                        $('#button-id-cancel').click(function() {
                            $('#edit_photo').html("");
                        });
                    });
                    $('#photos').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $('#photos').find('.delete_photo').click(function() {
                    $('#edit_photo').load($(this).attr('href') + ' .content form', function() {
                        $('#id_goto_next').val(location.href);
                        $('#button-id-cancel').click(function() {
                            $('#edit_photo').html("");
                            reinit();
                        });
                    });
                    $('#photos').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $('#photos').find('.crop_photo').each(function() {
                    $(this).attr('href', $(this).attr('href').replace(/goto_next=.+$/gim, "goto_next=" + location.href));
                });
            });
        });
        $('#photos').show();
        $('.form-actions:last').show();
    }
    $(function() {
        reinit();
        $('#add_photo').click(function() {
            $('#edit_photo').load($(this).attr('href') + ' .content form', function() {
                $('#id_goto_next').val(location.href);
                $('#button-id-cancel').click(function() {
                    $('#edit_photo').html("");
                    reinit();
                });
            });
            $('#photos').hide();
            $('.form-actions:last').hide();
            return false;
        });
    });
})(jQuery);
