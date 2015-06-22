/**
 * Initiates all grids on the page.
 * Add the class "grid-autoload" for each grid which should be automaticly load its next items.
 *
 * An autoload grid has to have an unique id.
 * The pagination for an autoload grid has to be part/inside of the grid.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the grid which contains the $('.grid-item') objects.
     *
     * @param   $main   the jQuery object of the grid wrapper
     */
    function Grid($main) {
        
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.autoload = $main.hasClass('grid-autoload');
        
        me.initGridItems();
        if (me.autoload) me.initAutoscroll();
        
        me.$main.data('list', me);
    }
    
    /**
     * Reinitialises the components of the grid
     * after new content got loaded by a filter.
     * 
     * Gets called internaly.
     */
    Grid.prototype.reinitByFilter = function() {
        
        if (this.me) var me = this.me;
        
        me.initGridItems();
        if (me.autoload) me.initAutoscroll();
    }    
    
    /**
     * Handles work which needs to be done on each grid item.
     *
     */
    Grid.prototype.initGridItems = function() {
        
        if (this.me) var me = this.me;
        
        $('.clearfix', me.$main).remove();
        
        $element = null;
        $('.grid-item', me.$main).each(function(index, element) {
            
            var counter = index+1;
            $element = $(element);
            
            if (counter % 4 == 0) $element.after('<div class="clearfix visible-lg"></div>');
            if (counter % 3 == 0) $element.after('<div class="clearfix visible-md"></div>');
            if (counter % 2 == 0) $element.after('<div class="clearfix visible-sm"></div>');
            
        });
        
        if ($element) $element.after('<div class="clearfix"></div>');
    }
    
    /**
     * Initialises the auto scroll behaviour.
     */
    Grid.prototype.initAutoscroll = function() {
        
        if (this.me) var me = this.me;
        
        var id = me.$main.attr("id");
        var $pagination = $('.pagination', me.$main).removeClass('item').hide();
        
        me.$main.data('jscroll', null);
        if ($pagination.length) {
            me.$main.jscroll({
                loadingHtml: '<small>Loading...</small>',
                padding: 100,
                contentSelector: '#'+id+' .grid-item, #'+id+' .pagination',
                nextSelector: '.next_page:last',
                pagingSelector: '#'+id+' .pagination',
                callback: function() { me.onAutoscrollItems(); }
            });
        }
    }
    
    /**
     * Autoscroll items got loaded.
     */
    Grid.prototype.onAutoscrollItems = function() {
        
        if (this.me) var me = this.me;
        
        $('.pagination').removeClass('item').hide();
        me.initGridItems();
        //lazyload_images();
    }
    
    function init() {
        
        $('.grid').each(function() {
            new Grid($(this));
        });
        
    }
    
    $(document).ready(init);
    
    
    
})();