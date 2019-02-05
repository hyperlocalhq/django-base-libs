/**
 * Handles styling of the magazine grid.
 * @author Daniel Lehmann
 */

(function() {
    
    function MagazineGrid($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$blocks = $('div', $main);
        
        me.setClearfix();
    }
    
    MagazineGrid.prototype.setClearfix = function() {
        
        var me = this;
        
        me.$blocks.each(function(index) {
            
            if (index == 0) return true;
            index++;
            
            var $block = $(this);
            
            if (index % 2 == 0) {
                $block.after('<div class="clearfix visible-sm"></div>');   
            }
            
            if (index % 3 == 0) {
                $block.after('<div class="clearfix visible-md visible-lg"></div>');   
            }
            
        });        
    }
    
    $('.magazine-grid').each(function() {
        new MagazineGrid($(this)); 
    });
    
})();