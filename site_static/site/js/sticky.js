var $stickyDiv = $(".sticky");
var $stickyHeight = 600;
var $padding = 0;
var $topOffset = 150;
var $footerHeight = 83;

function scrollSticky(){
    if($(window).height() >= $stickyHeight) {
        
        var aOffset = $stickyDiv.offset();
        var height = $stickyDiv.height();

        if($(document).height() - $footerHeight - $padding < $(window).scrollTop() + $stickyHeight) {
            var $top = $(document).height() - $stickyHeight - $footerHeight - $padding;
            $stickyDiv.attr('style', 'position:absolute; top:'+$top+'px;');
            // $('#container').css("margin-top",height);

        }else if($(window).scrollTop() + $padding > $topOffset) {
            $stickyDiv.attr('style', 'position:fixed; top:'+$padding+'px;');
            // $('#container').css("margin-top",height);

        }else{
            $stickyDiv.attr('style', 'position:relative;');
            // $('#container').css("margin-top",0);
        }
    }
}

$(window).scroll(function(){
    scrollSticky()
});
