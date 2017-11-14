/**
 TinyMCE settings for administration.
 */
/**
 TinyMCE settings for administration.
 */

oTinyMCEConfig = {
    
    // main settings
    mode: "textareas",
    //elements: "summary, body",
    theme: "advanced",
    language: "de",
    browsers: "gecko",
    dialog_type: "window",
    
    // general settings
    width: '758',
    height: '300',
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
    //cleanup_callback : "CleanupCallback",
    
    // theme_advanced
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "bottom",
    theme_advanced_buttons3: "",
    theme_advanced_path: false,
    theme_advanced_blockformats: "p,h2,h3,h4,pre",
    theme_advanced_resizing: true,
    theme_advanced_resize_horizontal: false,
    theme_advanced_resizing_use_cookie: true,
    advlink_styles: "intern=internal;extern=external",
    
    // plugins
    plugins: "advimage,advlink,fullscreen,paste,media,searchreplace,grappelli,grappelli_contextmenu,template",
    advimage_update_dimensions_onchange: true,
    
    // grappelli settings
    grappelli_adv_hidden: false,
    grappelli_show_documentstructure: 'on',
    
    // elements
    // removed valid_elements, extended_valid_elements, valid_child_elements – now using the defaults
    invalid_elements: 'script',
}


// custom changes by studio 38

oTinyMCEConfig.mode = 'none';
oTinyMCEConfig.theme_advanced_styles = "[all] clearfix=clearfix;[img] Image left-aligned=img_left;[img] Image left-aligned (no top space)=img_left_nospacetop;[img] Image right-aligned=img_right;[img] Image right-aligned (no top space)=img_right_nospacetop;[img] Image Block=img_block";
oTinyMCEConfig.language = window.settings.lang;
oTinyMCEConfig.object_resizing = true;
oTinyMCEConfig.cleanup_on_startup = true;
oTinyMCEConfig.forced_root_block = "p";
oTinyMCEConfig.remove_trailing_nbsp = true;
oTinyMCEConfig.plugins = "advimage,advlink,fullscreen,paste,media,searchreplace,grappelli,grappelli_contextmenu,template";
oTinyMCEConfig.grappelli_show_documentstructure = 'off';

oTinyMCEConfig.mode = 'textareas';
oTinyMCEConfig.content_css = window.settings.STATIC_URL+"site/css/richtext.css";

oTinyMCEConfig.theme_advanced_buttons1 = "formatselect,|,bold,italic,underline,|,bullist,numlist,blockquote,|,link,unlink,|,image,media,grappelli_documentstructure";
oTinyMCEConfig.theme_advanced_buttons2 = "";
oTinyMCEConfig.width = '543';
oTinyMCEConfig.plugins = "media";

tinyMCE.init(oTinyMCEConfig);
