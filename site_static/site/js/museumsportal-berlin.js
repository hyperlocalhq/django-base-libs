$(window).load(function() {
    $('#gallery .cancel').click(function(e){
        $('body').toggleClass('gallery');
    });

    $('.images li').click(function(e){
        $('body').toggleClass('gallery');
    });

    $('#gallery .info').click(function(e){
        $('#gallery').toggleClass('info');
    });
});

var slider = new Swipe(document.getElementById('slider'));

// $(function(){
//   var liWidths = [];
//   $('ul.fillwidth').fillwidth({ liWidths: liWidths });
// });

$(window).load(function() {
    $('.images').isotope({
        itemSelector : '.item',
        layoutMode : 'masonry',
        masonry: {
            columnWidth: 340
        }
    });
});