(function($) {
    $(document).ready(function() {

        function MarkupHelper($main) {

            var me = this;
            me.$main = $main;

            if (me.$main.attr('data-markup-helper-initiate')) return;
            me.$main.attr('data-markup-helper-initiate', '1');

            me.current_markup_type = null;
            me.last_plain_text = null;
            me.last_html_text = null;

            // get the corresponding textarea fields id
            var token = me.$main.attr("id").match(/(.*?)_markup_type/g);
            me.id = RegExp.$1;

            me.toggleMarkup();
            me.$main.change(function() {me.toggleMarkup();});
        }

        MarkupHelper.prototype.toggleMarkup = function() {

            var me = this;

            var markup_type = me.$main.val();
            if (markup_type === 'hw') {
                if (me.current_markup_type === 'pt') me.convertFromPlainText();
                MarkupHelper.setCkEditor(me.id);
            } else {
                MarkupHelper.unsetCkEditor(me.id);
                if (me.current_markup_type !== null) {
                    if (markup_type === 'pt') me.convertToPlainText();
                    else if (me.current_markup_type === 'pt') me.convertFromPlainText();
                }
            }

            me.current_markup_type = markup_type;
        }

        MarkupHelper.prototype.convertToPlainText = function() {

            var me = this;

            var textfield = document.getElementById(me.id);
            var text = textfield.value;

            me.last_html_text = text;

            // adding the appropriate linebreaks to <br/>,<p> and <h?>
            text = text.split("\n").join(''); // get rid of all linebreaks
            text = text.replace(/\<br *\/?\>(?!$)/ig, "<br/>\n");
            text = text.replace(/\<\/p\>(?!$)/ig, "</p>\n\n");
            text = text.replace(/\<\/h[1-6]{1}\>(?!$)/ig, "</h>\n\n");

            // get rid of all tags
            text = text.replace(/\<.+?\>/ig, "");

            text = MarkupHelper.htmlSpecialCharsDecode(text);

            me.last_plain_text = text;
            textfield.value = text;
        }

        MarkupHelper.prototype.convertFromPlainText = function() {

            var me = this;

            var textfield = document.getElementById(me.id);
            var text = textfield.value;

            // if no changes were applied, keep the previous html markup
            if (me.last_html_text !== null && me.last_plain_text == text) {
                textfield.value = me.last_html_text;
                me.last_html_text = null;
                return;
            }

            text = MarkupHelper.htmlSpecialChars(text);

            // converting linebreaks to <br/> and <p>
            var tags = text.split("\n");
            for (var i=0; i<tags.length-1; i++) {
                if (tags[i+1] != "") {
                    tags[i] += "<br/>\n"+tags[i+1];
                    tags.splice(i+1,1);
                    i--
                } else {
                    tags.splice(i+1,1);
                }
            }

            text = '';
            for (var i=0; i<tags.length; i++) {
                text += '<p>'+tags[i]+'</p>';
                if (i != tags.length-1) text += "\n\n";
            }

            me.last_html_text = null;
            textfield.value = text;
        }

        MarkupHelper.setCkEditor = function(sId) {

            if (window.CUSTOM_CKEDITOR_CONFIG) {
                CKEDITOR.replace(sId, {
                    customConfig: window.CUSTOM_CKEDITOR_CONFIG
                });
            } else {
                CKEDITOR.replace(sId);
            }
        }

        MarkupHelper.unsetCkEditor = function(sId) {

            var ck_instance = CKEDITOR.instances[sId];
            if (ck_instance) {
                ck_instance.destroy();
            }
        }

        MarkupHelper.htmlSpecialChars = function(text) {

            var map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;',
                'ö': '&ouml;',
                'ü': '&uuml;',
                'ä': '&auml;',
                'Ö': '&Ouml;',
                'Ü': '&Uuml;',
                'Ä': '&Auml;',
                'ß': '&szlig;'
            };

            return text.replace(/[&<>"']/g, function(m) { return map[m]; });
        }

        MarkupHelper.htmlSpecialCharsDecode = function(string) {

            string = string.toString().replace(/&lt;/g, '<').replace(/&gt;/g, '>');
            string = string.replace(/&#0*39;/g, "'");
            string = string.replace(/&quot;/g, '"');
            string = string.replace(/&ouml;/g, 'ö');
            string = string.replace(/&uuml;/g, 'ü');
            string = string.replace(/&auml;/g, 'ä');
            string = string.replace(/&Ouml;/g, 'Ö');
            string = string.replace(/&Uuml;/g, 'Ü');
            string = string.replace(/&Auml;/g, 'Ä');
            string = string.replace(/&szlig;/g, 'ß');

            // Put this in last place to avoid escape being double-decoded
            string = string.replace(/&amp;/g, '&');

            return string;
        }

        MarkupHelper.initiate = function() {

            $('.markupType').each(function() {
                new MarkupHelper($(this));
            });
        }

        window.setTimeout(MarkupHelper.initiate, 500);
    });

}(django.jQuery));
