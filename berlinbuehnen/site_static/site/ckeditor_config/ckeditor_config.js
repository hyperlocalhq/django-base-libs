/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

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
};
