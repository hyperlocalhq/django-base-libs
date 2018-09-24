/* jshint unused:false, eqnull:false */
/* global self: false */
/* global jQuery: false */
/* global qq: false */
/* global translatable_file_uploader_options: false */
/* global lazyload_images: false */
(function($, undefined) {
    function reinit() {
        lazyload_images();
        var dragCheck = false;
        $('#photos').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #photos>*', function() {
                $('#photos').sortable({
                    start: function(){
                        // On drag set that flag to true
                        dragCheck = true;
                    },
                    stop: function(){
                        // On stop of dragging reset the flag back to false
                        setTimeout(function() {
                            dragCheck = false;
                        }, 500);
                    },
                    placeholder: "ui-state-highlight",
                    update: function(event, ui) {
                        var tokens = [];
                        $('.photo', '#photos').each(function() {
                            if ($(this).data('token')) {
                                tokens[tokens.length] = $(this).data('token');
                            }
                        });
                        $.post(load_url, {ordering: tokens.join(',')});
                    },
                    forcePlaceholderSize: true,
                    create: function() {
                        var list = this;
                        var resize = function(){
                            $(list).css("height", "auto");
                            //$(list).height($(list).height());
                        };
                        // $(list).height($(list).height());
                        $(list).find('img').load(resize).error(resize);
                    }
                });
                $('#photos').disableSelection().find('.edit').click(function() {
                    if (dragCheck) {
                        return false;
                    }
                    $('#edit_photo').load($(this).attr('href') + ' #edit_photo form', edit_photo_loaded);
                    $('#photos').parents('fieldset:first').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $('#add_photo').click(function() {
                    $('#edit_photo').load($(this).attr('href') + ' #edit_photo form', edit_photo_loaded);
                    $('#photos').parents('fieldset:first').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $('#photos').find('.crop').each(function() {
                    if ($(this).attr('href')) {
                        $(this).attr('href', $(this).attr('href').replace(/goto_next=.+$/gim, "goto_next=" + location.href));
                    }
                });
                $(window).trigger('scrollstop');
            });
        });
        $('#photos').parents('fieldset:first').show();
        $('.form-actions:last').show();
    }
    $(document).on('click', '#crop_list_image', function() {
        location.href = $('#photos').find('.crop_list_image:first').attr('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        return false;
    });
    $(document).on('click', '#crop_cover_image', function() {
        location.href = $('#photos').find('.crop_cover_image:first').attr('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        return false;
    });
    function edit_photo_loaded() {
        $('textarea').autosize();

        $('#button-id-cancel').click(function() {
            $('#edit_photo').html("");
            reinit();
        });
        $('#button-id-crop-photo').click(function() {
            location.href = $(this).data('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        });
        $('#button-id-delete-photo').click(function() {
            var delete_url = $(this).data('href');
            $('#deleteConfirmation').removeClass('hide').modal('show');
            $('#button-id-confirm-deletion').click(function() {
                $.post(delete_url, {}, function() {
                    $('#deleteConfirmation').modal('hide');
                    $('#edit_photo').html("");
                    reinit();
                });
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
        };
        var options = $.extend(translatable_file_uploader_options, {
            allowedExtensions: ['gif', 'jpg', 'png', 'tif', 'bmp'],
            action: '/' + self.settings.lang + '/helper/ajax-upload/',
            element: $('#image_uploader')[0],
            multiple: false,
            onComplete: function(id, fileName, responseJSON) {
                if(responseJSON.success) {
                    $('.messages').html("");
                    // set the original to media_file_path
                    $('#id_media_file_path').val(responseJSON.path);
                    // load the modified version for the preview
                    $.post('/' + self.settings.lang + '/helper/modified-path/', {
                        file_path: self.settings.media_url + responseJSON.path,
                        mod_sysname: 'medium'
                    }, function(data, textStatus, jqXHR) {
                        console.log(data);
                        $('#image_preview').html('<img class="img-responsive" alt="" src="' + data + '" />');
                        $('#image_uploader').hide();
                        $('#image_help_text').hide();
                    },
                    'text'
                    );
                }
            },
            onAllComplete: function(uploads) {
                // uploads is an array of maps
                // the maps look like this: {file: FileObject, response: JSONServerResponse}
                $('.qq-upload-success').fadeOut("slow", function() {
                    $(this).remove();
                });
            },
            params: {
                'csrf_token': $('input[name="csrfmiddlewaretoken"]').val(),
                'csrf_name': 'csrfmiddlewaretoken',
                'csrf_xname': 'X-CSRFToken'
            },
            showMessage: function(message) {
                $('.messages').html('<div class="alert alert-danger">' + message + '</div>');
            }
        });
        var uploader = new qq.FileUploader(options);
    }
    $(function() {
        reinit();
    });
})(jQuery);
