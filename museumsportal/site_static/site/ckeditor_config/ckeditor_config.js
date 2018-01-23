/* global CKEDITOR:false */

CKEDITOR.stylesSet.add('museumsportal_styles', [
    {
        name: 'Image w/ description on the left',
        element: 'p',
        attributes: {'class': 'img_left'}
    },
    {
        name: 'Full-width image',
        element: 'p',
        attributes: {'class': 'img_block'}
    }
]);

CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here.
    // For complete reference see:
    // http://docs.ckeditor.com/#!/api/CKEDITOR.config

    config.forcePasteAsPlainText = false;
    // Set the most common block elements.
    config.format_tags = 'p;h2;h3;h4';

    // Simplify the dialog windows.
    //config.removeDialogTabs = 'image:advanced;link:advanced';
    config.removeDialogTabs = 'link:advanced';

    config.extraPlugins = 'oembed,widget';
    config.oembed_maxWidth = '560';
    config.oembed_maxHeight = '315';
    config.oembed_WrapperClass = 'embededContent';
    config.allowedContent = true;
    config.extended_valid_elements  = 'script[language|type|async|src|charset]';


    config.toolbarGroups = [
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
        { name: 'links', groups: [ 'links' ] },
        { name: 'insert', groups: [ 'insert'] },
        { name: 'forms', groups: [ 'forms' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'others', groups: [ 'others' ] },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'colors', groups: [ 'colors' ] },
        { name: 'about', groups: [ 'about' ] }
    ];
    config.removeButtons = 'Underline,Subscript,Superscript,Source,Table,HorizontalRule,SpecialChar,About';

    config.stylesSet = 'museumsportal_styles';
    config.contentsCss = window.settings.STATIC_URL + 'site/css/style.css';
    //config.bodyClass = 'cms-plugin-richtext';
    config.image_prefillDimensions = false;
};
