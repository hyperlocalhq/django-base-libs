/**
 * Handles the google map functionality.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function Map() {
        
        var me = this;
        this.me = me;
        
        me.$height = $('.gmap-height');
        me.$sidebar = $('#map-sidebar-wrapper');
        me.$buttons = $('#map-buttons-overflow');
        me.$body = $('body');
        me.$window = $(window);
        
        me.onResize();
        $(window).resize(function() {me.onResize();});
    }
    
    Map.prototype.calculateHeight = function() {
     
        var me = this.me;
        
        var window_height = me.$window.height();
        var header_height = $('.navbar-wrapper').height();
        
        var margin = 40;
        if (me.$body.hasClass('is-sm')) {
            margin = -20;   
        } else if (me.$body.hasClass('is-xs')) {
            margin = 10;   
        }
        
        me.$height.height(window_height - header_height - margin);
        
        
        var window_width = me.$window.width() + 30;
        if (window_width > 430) window_width = 410;
        
        me.$sidebar.css('max-width', window_width + "px");
        
        var buttons_margin = (410 - window_width + 52) * (-1);
        me.$buttons.css('left', buttons_margin + "px");
    }
    
    Map.prototype.onResize = function() {
     
        var me = this.me;
        
        me.calculateHeight();
        
    }
    
    function init() {
        
        new Map();
        
    }
    
    $(document).ready(init);
    
})();