/**
 * Initiates all lists on the page.
 * Add the class "list-autoload" for each list which should be automaticly load its next items.
 *
 * Each item can have a link with the class "list-item-link" inside which will be used on the entire item.
 * Other included links will still work.
 *
 * An autoload list has to have an unique id.
 * The pagination for an autoload list has to be part/inside of the list.
 *
 * @author Daniel Lehmann
 */

(function() {
    
    /**
     * The constructor.
     * Gets the jQuery object of the list which contains the $('.list-item') and $('.list-headline') objects.
     *
     * @param   $main   the jQuery object of the list wrapper
     */
    function List($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.autoload = $main.hasClass('list-autoload');
        me.last_headline = "";
        me.last_width = -1;
        me.small = false;
        me.resize_timer = null;
        
        me.$first_item = $('.list-item', me.$main).first();
        me.$first_body = $('.list-item-body',  me.$first_item);
        me.$first_head = $('.list-item-head',  me.$first_item);
        
        me.initListItems();
        if (me.autoload) me.initAutoscroll();
        $(window).resize(function() {me.onResize();});
    }
    
    /**
     * Handles work which needs to be done on each list item and list headline.
     *
     * @param   new_items   initiate only new autoloaded items
     */
    List.prototype.initListItems = function(new_items) {
        
        if (this.me) var me = this.me;
        
        var $items = $('.list-item', me.$main);
        if (new_items) $items = $items.not('.old-list-item');
        
        $items.each(function() {
            
            var $item = $(this);
            var $link = $('.list-item-link', $item);
            
            $item.data('link', $link);
            $item.click(me.onClick);
        });
        
        var $headlines = $('.list-headline', me.$main);
        if (new_items) $headlines = $headlines.not('.old-list-item').addClass('old-list-item');
        
        $headlines.each(function() {
            
            var $headline = $(this);
            if ($headline.html() != me.last_headline) me.last_headline = $headline.html();
            else $headline.css('display', 'none');
        });
        
        me.onResize(new_items);
    }
    
    /**
     * Sets the width of the list item bodies.
     */
    List.prototype.setListItemsBodyWidth = function() {
        
        if (this.me) var me = this.me;
        
        var $bodies = $('.list-item-body', me.$main);
        
        if (me.small) {
            $bodies.css('width', '');
        } else {
            var width =  me.$first_head.width();
            $bodies.width(me.last_width - width);
        }
    }
    
    /**
     * Callculates the max height of the inner objects of the item body.
     *
     * @param   $item   the list item jQuery object
     */
    List.prototype.setListItemBodyHeight = function($item) {
        
        if (this.me) var me = this.me;
        
        var $body = $('.list-item-body', $item);
        var $h3 = $('h3', $body);
        var $p = $('p', $body);
        
        if (!$p.length) $p = $('.copy', $body);
        
        
        // putting it back to original condition
        $p.each(function() {
            
            $object = $(this);
            var text = $object.data('text');
            if (text) {
                $object.html(text);
                $object.css('display', 'block');
            } else {
                var text = $object.html();
                text = text.replace(/(\<br\>|\<br\/\>)/ig, "\n");
                text = text.replace(/\<\/br\>/ig, "");
                $object.html(text);
                text = $object.text();
                text = text.replace(/\n/g, "<br/>");
                $object.html(text);
                $object.data('text', text);
            }
        });
        
        $h3.css('display', 'block');
        
        if (me.small) return;
        
        
        // checking overflow
        var body_height = $body.height();
        var overflow = false
        
        $h3.each(function() {
            
            var $object = $(this);
            
            if (overflow) {
                $object.css('display', 'none');
            } else {
            
                var top = $object.position().top;
                var height = $object.height();
                
                if (top + height > body_height) {
                    overflow = true;
                    $object.css('display', 'none');
                }
            }
        });
        
        var $last_p = null;
        $p.each(function() {
            
            var $object = $(this);
            
            if (overflow) {
                $object.css('display', 'none');   
            } else {
                
                var top = $object.position().top;
                var height = $object.height();
                
                if (top + height > body_height) {
                    overflow = true;
                    if (top > body_height) {
                        $object.css('display', 'none');
                    } else {
                        $last_p = $object;   
                    }
                }
            }
        });
        
        // shortening the last visible paragraph
        if ($last_p) {
            
            var top = $last_p.position().top;
            var text = "";
            var first_half = $last_p.data('text');
            var second_half = "";
            var split = first_half.length;
            
            while (split) {
                
                $last_p.html(text + first_half);
                
                while (top + $last_p.height() > body_height) {
                    
                    split = Math.floor(split/2);
                    second_half = first_half.substr(split);
                    first_half = first_half.substr(0, split);
                    
                    $last_p.html(text + first_half);
                }
                
                text += first_half;
                first_half = second_half;
                second_half = "";
            }
            
            if (text.length > 3) {
                
                text = text.substr(0, text.length-3);
                while (text.length && text.charAt(text.length-1) != " ") {
                    text = text.substr(0, text.length-1);
                }
                
                if (text.length) $last_p.html(text + "...");
                else $last_p.css('display', 'none');
                
            } else {
                $last_p.css('display', 'none');   
            }
        }
    }
    
    /**
     * Initialises the auto scroll behaviour.
     */
    List.prototype.initAutoscroll = function() {
        
        if (this.me) var me = this.me;
        
        var id = me.$main.attr("id");
        var $pagination = $('.pagination', me.$main).removeClass('item').hide();
        
        me.$main.data('jscroll', null);
        if ($pagination.length) {
            me.$main.jscroll({
                loadingHtml: '<small>Loading...</small>',
                padding: 100,
                contentSelector: '#'+id+' .list-headline, #'+id+' .list-item, #'+id+' .pagination',
                nextSelector: '.next_page:last',
                pagingSelector: '#'+id+' .pagination',
                callback: function() { me.onAutoscrollItems(); }
            });
        }
    }
    
    /**
     * Autoscroll items got loaded.
     */
    List.prototype.onAutoscrollItems = function() {
        
        if (this.me) var me = this.me;
        
        $('.pagination').removeClass('item').hide();
        me.initListItems(true);
        lazyload_images();
    }
    
    /**
     * An item got clicked.
     */
    List.prototype.onClick = function(event) {
        
        var $target =  $(event.target);
        if ($target.is('a')) return true;
        
        event.stopPropagation();
        
        var $this = $(this);
        var $link = $this.data('link');
        
        if ($link) location.href = $link.attr('href');
    }
    
    /**
     * The window got resized.
     *
     * @param   new_items   check only new autoloaded items
     */
    List.prototype.onResize = function(new_items) {
        
        if (this.me) var me = this.me;
        
        if (me.resize_timer) {
            window.clearTimeout(me.resize_timer);   
            me.resize_timer = null;
        }
        
        
        var doResize = function () {
            
            me.resize_timer = null;
            
            var old_small = me.small;
            var current_body_width = me.$first_body.css('width');
            
            // has to be smaller then the smallest value for measuring
            me.$first_body.css('width', '300px');
            if (0 == me.$first_body.position().left) {
                me.$main.addClass("small");   
                me.small = true;
            } else {
                me.$main.removeClass("small");   
                me.small = false;
            }
            
            
            var new_width = me.$main.width();
            
            
            if (new_width != me.last_width || new_items || old_small != me.small) {
                
                me.last_width = new_width;
            
                me.setListItemsBodyWidth();
                
                var $items = $('.list-item', me.$main);
                if (new_items) {
                    if (old_small == me.small) $items = $items.not('.old-list-item').addClass('old-list-item');
                    else $items.not('.old-list-item').addClass('old-list-item');
                }
                
                $items.each(function() {
                    me.setListItemBodyHeight($(this)); 
                });
                
            } else {
            
                me.$first_body.css('width', current_body_width); 
            }
        }
        
        me.resize_timer = window.setTimeout(function() {doResize();}, 25);
    }
    
    
    function init() {
        
        $('.list').each(function() {
            new List($(this));
        });
        
    }
    
    $(document).ready(init);
    
})();