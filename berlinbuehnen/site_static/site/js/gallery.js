/**
 * Initiates the media gallery.
 * The Videos have to be always the first galery items!!!
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the gallery which contains the $('.gallery-item') objects.
     *
     * @param   $main   the jQuery object of the gallery wrapper
     */
    function Gallery($main) {
        
        var me = this;
        this.me = me;
        
        me.margin_head = 60;
        me.margin_vertical = 20;
        
        me.$main = $main;
        me.$items = $('.gallery-item', $main);   
        me.player = new Array();
        
        
        
        var $gallery_head = $('.gallery-head', $main);
        me.margin_head += $gallery_head.height();
        
        me.$columns = $('<div class="col-xs-12 col-sm-6 col-md-4 clearfix" style="height:1px;"/>');
        $gallery_head.after(me.$columns);
        
        $('.video', $main).each(function() {
            
            var $this = $(this);
            var $embed = $($this.children()[0]);
            var $player = $('<div/>');
            
            $player.data("width", $embed.width());
            $player.data("height", $embed.height());
            $this.data("player", $player);
            
            $player.append($embed);
            $embed.css("width", "100%");
            $embed.css("height", "100%");
            $this.append($player);
            
            me.player.push($player);
        });
        
        $('.image', $main).each(function() {
            
            var $this = $(this);
            var $image = $($this.children()[0]);
            $image.load(function() {me.onImageLoaded();});
            
        });
        
        me.arrange();
        $(window).resize(function() {me.arrange();});
    }
    
    /**
     * Arranges the galery items in the grid.
     */
    Gallery.prototype.arrange = function() {
        
        if (this.me) var me = this.me;
        
        me.$items.css('display', 'none');
        var width = me.$main.width();
        var columns_width = me.$columns.width();
        
        var colums = 0;
        
        if (columns_width > width * 0.8) colums = 1;
        else if (columns_width > width * 0.43) colums = 2;
        else colums = 3;
        
        
        me.$items.css('display', 'block');
        me.setVideosHeight();
        
        var heights = new Array(me.margin_head, me.margin_head, me.margin_head);
        me.$items.each(function() {
            
            var $item = $(this);
            var height = $item.height() + me.margin_vertical;
            
            if ($item.hasClass("video")) {
                
                $item.css('top', heights[0]+'px');
                heights[0] += height;
                if (colums != 1) heights[1] += height;
                
            } else {
                
                column = 0;
                min_height = heights[0];
                for (i=1; i<colums; i++) {
                    if (min_height > heights[i]) {
                        min_height = heights[i];
                        column = i;
                    }
                }
                
                $item.css('top', heights[column]+'px');
                heights[column] += height;
                
                var left = 100/colums * column;
                $item.css('left', left+'%');
            }
            
        });
        
        
        var max_height = heights[0];
        for (i=1; i<colums; i++) {
            if (max_height < heights[i]) max_height = heights[i];
        }
        
        me.$main.height(max_height);
    }
    
    /**
     * Recalculates the height of the video items.
     */
    Gallery.prototype.setVideosHeight = function() {
        
        if (this.me) var me = this.me;
        
        for (var i=0; i<me.player.length; i++) {
            var $player = me.player[i];
            $player.css("width", "100%");
            width = $player.width();
            height = width * $player.data("height") / $player.data("width");
            $player.width(width);
            $player.height(height);
        }
    }
    
    /**
     * An image got loaded.
     * Rearranges the images after all got loaded.
     */
    Gallery.prototype.onImageLoaded = function() {
        
        if (this.me) var me = this.me;
        me.arrange();
    }
    
    
    function init() {
        
        $('.gallery').each(function() {
            new Gallery($(this));
        });
        
    }
    
    $(document).ready(init);
    
    
})();