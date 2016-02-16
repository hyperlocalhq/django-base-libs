/**
 * Provides functionality and styles for the blog grid.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function BlogGrid($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$blocks = $('.col-xs-12', me.$main);
        me.$body = $('body');
        
        me.is_magazine = me.$main.hasClass('magazine');
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt();});
        $('img', $main).load(function() {me.styleIt();});
        me.styleIt();
        me.styleIt(200);
    }
    
    BlogGrid.prototype.styleIt = function(delay) {
        
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        me.mazeIt();
    }
    
    BlogGrid.prototype.mazeIt = function() {
     
        var me = this.me;
        
        var margin = (me.$body.hasClass('is-xs')) ? 10 : 30;
        var row_width = me.$main.width();
        var col_width = (me.$blocks.length > 1) ? $(me.$blocks.get(1)).width() : $(me.$blocks.get(0)).width();
        var columns = Math.round(row_width / col_width);
        
        var heights = [];
        for (var i=0; i<columns; i++) {
            heights[i] = 0;
        }
        
        me.$blocks.each(function(index) {
           
            var $block = $(this);
            
            var column = 0;
            var height = heights[0];
            for (var i=1, length = heights.length; i<length; i++) {
                if (heights[i] < height) {
                    height = heights[i];
                    column = i;
                }
            }
            
            $block.css('top', height + 'px');
            $block.css('left', (column * (col_width + margin)) + 'px');
            
            heights[column] += $block.height();
            
            if (index == 0 && !me.is_magazine) {
                for (var i=1, length = heights.length; i<length; i++) {
                    heights[i] = heights[0];
                }
            }
        });
        
        var max_height = 0;
        for (var i=0, length=heights.length; i<length; i++) {
            if (heights[i] > max_height) max_height = heights[i];   
        }
        me.$main.height(max_height);
    }
    
    $('.blog-grid').each(function() {
        new BlogGrid($(this)); 
    });
    
    
    
})();