/**
 TinyMCE settings for administration.
 */

var FILEBROWSER_MEDIA_URL = "/uploads/";
var FILEBROWSER_URL_ADMIN = "/admin/filebrowser/browse/";

function CustomOnChangeHandler(inst) {
    if (window.customOnChangeHandler) {
        window.customOnChangeHandler(inst);
    }
}

function CustomFileBrowser(field_name, url, type, win) {
    
    // var cmsURL = "/admin/filebrowser/?pop=2";
    var cmsURL = FILEBROWSER_URL_ADMIN + "?pop=2";
    cmsURL = cmsURL + "&type=" + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no",
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId,
    });
    return false;
}

function CustomCleanup(type, value) {
    switch (type) {
        case "get_from_editor":
            // remove multiple spaces
            value = value.replace(/\s{2,}/g, "&nbsp;");
            // remove multiple breaks
            value = value.replace(/(\<br \/\>){2,}/g, "<br />");
            // remove empty paragraphs
            value = value.replace(/\<p\>\s+\<\/p\>/g, "");
            value = value.replace(/\<p\>\<br \/\>\s\<\/p\>/g, "");
            value = value.replace(/\<p\>\s\<br \/\>\<\/p\>/g, "");
            // remove empty headlines
            value = value.replace(/\<h1\>\s+\<\/h1\>/g, "");
            value = value.replace(/\<h2\>\s+\<\/h2\>/g, "");
            value = value.replace(/\<h3\>\s+\<\/h3\>/g, "");
            value = value.replace(/\<h4\>\s+\<\/h4\>/g, "");
            value = value.replace(/\<h1\>(\&nbsp\;)+\<\/h1\>/g, "");
            value = value.replace(/\<h2\>(\&nbsp\;)+\<\/h2\>/g, "");
            value = value.replace(/\<h3\>(\&nbsp\;)+\<\/h3\>/g, "");
            value = value.replace(/\<h4\>(\&nbsp\;)+\<\/h4\>/g, "");
            // remove headlines with breaks
            value = value.replace(/\<h1\>\<br \/\>\<\/h1\>/g, "");
            value = value.replace(/\<h2\>\<br \/\>\<\/h2\>/g, "");
            value = value.replace(/\<h3\>\<br \/\>\<\/h3\>/g, "");
            value = value.replace(/\<h4\>\<br \/\>\<\/h4\>/g, "");
            // remove empty listelements
            value = value.replace(/\<li\>\s+\<\/li\>/g, "");
            value = value.replace(/\<li\>\s+\<br \/\>\<\/li\>/g, "");
            value = value.replace(/\<li\>\<br \/\>\<\/li\>/g, "");
            value = value.replace(/\<ol\>\s+\<\/ol\>/g, "");
            value = value.replace(/\<ul\>\s+\<\/ul\>/g, "");
    }
    return value;
}

// original configuration from grappelli
oTinyMCEConfig = {
    
    // main settings
    mode: "textareas",
    //elements: "summary, body",
    theme: "advanced",
    language: "de",
    skin: "grappelli",
    browsers: "gecko",
    dialog_type: "window",
    
    // general settings
    width: '758',
    height: '550',
    indentation: '10px',
    fix_list_elements: true,
    relative_urls: false,
    remove_script_host: true,
    accessibility_warnings: false,
    object_resizing: false,
    cleanup_on_startup: true,
    //forced_root_block: "p",
    remove_trailing_nbsp: true,
    
    // callbacks
    file_browser_callback: "CustomFileBrowser",
    //cleanup_callback : "CleanupCallback",
    
    // theme_advanced
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "bottom",
    theme_advanced_buttons1: "formatselect,styleselect,|,bold,italic,underline,|,bullist,numlist,blockquote,|,undo,redo,|,link,unlink,|,image,|,fullscreen,|,grappelli_adv",
    theme_advanced_buttons2: "search,|,pasteword,template,media,charmap,|,code,|,table,cleanup,grappelli_documentstructure",
    theme_advanced_buttons3: "",
    theme_advanced_path: false,
    theme_advanced_blockformats: "p,h2,h3,h4,pre",
    theme_advanced_resizing: true,
    theme_advanced_resize_horizontal: false,
    theme_advanced_resizing_use_cookie: true,
    advlink_styles: "intern=internal;extern=external",
    
    // plugins
    plugins: "fbimage,advlink,fullscreen,paste,media,searchreplace,grappelli,grappelli_contextmenu,template,noneditable",
    advimage_update_dimensions_onchange: true,
    
    // grappelli settings
    grappelli_adv_hidden: false,
    grappelli_show_documentstructure: 'on',
    
    // templates
    template_templates: [
        {
            title : "2 Spalten, symmetrisch",
            src : "/grappelli/tinymce/templates/2col/",
            description : "Symmetrical 2 Columns."
        },
        {
            title : "2 Spalten, symmetrisch mit Unterteilung",
            src : "/grappelli/tinymce/templates/4col/",
            description : "Asymmetrical 2 Columns: big left, small right."
        },
    ],
    
    // elements
    // removed valid_elements, extended_valid_elements, valid_child_elements – now using the defaults
    invalid_elements: 'script',
    
}


// custom changes by studio 38

oTinyMCEConfig.mode = 'none';
oTinyMCEConfig.language = window.settings.LANGUAGE_CODE;
oTinyMCEConfig.object_resizing = true;
oTinyMCEConfig.cleanup_on_startup = true;
oTinyMCEConfig.forced_root_block = "p";
oTinyMCEConfig.remove_trailing_nbsp = true;
oTinyMCEConfig.onchange_callback = CustomOnChangeHandler;
oTinyMCEConfig.FILEBROWSER_URL_ADMIN = FILEBROWSER_URL_ADMIN;
oTinyMCEConfig.grappelli_show_documentstructure = 'off';
oTinyMCEConfig.width = undefined;

oTinyMCEConfig.style_formats = [
    {title: '[all] clearfix', selector: "*", classes: 'clearfix'},
    {title: 'Image styles'},
    {title: '[img] Image left-aligned', selector: 'img', classes: 'img_left'},
    {title: '[img] Image right-aligned', selector: 'img', classes : 'img_right'},
    {title: '[img] Image Block', selector: 'img', classes: 'img_block'}
];

tinymce.PluginManager.load('paste', window.settings.JETSON_MEDIA_URL + 'tinymce_setup/plugins/paste/editor_plugin.js');
tinymce.PluginManager.load('fbimage', window.settings.JETSON_MEDIA_URL + 'tinymce_setup/plugins/fbimage/editor_plugin.js');
