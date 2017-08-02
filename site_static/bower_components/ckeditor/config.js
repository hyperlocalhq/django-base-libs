/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */
 
CKEDITOR.config.forcePasteAsPlainText = false;

 
CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here.
    // For complete reference see:
    // http://docs.ckeditor.com/#!/api/CKEDITOR.config

    // Set the most common block elements.
    config.format_tags = 'p;h2;h4;h5';

    // Simplify the dialog windows.
    //config.removeDialogTabs = 'image:advanced;link:advanced';
    config.removeDialogTabs = 'link:advanced';
    
    config.extraPlugins = 'oembed,widget';
    config.oembed_maxWidth = '560';
    config.oembed_maxHeight = '315';
    config.oembed_WrapperClass = 'embededContent';
    config.allowedContent = true;

    config.toolbar = [
        ['Cut', 'Copy', '-', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'], ['Scayt'], ['Styles'], ['Source'], ['Maximize'],
        '/',
        ['Bold', 'Italic', '-', 'Underline', 'Strike', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'], ['Image', '-', 'oembed', '-', 'SpecialChar', '-', 'HorizontalRule', '-', 'Blockquote'], ['Link', 'Unlink', 'Anchor']
    ];
};

if (window.jQuery) {
    jQuery('head').append('<link href="https://fonts.googleapis.com/css?family=Lato:400,400italic,700,700italic,300,300italic,900" rel="stylesheet" type="text/css">');
}
