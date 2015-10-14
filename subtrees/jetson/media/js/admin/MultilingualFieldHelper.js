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
    var active_language = window.settings.lang;
    var all_languages = [];

    $(document).ready(function() {
        // TODO: cleanup unnecessary data values for simplicity
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
            
            all_languages = langs;
            
            if ($(this).siblings('fieldset.multilingual-set-' + $(this).data('set_hash')).length == 0) return;
            if (!$(this).is('.closed')) {
                $('a.switch-lang.lang-' + $(this).meta('multilingual-language')[0] + ':first', this).trigger('click');
            } else if (!$(this).parent().find('fieldset.multilingual-set-' + $(this).data('set_hash')).not('.closed').length && $(this).meta('multilingual-language')[0] != window.settings.lang) {
                $(this).hide();
            }
        });
    
        $('body').on('click', 'fieldset.multilingual a.switch-lang', function() {
            var lang = $(this).meta('lang')[0];
            $('input[name=' + lang + ']').click();
            return false;
        }).on('activate', 'fieldset.multilingual a.switch-lang', function(event) {
            var $this_fieldset = $(this).parents('fieldset.multilingual:first');
            var set_hash = $this_fieldset.meta('multilingual-set')[0];
            var lang = $(this).meta('lang')[0];
            var $context = $this_fieldset.parent();
            $('fieldset.multilingual-set-' + set_hash, $context).hide();
            var $fieldset_to_show = $('fieldset.multilingual-set-' + set_hash + '.multilingual-language-' + lang, $context);
            $($fieldset_to_show).show();
            if ($fieldset_to_show.is('.grp-closed')) {
                $('.grp-collapse-handler', $fieldset_to_show).first().trigger('click');
                $fieldset_to_show.removeClass("grp-closed").addClass("grp-open").show();
            }
            event.stopPropagation();
            return false;
        });
        
        if (all_languages.length) {
            function activate_language() {
                active_language = $(this).attr('name');
                $('.language_button').removeClass('selected');
                $(this).addClass('selected');
                $('fieldset.multilingual a.switch-lang.lang-' + active_language).trigger("activate");
            }
            var $lang_tabs = $('<div id="page_form_lang_tabs"></div>');
            $(all_languages).each(function() {
                $('<input type="button" class="language_button' + (active_language == this? " selected": "")  + '" name="' + this + '" value="' + window.settings.languages[this] + '" />').appendTo($lang_tabs).click(activate_language);
            });
            $('#grp-content-container').before($lang_tabs).before('<div id="lang_tab_content"><h2 class="header"></h2></div>');
            
            // activate the translatable blocks in default language
            // and hide blocks in other languages
            $('input[name="' + active_language + '"]').click();
        }
    
    });
}(jQuery));