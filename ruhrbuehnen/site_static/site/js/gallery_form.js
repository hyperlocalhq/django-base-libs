/* jshint unused:false, eqnull:false */
/* global self: false */
/* global jQuery: false */
/* global qq: false */
/* global translatable_file_uploader_options: false */
/* global lazyload_images: false */
(function($, undefined) {
    function reinit_videos() {
        var dragCheck = false;
        $('#videos').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #videos>*', function() {
                $('#videos').sortable({
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
                        $('.video', '#videos').each(function() {
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
                $('#videos').disableSelection().find('.edit').click(function() {
                    if (dragCheck) {
                        return false;
                    }
                    $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_video_loaded);
                    $('#media_item_overviews').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $(window).trigger('scrollstop');
            });
        });
        $('#media_item_overviews').show();
        $('.form-actions:last').show();
    }
    $('#add_video').click(function() {
        $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_video_loaded);
        $('#media_item_overviews').hide();
        $('.form-actions:last').hide();
        return false;
    });
    function edit_video_loaded() {
        $("select").not('[name*="__prefix__"]').selectbox();

        $('textarea').autosize();

        $('#submit-id-cancel').click(function(e) {
            e.preventDefault();
            $('#edit_media_item').html("");
            reinit_videos();
        });
        $('#button-id-delete-video').click(function() {
            var delete_url = $(this).data('href');
            $('#deleteConfirmation').removeClass('hide').modal('show');
            $('#button-id-confirm-deletion').click(function() {
                $.post(delete_url, {}, function() {
                    $('#deleteConfirmation').modal('hide');
                    $('#edit_media_item').html("");
                    reinit_videos();
                });
                return false;
            });
        });
        $('#edit_media_item form').attr('target', 'hidden_iframe');
        self.hidden_iframe_loaded = function(html) {
            var $form = $('<div>' + html + '</div>').find('form');
            if ($form.length) {
                $('#edit_media_item').html('').append($form);
                edit_video_loaded();
            } else {
                $('#edit_media_item').html('');
                reinit_videos();
            }
        };
    }
    
    
    
    function reinit_streamings() {
        var dragCheck = false;
        $('#streamings').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #streamings>*', function() {
                $('#streamings').sortable({
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
                        $('.streaming', '#streamings').each(function() {
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
                $('#streamings').disableSelection().find('.edit').click(function() {
                    if (dragCheck) {
                        return false;
                    }
                    $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_streaming_loaded);
                    $('#media_item_overviews').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $(window).trigger('scrollstop');
            });
        });
        $('#media_item_overviews').show();
        $('.form-actions:last').show();
    }
    $('#add_streaming').click(function() {
        $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_streaming_loaded);
        $('#media_item_overviews').hide();
        $('.form-actions:last').hide();
        return false;
    });
    function edit_streaming_loaded() {
        $("select").not('[name*="__prefix__"]').selectbox();

        $('textarea').autosize();

        $('#submit-id-cancel').click(function(e) {
            e.preventDefault();
            $('#edit_media_item').html("");
            reinit_streamings();
        });
        $('#button-id-delete-streaming').click(function() {
            var delete_url = $(this).data('href');
            $('#deleteConfirmation').removeClass('hide').modal('show');
            $('#button-id-confirm-deletion').click(function() {
                $.post(delete_url, {}, function() {
                    $('#deleteConfirmation').modal('hide');
                    $('#edit_media_item').html("");
                    reinit_streamings();
                });
                return false;
            });
        });
        $('#edit_media_item form').attr('target', 'hidden_iframe');
        self.hidden_iframe_loaded = function(html) {
            var $form = $('<div>' + html + '</div>').find('form');
            if ($form.length) {
                $('#edit_media_item').html('').append($form);
                edit_streaming_loaded();
            } else {
                $('#edit_media_item').html('');
                reinit_streamings();
            }
        };
    }
    
    
    
    
    function reinit_images() {
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
                    $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_photo_loaded);
                    $('#media_item_overviews').hide();
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
        $('#media_item_overviews').show();
        $('.form-actions:last').show();
    }
    $('#add_photo').click(function() {
        $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_photo_loaded);
        $('#media_item_overviews').hide();
        $('.form-actions:last').hide();
        return false;
    });
    $(document).on('click', '#crop_list_image', function() {
        location.href = $('#photos').find('.crop_list_image:first').attr('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        return false;
    });
    $(document).on('click', '#crop_cover_image', function() {
        location.href = $('#photos').find('.crop_cover_image:first').attr('href').replace(/goto_next=.+$/, 'goto_next=' + location.href);
        return false;
    });
    function edit_photo_loaded() {
        $("select").not('[name*="__prefix__"]').selectbox();

        $('textarea').autosize();

        $('#submit-id-cancel').click(function(e) {
            e.preventDefault();
            $('#edit_media_item').html("");
            reinit_images();
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
                    $('#edit_media_item').html("");
                    reinit_images();
                });
                return false;
            });
        });
        $('#edit_media_item form').attr('target', 'hidden_iframe');
        self.hidden_iframe_loaded = function(html) {
            var $form = $('<div>' + html + '</div>').find('form');
            if ($form.length) {
                $('#edit_media_item').html('').append($form);
                edit_photo_loaded();
            } else {
                $('#edit_media_item').html('');
                reinit_images();
            }
        };
        if ($('#image_uploader').length) {
            var options = $.extend(translatable_file_uploader_options, {
                allowedExtensions: ['gif', 'jpg', 'png'],
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
                            mod_sysname: 'gallery_image'
                        }, function(data, textStatus, jqXHR) {
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
    }
    
    

    
    function reinit_pdfs() {
        var dragCheck = false;
        $('#pdfs').each(function() {
            var load_url = $(this).data("load-url");
            $(this).load(load_url + ' #pdfs>*', function() {
                $('#pdfs').sortable({
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
                        $('.pdf', '#pdfs').each(function() {
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
                $('#pdfs').disableSelection().find('.edit').click(function() {
                    if (dragCheck) {
                        return false;
                    }
                    $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_pdf_loaded);
                    $('#media_item_overviews').hide();
                    $('.form-actions:last').hide();
                    return false;
                });
                $(window).trigger('scrollstop');
            });
        });
        $('#media_item_overviews').show();
        $('.form-actions:last').show();
    }
    $('#add_pdf').click(function() {
        $('#edit_media_item').load($(this).attr('href') + ' #edit_media_item form', edit_pdf_loaded);
        $('#media_item_overviews').hide();
        $('.form-actions:last').hide();
        return false;
    });
    function edit_pdf_loaded() {
        $("select").not('[name*="__prefix__"]').selectbox();

        $('textarea').autosize();

        $('#submit-id-cancel').click(function(e) {
            e.preventDefault();
            $('#edit_media_item').html("");
            reinit_pdfs();
        });
        $('#button-id-delete-pdf').click(function() {
            var delete_url = $(this).data('href');
            $('#deleteConfirmation').removeClass('hide').modal('show');
            $('#button-id-confirm-deletion').click(function() {
                $.post(delete_url, {}, function() {
                    $('#deleteConfirmation').modal('hide');
                    $('#edit_media_item').html("");
                    reinit_pdfs();
                });
                return false;
            });
        });
        $('#edit_media_item form').attr('target', 'hidden_iframe');
        self.hidden_iframe_loaded = function(html) {
            var $form = $('<div>' + html + '</div>').find('form');
            if ($form.length) {
                $('#edit_media_item').html('').append($form);
                edit_pdf_loaded();
            } else {
                $('#edit_media_item').html('');
                reinit_pdfs();
            }
        };
        if ($('#pdf_uploader').length) {
            var options = $.extend(translatable_file_uploader_options, {
                allowedExtensions: ['pdf'],
                action: '/' + self.settings.lang + '/helper/ajax-upload/',
                element: $('#pdf_uploader')[0],
                multiple: false,
                onComplete: function(id, fileName, responseJSON) {
                    if(responseJSON.success) {
                        $('.messages').html("");
                        // set the original to media_file_path
                        $('#id_media_file_path').val(responseJSON.path);
                        // load the modified version for the preview
                        $.post('/' + self.settings.lang + '/helper/modified-path/', {
                            file_path: responseJSON.path,
                            mod_sysname: 'medium'
                        }, function(data, textStatus, jqXHR) {
                            $('#pdf_preview').html('<img class="img-responsive" alt="" src="' + window.settings.STATIC_URL + 'site/img/pdf.png" />');
                            $('#pdf_uploader').hide();
                            $('#pdf_help_text').hide();
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
    }
    
    $(function() {
        reinit_videos();
        reinit_streamings();
        reinit_images();
        reinit_pdfs();
    });
})(jQuery);
