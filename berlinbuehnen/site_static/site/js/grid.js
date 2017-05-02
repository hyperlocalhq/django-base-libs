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
        me.$items = $('.grid-item', me.$main);
        me.$featured = $('.grid-item.featured', me.$main)
        me.autoload = $main.hasClass('grid-autoload');
        me.mazery = $main.hasClass('mazery-grid');
        me.is_two_columns = $main.hasClass('grid-two-columns');
        me.is_three_columns = $main.hasClass('grid-three-columns');

        $('.ad_banner', me.$main).removeClass('clearfix');

        me.initGridItems();
        if (me.autoload) me.initAutoscroll();

        me.$main.data('list', me);

        if (me.mazery) {

            if (me.$featured.length) {
                var $first = $(me.$featured.get(0));
                $first.detach();
                me.$main.prepend($first);
            }

            $(window).resize(function() {me.createMazery();});
            $('img', me.$main).load(function() {me.createMazery();});
        }
    }

    /**
     * Reinitialises the components of the grid
     * after new content got loaded by a filter.
     *
     * Gets called internaly.
     */
    Grid.prototype.reinitByFilter = function() {

        if (this.me) var me = this.me;

        me.$items = $('.grid-item', me.$main);
        me.initGridItems();
        if (me.autoload) me.initAutoscroll();
        lazyload_images();

        $('[data-toggle="tooltip"]').tooltip();
        window.tooltipAdjustments();
    }

    Grid.prototype.toggleFavorite = function(event) {

        var $button = $(event.target);

        if ($button.hasClass('favorite')) {
            if ($button.attr('data-content-type-id') && $button.attr('data-object-id')) {
                FavoriteManager.toggle(event.target, $button.attr('data-content-type-id'), $button.attr('data-object-id'), '/');
                return false;
            } else if ($button.attr('data-href')) {
                location.href =  $button.attr('data-href');
                return false;
            }
        }

        return true;
    }

    /**
     * Handles work which needs to be done on each grid item.
     *
     */
    Grid.prototype.initGridItems = function() {

        if (this.me) var me = this.me;

        $('.clearfix', me.$main).remove();

        me.$items.off().click(function(event) {return me.toggleFavorite(event);});

        if (!me.mazery) {

            $element = null;
            var counter_sm = 0;
            var counter_md = 0;
            var counter_lg = 0;

            me.$items.each(function(index, element) {

                $element = $(element);

                if ($element.hasClass('ad-lg')) {
                    counter_lg++;
                } else if ($element.hasClass('ad-md')) {
                    counter_md++;
                } else if ($element.hasClass('ad-sm')) {
                    counter_sm++;
                } else if ($element.hasClass('ad-xs')) {

                } else {
                    counter_sm++;
                    counter_md++;
                    counter_lg++;
                }

                if (me.is_two_columns) {
                    if (counter_lg % 2 == 0) $element.after('<div class="clearfix visible-lg"></div>');
                    if (counter_md % 2 == 0) $element.after('<div class="clearfix visible-md"></div>');
                } else if (me.is_three_columns) {
                    if (counter_lg % 3 == 0) $element.after('<div class="clearfix visible-lg"></div>');
                    if (counter_md % 3 == 0) $element.after('<div class="clearfix visible-md"></div>');
                    if (counter_sm % 2 == 0) $element.after('<div class="clearfix visible-sm"></div>');
                } else {
                    if (counter_lg % 4 == 0) $element.after('<div class="clearfix visible-lg"></div>');
                    if (counter_md % 3 == 0) $element.after('<div class="clearfix visible-md"></div>');
                    if (counter_sm % 2 == 0) $element.after('<div class="clearfix visible-sm"></div>');
                }

            });

            if ($element) $element.after('<div class="clearfix"></div>');

        } else {

            me.createMazery();
        }

        $('[data-toggle="tooltip"]').tooltip();
        window.tooltipAdjustments();
    }

    Grid.prototype.createMazery = function() {

        if (this.me) var me = this.me;

        me.$main.css('height', 'auto');
        me.$items.css('width', '');

        var $body = $('body');

        var cols = 3;
        if ($body.hasClass('is-sm')) cols = 2;
        else if ($body.hasClass('is-xs')) cols = 1;

        if (cols == 1) {

            me.$items.css('position', 'relative').css('top', '0px').css('left', '0px');

        } else {

            var heights = [0,0,0];

            var width = ((me.$main.width() - (20 * cols)) / cols);
            var lefts = [20, width+40, width*2+60];


            me.$featured.each(function() {

                var $item = $(this);

                if ($item.css('display') == "none") return true;

                $item.css('left', lefts[0]+'px');
                $item.css('top', '0px');
                $item.css('position', 'absolute');

                $item.width(width*2 + 20);

                var height = $item.height();
                heights[0] = height;
                heights[1] = height;

                return false;
            });


            var featured_found = false;
            me.$items.each(function() {

                var $item = $(this);
                if ($item.css('display') == "none") return true;

                if (!featured_found && $item.hasClass('featured')) {
                    featured_found = true;
                    return true;
                }

                var col = 0;
                for (var i=1; i<cols; i++) {
                    if (heights[i] < heights[col]) col = i;
                }

                $item.css('left', lefts[col]+'px');
                $item.css('top', heights[col]+'px');
                $item.css('position', 'absolute');
                $item.width(width);

                heights[col] += $item.height();
            });


            var col = 0;
            for (var i=1; i<cols; i++) {
                if (heights[i] > heights[col]) col = i;
            }

            me.$main.height(heights[col]);
        }


        $('[data-toggle="tooltip"]').tooltip();
        window.tooltipAdjustments();
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
        me.$items = $('.grid-item:visible', me.$main);
        me.initGridItems();
        lazyload_images();
    }

    function init() {

        $('.grid').each(function() {
            new Grid($(this));
        });

    }

    $(document).ready(init);



})();
