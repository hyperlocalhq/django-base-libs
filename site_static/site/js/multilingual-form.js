$(window).load(function() {
    function activate(language) {
        $('.multilingual').addClass('hide');
        $('.lang-' + language).removeClass('hide');
    }

    /* show the language-specific fields only for the current language */
    activate(window.settings.lang);

    var $form_language = $('#form_language');

    /* set a badge with an exclamation mark to the language which language-specific fields have errors */
    //$.each(window.settings.frontend_languages, function(lang_code, lang_name) {
    //    if ($('.lang-' + lang_code + ' .has-error').length) {
    //        $('li[data-lang="' + lang_code + '"] a', $form_language).append(' <span class="badge">!</span>');
    //    }
    //});

    /* handle language switching */
    //$('a', $form_language).click(function() {
    //    $('.active', $form_language).removeClass('active');
    //    var $item = $(this).closest('li').addClass('active');
    //    var language = $item.data('lang');
    //    activate(language);
    //    return false;
    //});
    $form_language.change(function() {
        var language = $(this).val();
        activate(language);
    })
});