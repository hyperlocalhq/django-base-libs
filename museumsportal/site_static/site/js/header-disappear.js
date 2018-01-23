$(function(){
    var lastScrollTop = 0, delta = 50;

    $(window).scroll(function(event){
       var st = $(this).scrollTop(), threshold = 271;
       if (st > threshold) {

         if(Math.abs(lastScrollTop - st) <= delta)
            return;

         if (st > lastScrollTop){
             // Scroll Down
              $(".navbar-wrapper").delay(10).queue(function() {
                  $(this).removeClass("nav-visible").addClass("nav-hidden");
                  $(this).dequeue();
              });

         } else {
            // Scroll Up
              $('.navbar-wrapper').delay(10).queue(function() {
                  $(this).removeClass("nav-hidden").addClass("nav-visible");
                  $(this).dequeue();
              });
         }
       lastScrollTop = st;
       }
    });
});