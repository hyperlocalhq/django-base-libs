/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */
 
CKEDITOR.config.forcePasteAsPlainText = false;

 
CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	/*config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];*/

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	//config.removeButtons = 'Underline,Subscript,Superscript';

	// Set the most common block elements.
	config.format_tags = 'p;h2;h4;h5';

	// Simplify the dialog windows.
	//config.removeDialogTabs = 'image:advanced;link:advanced';
	config.removeDialogTabs = 'link:advanced';
    
    config.extraPlugins = 'embed';
    
    config.toolbar = [
        ["Cut", "Copy", "-", "Paste", "PasteText", "PasteFromWord", "-", "Undo", "Redo"], ["Scayt"], ["Styles"], ["Source"], ["Maximize"],
        '/',
        ["Bold", "Italic", "-", "Underline", "Strike", "-", "Subscript", "Superscript", "-", "RemoveFormat"], ["Image", "-", "Embed", "-", "SpecialChar", "-", "HorizontalRule", "-", "Blockquote"], ["Link", "Unlink", "Anchor"]
    ]
};

document.write("<link href='https://fonts.googleapis.com/css?family=Lato:400,400italic,700,700italic,300,300italic,900' rel='stylesheet' type='text/css'>");