$(document).ready(function() {
    $('textarea.hasMarkupType').tinymce({
        // Location of TinyMCE script
        script_url: settings.STATIC_URL + 'site/tinymce/jscripts/tiny_mce/tiny_mce.js',

        // General options
        theme: "advanced",
        plugins: "pagebreak,style,iespell,searchreplace,paste",

        // Theme options
        theme_advanced_buttons1: "cut,copy,paste,pastetext,pasteword,|,search,replace",
        theme_advanced_buttons2: "bullist,numlist,|,undo,redo,|,link,unlink,cleanup",
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: "none",
        theme_advanced_resizing: true,
        
        // CSS
        content_css: settings.STATIC_URL + 'site/css/frontend_tinymce.css',
        popup_css: settings.STATIC_URL + 'site/css/frontend_tinymce_popup.css'
    });
});

