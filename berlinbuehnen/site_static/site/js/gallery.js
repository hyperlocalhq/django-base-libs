/**
 * Initiates all media galleries.
 * The Videos have to be the first gallery items in each gallery!!!
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
        me.images = new Array();
        
        me.columns = 0;
        me.image_loaded = false;
        me.$active_image = null;
        me.active_image_index = 0;
        me.last_width = -1;
        
        
        
        var $gallery_head = $('.gallery-head', $main);
        me.margin_head += $gallery_head.height();
        
        me.$columns = $('<div class="col-xs-12 col-sm-6 col-md-4 clearfix" style="height:1px;"/>');
        $gallery_head.after(me.$columns);
        
        $('.video', $main).each(function() {
            
            var $this = $(this);
            
            var $embed = $($this.children()[0]);
            var $player = $('<div/>');
            
            // checking for edge-cdn.net player and setting width and height
            var $script = $('script', $this);
            if ($script.length && $embed.height() == 0) {
                var src = $script.attr('src').toLowerCase();
                if (src.indexOf('edge-cdn.net') >= 0) {
                    var width = src.split('width=', 2);
                    width = width[1].split('&', 2);
                    var height= src.split('height=', 2);
                    height = height[1].split('&', 2);
                    $embed.width(width[0]);
                    $embed.height(height[0]);
                }
            }
            
            $player.data("width", $embed.width());
            $player.data("height", $embed.height());
            $this.data("player", $player);
            
            $player.append($embed);
            $embed.css("width", "100%");
            $embed.css("height", "100%");
            $this.append($player);
            
            me.player.push($player);
        });
        
        $('.image', $main).each(function(index, element) {
            
            var $this = $(this);
            var $image = $('.gallery-image', $this);
            var $text = $('.gallery-image-text', $this);
            
            $text.detach();
            
            $image.data("index", index);
            $image.data("text", $text);
            me.images.push($image);
            
            $image.click(function() {me.openLayer($(this));});
            $image.load(function() {me.onImageLoaded();});
            
        });
        
        var $layer = $('#gallery-layer');
        if ($layer.length) {
            me.$layer = $layer;
        } else {
            me.$layer = $('<div id="gallery-layer"><div id="gallery-layer-close"></div><div id="gallery-layer-prev" class="fawesome back"></div><div id="gallery-layer-next" class="fawesome more"></div></div>');
            $('body').append(me.$layer);
            $('#gallery-layer-close').click(function() {me.closeLayer();});
        }
        
        me.$next = $('#gallery-layer-next');
        me.$prev = $('#gallery-layer-prev');
        
        me.onResize();
        $(window).resize(function() {me.onResize();});
    }
    
    /**
     * Arranges the galery items in the grid.
     */
    Gallery.prototype.arrange = function() {
        
        if (this.me) var me = this.me;
        
        me.$items.css('display', 'none');
        var width = me.$main.width();
        var columns_width = me.$columns.width();
        
        var columns = 0;
        
        if (columns_width > width * 0.8) columns = 1;
        else if (columns_width > width * 0.43) columns = 2;
        else columns = 3;
        
        me.columns = columns;
        
        
        me.$items.css('display', 'block');
        me.setVideosHeight();
        
        var heights = new Array(me.margin_head, me.margin_head, me.margin_head);
        me.$items.each(function() {
            
            var $item = $(this);
            var height = $item.height() + me.margin_vertical;
            
            if ($item.hasClass("video")) {
                
                $item.css('top', heights[0]+'px');
                heights[0] += height;
                if (columns != 1) heights[1] += height;
                
            } else {
                
                column = 0;
                min_height = heights[0];
                for (i=1; i<columns; i++) {
                    if (min_height > heights[i]) {
                        min_height = heights[i];
                        column = i;
                    }
                }
                
                $item.css('top', heights[column]+'px');
                heights[column] += height;
                
                var left = 100/columns * column;
                $item.css('left', left+'%');
            }
            
        });
        
        
        var max_height = heights[0];
        for (i=1; i<columns; i++) {
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
    
    /**
     * Opens the layer.
     *
     * @param   $image   the jQuery image object which got clicked
     */
    Gallery.prototype.openLayer = function($image) {
        
        if (this.me) var me = this.me;
        
        me.resizedLayer();        
        
        me.$prev.off();
        me.$next.off();
        
        me.$layer.off('swiperight');
        me.$layer.off('swipeleft');
        
        if (me.images.length == 1) {
            me.$prev.css('display', 'none');
            me.$next.css('display', 'none');
        } else {
            me.$prev.css('display', 'block');
            me.$next.css('display', 'block');
            me.$prev.click(function() {me.prevImage();});
            me.$next.click(function() {me.nextImage();});
            me.$layer.on('swiperight', function() {me.prevImage();});
            me.$layer.on('swipeleft', function() {me.nextImage();});
        }
        
        $('body').css('overflow', 'hidden');
        me.$layer.css('display', 'block');
        
        me.showImage($image);
        
    }
    
    /**
     * Closes the layer.
     */
    Gallery.prototype.closeLayer = function() {
        
        if (this.me) var me = this.me;
        
        me.$layer.css('display', 'none');
        $('body').css('overflow', 'auto');
           
        me.$active_image.remove();
        me.$active_image = null;
    }
    
    /**
     * Shows the next image.
     */
    Gallery.prototype.nextImage = function() {
        
        if (this.me) var me = this.me;
        
        me.active_image_index++;
        if (me.active_image_index >= me.images.length) me.active_image_index = 0;
        
        me.showImage(me.images[me.active_image_index]);
    }
    
    /**
     * Shows the previews image.
     */
    Gallery.prototype.prevImage  = function() {
        
        if (this.me) var me = this.me;
        
        me.active_image_index--;
        if (me.active_image_index < 0) me.active_image_index = me.images.length-1;
        
        me.showImage(me.images[me.active_image_index]);
    }
    
    /**
     * Shows the image.
     *
     * @param   $image   the jQuery image object to be shown
     */
    Gallery.prototype.showImage = function($image) {
        
        if (this.me) var me = this.me;
        
        if (me.$active_image) {
            /*me.$active_image.animate({opacity: 0}, 400, function() {
                this.remove();   
            });*/
            me.$active_image.remove();
        }
        
        me.active_image_index = $image.data("index");
        
        var new_image = new Image();
        var $new_image = $(new_image);
        me.image_loaded = false;
        $new_image.load(function() {me.image_loaded = true; me.resizedLayer();});
        
        var $image_wrapper = $('<div class="gallery-image-wrapper"/>');
        $image_wrapper.prepend($new_image);
        
        var $image_text = $image.data("text");
        $image_wrapper.append($image_text);
        
        me.$layer.prepend($image_wrapper);
        
        me.$active_image = $image_wrapper;
        new_image.src = $image.attr("data-image-big");
        me.resizedLayer();
    }
    
    /**
     * Adjusts the layer on resize.
     */
    Gallery.prototype.resizedLayer = function() {
        
        if (this.me) var me = this.me;
        
        me.$layer.removeClass("medium").removeClass("small");
        if (me.columns == 2) me.$layer.addClass("medium");
        else if (me.columns == 1) me.$layer.addClass("small");
        
        if (me.$active_image && me.image_loaded) {
            
            var min_top_padding = (me.columns == 1) ? 0 : 20;
            var min_bottom_padding = 25;
            
            var $image = $('img', me.$active_image);
            var $text = $('.gallery-image-text', me.$active_image);
        
            $image.css("padding-top", min_top_padding+"px");
            $image.css("padding-bottom", min_bottom_padding+"px");
            $text.width($image.width());
            
            var text_height = $text.height();
            $image.css("padding-bottom", (text_height + min_bottom_padding)+"px");
            var image_height = $image.height();
            
            var top_padding = Math.round((me.$active_image.height() - (image_height + text_height + min_top_padding + min_bottom_padding)) / 2) + min_top_padding;
            $image.css("padding-top", top_padding+"px");
            
            $text.width($image.width());
            $text.css("top", (image_height + top_padding) + "px");
            $text.css("left", $image.position().left + "px");
            
            me.$active_image.animate({opacity: 1}, 400);
        }
    }
    
    /**
     * The window got resized.
     */
    Gallery.prototype.onResize = function() {
        
        if (this.me) var me = this.me;
        
        var new_width = me.$main.width();
        
        if (new_width != me.last_width) {
            me.last_width = new_width;
            me.arrange();
        }
        
        if (me.$layer.css('display') == "block") me.resizedLayer();
    }
    
    function init() {
        
        $('.gallery').each(function() {
            new Gallery($(this));
        });
        
    }
    
    $(document).ready(init);
    
    
})();