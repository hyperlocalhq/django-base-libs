/**
 * editor_plugin_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

(function() {
	tinymce.create('tinymce.plugins.FilebrowserImagePlugin', {
		init : function(ed, url) {
			// Register commands
			ed.addCommand('mceFilebrowserImage', function() {
				// Internal image object like a flash placeholder
				if (ed.dom.getAttrib(ed.selection.getNode(), 'class', '').indexOf('mceItem') != -1)
					return;

				ed.windowManager.open({
					file : url + '/image.htm',
					width : 480 + parseInt(ed.getLang('fbimage.delta_width', 0)),
					height : 355 + parseInt(ed.getLang('fbimage.delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			// Register buttons
			ed.addButton('image', {
				title : 'advimage.image_desc',
				cmd : 'mceFilebrowserImage'
			});
		},

		getInfo : function() {
			return {
				longname : 'Filebrowser image',
				author : 'Aidas Bendoraitis',
				authorurl : 'https://github.com/archatas',
				//infourl : '',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('fbimage', tinymce.plugins.FilebrowserImagePlugin);
})();