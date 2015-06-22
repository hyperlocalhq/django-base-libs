/**
 * Handles the multiple collapsing of top widgets into one button.
 *
 * @author Daniel Lehmann
 */

$(document).ready(function() {
    
    $('.top-widgets').each(function() {
        
        var $widgets = $(this);
        var collapsed = 0;
        var collapsible = [];
        
        $('.top-widget-button', $widgets).each(function() {
            var target = $(this).data("target");
            for (var i=0, length=collapsible.length; i<length; i++) {
                if (collapsible[i] == target) break;    
            }
            if (i == length) collapsible.push(target);
        });
        
        for (var i=0, length=collapsible.length; i<length; i++) {
            $(collapsible[i]).on('show.bs.collapse', function(event) { onExpanding($(event.target)); });
            $(collapsible[i]).on('hide.bs.collapse', function(event) { onCollapsing($(event.target)); });
        }
        
        var onExpanding = function(me) {
            
            for (var i=0, length=collapsible.length; i<length; i++) {
                if (collapsible[i] == "#"+me.attr("id")) break;
            }
            if (i == length) return;
            
            collapsed--;
            if (collapsed < 0) collapsed = 0;
            $widgets.css('display', 'block');
        }
        
        var onCollapsing = function(me) {
            
            for (var i=0, length=collapsible.length; i<length; i++) {
                if (collapsible[i] == "#"+me.attr("id")) break;
            }
            if (i == length) return;
            
            collapsed++;
            if (collapsed >= collapsible.length) {
                $widgets.animate({height:1}, 200, "linear", function() {
                    $widgets.css('display', 'none');
                    $widgets.css('height', 'auto');
                });
                collapsed = 0;
            }
        }
    });
    
});