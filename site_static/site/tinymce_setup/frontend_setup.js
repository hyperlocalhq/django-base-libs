/* global tinyMCE:false, Typekit:false */
$(document).ready(function() {
    function disableShortcuts(){
        for (var i=0, len=tinyMCE.editors.length; i<len; i++) {
            var editor = tinyMCE.editors[i];
            editor.addShortcut("ctrl+b","nix","Dummy");
            editor.addShortcut("ctrl+i","nix","Dummy");
            editor.addShortcut("ctrl+u","nix","Dummy");
        }

        (function() {
            var config = {
                kitId: 'qru0sat',
                scriptTimeout: 3000
            };
            var h=document.getElementsByTagName("html")[0];h.className+=" wf-loading";var t=setTimeout(function(){h.className=h.className.replace(/(\s|^)wf-loading(\s|$)/g," ");h.className+=" wf-inactive"},config.scriptTimeout);var tk=document.createElement("script"),d=false;tk.src='//use.typekit.net/'+config.kitId+'.js';tk.type="text/javascript";tk.async="true";tk.onload=tk.onreadystatechange=function(){var a=this.readyState;if(d||a&&a!="complete"&&a!="loaded")return;d=true;clearTimeout(t);try{Typekit.load(config);}catch(b){}};var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(tk,s);
        })();
    }        
    $('textarea.tinymce').tinymce({
        // Location of TinyMCE script
        script_url: window.settings.STATIC_URL + 'site/tinymce/jscripts/tiny_mce/tiny_mce.js',

        valid_elements: "p,br,a",
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

        paste_auto_cleanup_on_paste: true,
        paste_text_sticky: true,
        paste_remove_spans: true,
        paste_remove_styles: true,
        paste_remove_styles_if_webkit: true,
        paste_text_linebreaktype: true,
        
        oninit: disableShortcuts,
        setup: function(ed) {
            ed.addCommand('Dummy', function(){});
            ed.onInit.add(function(ed) {
              ed.pasteAsPlainText = true;
            });
        },        
        // CSS

        content_css: window.settings.STATIC_URL + 'site/css/frontend_tinymce.css',

        popup_css: window.settings.STATIC_URL + 'site/css/frontend_tinymce_popup.css'
    });
});

