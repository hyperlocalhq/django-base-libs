$(document).ready(function(){
    $('textarea').autosize();

    $("textarea[maxlength]").each(function() {
        $(this).charCount({
            allowed: $(this).attr("maxlength")
        });
    });
});

$(window).load(function(){
    $(function() {
        var inputOn = 'c_on',
            radioOn = 'r_on',
            elms=$('input[type="checkbox"], input[type="radio"]');

        function setLabelClass() {
            elms.each(function(i,e) {
                $(e).parent('label')[e.checked?'addClass':'removeClass']($(e).is(':radio')?radioOn:inputOn);
            });
        }

        elms.on('change', setLabelClass);
        setLabelClass();
    });
});