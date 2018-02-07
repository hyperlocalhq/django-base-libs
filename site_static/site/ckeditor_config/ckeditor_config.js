/* global CKEDITOR:false */

CKEDITOR.stylesSet.add('ccb_styles', [
    {name: 'Caption (Heading)', element: 'h5', attributes: { 'class': 'caption' }},
    {name: 'Interview title (Heading)', element: 'h4', attributes: {'class': 'interview-title'}},
    {name: 'Intro (Paragraph)', element: 'p', attributes: {'class': 'intro'}},
    {name: 'Interview (Paragraph)', element: 'p', attributes: { 'class': 'interview'}},
    {name: 'Interviewee in title', element: 'strong', attributes: {'class': 'title-interviewee'}},
    {name: 'Interviewee in paragraph', element: 'span', attributes: { 'class': 'interviewee'}}
]);

CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here.
    // For complete reference see:
    // http://docs.ckeditor.com/#!/api/CKEDITOR.config

    config.forcePasteAsPlainText = false;
    // Set the most common block elements.
    config.format_tags = 'p;h2;h3;h4;h5';

    // Simplify the dialog windows.
    //config.removeDialogTabs = 'image:advanced;link:advanced';
    config.removeDialogTabs = 'link:advanced';

    config.extraPlugins = 'oembed,widget';
    config.oembed_maxWidth = '560';
    config.oembed_maxHeight = '315';
    config.oembed_WrapperClass = 'embededContent';
    config.allowedContent = true;
    config.entities = true;

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
    config.removeButtons = 'Underline,Subscript,Superscript,Source,Table,SpecialChar,About';

    config.stylesSet = 'ccb_styles';
    config.contentsCss = window.settings.STATIC_URL + 'site/css/ckeditor.css';
    config.bodyClass = 'cms-plugin-richtext article';
    config.image_prefillDimensions = false;
};
