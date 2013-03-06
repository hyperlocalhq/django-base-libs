$(document).ready(function() {
    $('textarea.tinymce').tinymce({
        // Location of TinyMCE script
        script_url: window.settings.STATIC_URL + 'site/tinymce/jscripts/tiny_mce/tiny_mce.js',

        // General options
        height: 300,
        resizable: "yes",
        theme: "advanced",
        plugins: "pagebreak,style,iespell,searchreplace,paste",

        // Theme options
        theme_advanced_buttons1: "",
        // theme_advanced_buttons1: "cut,copy,paste,pastetext,pasteword,|,search,replace",
        // theme_advanced_buttons2: "bullist,numlist,|,undo,redo,|,link,unlink,cleanup",
        theme_advanced_toolbar_location: "",
        theme_advanced_statusbar_location : "",
        theme_advanced_toolbar_align: "left",
        // theme_advanced_resizing: true,
        theme_advanced_resize_horizontal: false,
        // theme_advanced_statusbar_location: "bottom",
        theme_advanced_resizing_min_height: 150,

        paste_auto_cleanup_on_paste : true,
        paste_remove_spans: true,
        paste_remove_styles: true,
        paste_remove_styles_if_webkit: true,
        paste_text_linebreaktype: true,
        
        // CSS

        content_css: window.settings.STATIC_URL + 'site/css/frontend_tinymce.css',

        popup_css: window.settings.STATIC_URL + 'site/css/frontend_tinymce_popup.css'
    });
});

