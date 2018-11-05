/**
 * Base functionality of the page.
 *
 * @author Daniel Lehmann
 */

$(document).ready(function() {
    
    var current_width_sniffer = 'is-nothing';
    var widthSniffer = function() {
       
        var new_width_sniffer = false;
        $('.width-sniffer').each(function() {
            
            var $this = $(this);
            if ($this.css('display') == 'block') {
                
                if ($this.hasClass('visible-xs')) {
                    new_width_sniffer = 'is-xs';
                } else if ($this.hasClass('visible-sm')) {
                    new_width_sniffer = 'is-sm';
                } else if ($this.hasClass('visible-md')) {
                    new_width_sniffer = 'is-md';
                } else if ($this.hasClass('visible-lg')) {
                    new_width_sniffer = 'is-lg';
                }
                
                return false;
            }
        }); 
        
        if (new_width_sniffer && new_width_sniffer != current_width_sniffer) {
            var $body = $('body').removeClass(current_width_sniffer);
            current_width_sniffer = new_width_sniffer; 
            $body.addClass(new_width_sniffer);
        }        
    }
    $(window).resize(widthSniffer);
    widthSniffer();
    
});