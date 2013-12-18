$(function() {
    function activate(language) {
        $('.multilingual').addClass('hide');
        $('.lang-' + current_language).removeClass('hide');
    }
    var current_language = window.settings.lang;
    activate(current_language);

    var $form_language = $('#form_language');
    $('a',$form_language).click(function() {
        $('.active', $form_language).removeClass('active');
        var $item = $(this).closest('li').addClass('active');
        var language = $item.data('lang');
        activate(language);
        return false;
    });
});