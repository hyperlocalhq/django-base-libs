/**
 * Attaches objects to the top of the browser window.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object which should be attached to the top of the browser window.
     * Elements with the class "affix-offset-visible" are only visible if the scroll offset 
     * reached the "data-offset-top" value of the jQuery object.
     *
     * @param   $main   the jQuery object of the gallery wrapper
     */
    function Affix($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$visibles = $('.affix-offset-visible', me.$main);
        me.offset = $main.data('offset-top');
        if (!me.offset) me.offset = 0;
        
        me.$visibles.css('visibility', 'hidden');
        
        me.setOffset();
        $(window).scroll(function() {me.setOffset();});
        $(window).resize(function() {me.setOffset();});
    }
    
    Affix.prototype.setOffset = function() {
        
        if (this.me) var me = this.me;
        
        if ($('body').hasClass('is-xs')) {
            me.$visibles.css('visibility', 'visible');
            me.$main.css('top', '0px');
            return;
        }
        
        var scroll = $(window).scrollTop();
        
        if (scroll >= me.offset) {
            me.$visibles.css('visibility', 'visible');
            var top = me.offset;
        } else {
            me.$visibles.css('visibility', 'hidden');
            var top = scroll;
        }
        
        me.$main.css('top', '-'+top+'px');
    }
    
    
    function init() {
        
        $('.affix-rebuild').each(function() {
            new Affix($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();