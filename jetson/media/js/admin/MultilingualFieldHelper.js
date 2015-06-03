(function($) {
    $.fn.meta = function(m) {
        var c = jQuery(this).attr('class');
        if (!c) return false;
        var classes = c.split(" ");
        var meta = [];
        for (var i=0; i<classes.length; i++) {
            if (classes[i].substring(0, m.length) == m) {
                meta[meta.length] = classes[i].substring(m.length + 1, classes[i].length);
            }
        }
        return meta;
    }
    $(document).ready(function() {
        $('fieldset.multilingual').each(function() {
            var set_hash = $(this).meta('multilingual-set')[0];
            $(this).data('set_hash', set_hash);
            $(this).data('expanded', !$(this).is('.closed'));
            var langs = []
            var f = this;
            $('fieldset.multilingual-set-' + set_hash).each(function() {
                if ($(f).parent().get(0) == $(this).parent().get(0)) langs.push($(this).meta('multilingual-language')[0]);
            });
            if (langs.length < 2) return;
            
            var $langLinks = $('<ul class="multilingual-langs"></ul>');
            for (var i in langs) {
                 var $link = $('<a href="#" class="switch-lang lang-' + langs[i] + '" title="' + window.settings.languages[langs[i]] + '"><span>' + langs[i] + '</span></a> ');
                 $link.data('lang',langs[i]);
                 $link.data('set_hash',set_hash);
                 $link.data('fieldset', this);
                 $langLinks.append($link.wrap("<li>").parent());
            }
            var $header = $('h2,h4', this).first();
            $header.text($header.text().replace(/ \([^\)]+\)$/,''));
            $header.after($langLinks);
        });
        $('fieldset.multilingual a.switch-lang').click(function(event) {
            // .css('cssText', ...) – hack needed because grappelli css uses !important in styles.
            var context = $(this).parents('fieldset.multilingual:first').parent();
            $('fieldset.multilingual-set-' + $(this).data('set_hash'), context).hide();
            var fieldset_to_show = $('fieldset.multilingual-set-' + $(this).data('set_hash') + '.multilingual-language-' + $(this).data('lang'), context);
            $(fieldset_to_show).show();
            if ($(fieldset_to_show).is('.closed')) {
                $('h2,h4', fieldset_to_show).first().trigger('click');
            }
            event.stopPropagation();
            return false;
        });
        $('fieldset.multilingual').each(function() {
            if ($(this).siblings('fieldset.multilingual-set-' + $(this).data('set_hash')).length == 0) return;
            if (!$(this).is('.closed')) {
                $('a.switch-lang.lang-' + $(this).meta('multilingual-language')[0] + ':first', this).trigger('click');
            } else if (!$(this).parent().find('fieldset.multilingual-set-' + $(this).data('set_hash')).not('.closed').length && $(this).meta('multilingual-language')[0] != window.settings.lang) {
                $(this).hide();
            }
        });
    
    });
}(jQuery));