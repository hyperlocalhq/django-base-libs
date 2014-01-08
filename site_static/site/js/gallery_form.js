(function($, undefined) {
    function reinit() {
        $('#photos').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #photos>*', function() {
                $('#photos').sortable({
                    placeholder: "ui-state-highlight",
                    update: function(event, ui) {
                        var tokens = []
                        $('.photo', '#photos').each(function() {
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
                            //$(list).height($(list).height());
                        };
                        // $(list).height($(list).height());
                        $(list).find('img').load(resize).error(resize);
                    }                    
                })
                $('#photos').disableSelection().find('.edit').click(function() {
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
    function edit_photo_loaded() {
        $('textarea').autosize();
        activate_form_language(window.settings.lang);

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
        var options = $.extend(translatable_file_uploader_options, {
            allowedExtensions: ['gif', 'jpg', 'png', 'tif', 'bmp'],               
            action: "/helper/ajax-upload/",
            element: $('#image_uploader')[0],
            multiple: false,
            onComplete: function(id, fileName, responseJSON) {
                if(responseJSON.success) {
                    $('.messages').html("");
                    // set the original to media_file_path
                    $('#id_media_file_path').val('uploads/' + fileName);
                    // load the modified version for the preview
                    $.post('/helper/modified-path/', {
                        file_path: 'uploads/' + fileName,
                        mod_sysname: 'one_column'
                    }, function(data, textStatus, jqXHR) {
                        $('#image_preview').html('<img class="img-responsive" alt="" src="/media/' + data + '" />');
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
                $('.messages').html('<div class="alert alert-error">' + message + '</div>');
            }
        });
        var uploader = new qq.FileUploader(options);
    }    
    $(function() {
        reinit();
    });
})(jQuery);
