/**
 * Provides functionality and styles for the projects grid.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    function ProjectsGrid($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$blocks = $('.col-xs-12', me.$main);
        me.$elements = $('.wrapper', me.$main);
        me.$uploads = $('.upload-project', me.$main);
        me.$body = $('body');
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $link = $('.content', $element);
            
            if ($('img', $element).length) {
                $link.prepend($('<div class="underlay"></div>'));
            }
            $link.data('$tap-hover', $element);
        });
        
        
        $(window).resize(function() {me.styleIt(200);});
        $(document).ready(function() {me.styleIt();});
        $('img', $main).load(function() {me.styleIt();});
        me.styleIt();
    }
    
    ProjectsGrid.prototype.styleIt = function(delay) {
        
        var me = this.me;
        
        if (delay) {
            setTimeout(function() {me.styleIt();}, delay);
            return;
        }
        
        me.$elements.each(function() {
            
            var $element = $(this);
            var $underlay = $('.underlay', $element);
            var $image = $('img', $element);
            var $text = $('h2', $element);
            
            var image_height = $image.height();
            var text_height = $text.height();
            
            var threshold = (me.$body.hasClass('is-sm')) ? 40 : 55;
            var offset = Math.round((image_height - text_height) / 2);
            if (offset < threshold) offset = threshold;
            
            var padding = (me.$body.hasClass('is-sm')) ? 10 : 20;
            $text.css('top', offset + "px");
            $underlay.height(offset + text_height + padding);
            
            if ($underlay.height() > image_height) $underlay.addClass('has-border');
            else $underlay.removeClass('has-border');
        });
        
        me.$uploads.each(function() {
           
            var $add = $(this);
            var $icon = $('.fawesome', $add);
            var $text = $('h3', $add);
            
            $icon.css('padding-top', '');
            $icon.css('padding-top', Math.round(($add.height() - ($icon.height() + $text.height()) - 20) / 2) + 'px');
            
        });
        
        me.mazeIt();
    }
    
    ProjectsGrid.prototype.mazeIt = function() {
     
        var me = this.me;
        
        var margin = (me.$body.hasClass('is-xs')) ? 10 : 20;
        var row_width = me.$main.width();
        var col_width = $(me.$blocks.get(0)).width();
        var columns = Math.round(row_width / col_width);
        
        var heights = [];
        for (var i=0; i<columns; i++) {
            heights[i] = 0;
        }
        
        me.$blocks.each(function() {
           
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
            
            heights[column] += $block.height() + margin;
            
        });
        
        var max_height = 0;
        for (var i=0, length=heights.length; i<length; i++) {
            if (heights[i] > max_height) max_height = heights[i];   
        }
        me.$main.height(max_height);
    }
    
    $('.projects-grid').each(function() {
        new ProjectsGrid($(this)); 
    });
    
})();