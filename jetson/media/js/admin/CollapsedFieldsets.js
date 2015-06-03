$j = jQuery;

$j(document).ready(function(){
    
    /// FIELDSETS
    $j('fieldset[class*="collapse-closed"]').each(function() {
        $j(this).addClass("collapsed");
        $j(this).find('h2:first').addClass("collapse-toggle");
    });
    $j('fieldset[class*="collapse-open"]').each(function() {
        $j(this).find('h2:first').addClass("collapse-toggle");
    });
    $j('h2.collapse-toggle').bind("click", function(e){
        $j(this).parent().toggleClass('collapsed');
        $j(this).parent().toggleClass('collapse-closed');
        $j(this).parent().toggleClass('collapse-open');
    });
    /// OPEN FIELDSETS WITH ERRORS
    $j('fieldset[class*="collapse-closed"]').children('div[class*="errors"]').each(function(i) {
        $j(this).parent().toggleClass("collapsed");
        $j(this).parent().toggleClass('collapse-closed');
        $j(this).parent().toggleClass('collapse-open');
    });
    
});
