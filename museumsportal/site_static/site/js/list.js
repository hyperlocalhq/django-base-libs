/* jshint unused:false, eqnull:false, sub:true */
/* global $:false */
/* global lazyload_images:false */
/* global console:false */

(function($, undefined) {
    var activation_event = "click";
    if (navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|IEMobile|Opera Mini|webOS/i)) {
        activation_event = "touchstart";
    }
    var $current_item;
    var $item_on_next_row;

    function layout_description() {
        var $container = $('#container').css('position', 'relative');
        if (!$current_item || !$current_item.length) {
            return;
        }
        $current_item.addClass('item-preview'); // open the new preview

        if ($item_on_next_row) {
            $item_on_next_row.removeClass('first_item_on_next_row');
        }

        $item_on_next_row = $current_item.nextAll('.item:visible:first');
        while ($item_on_next_row.length && $current_item.position().top >= $item_on_next_row.position().top) {
            $item_on_next_row = $item_on_next_row.nextAll('.item:visible:first');
        }
        if ($item_on_next_row.length) {
            $item_on_next_row.addClass('first_item_on_next_row');
        }

        var $description = $current_item.find(".description");

        // define position for the description
        var left = $current_item.position().left;
        var width = $container.width();
        var offset_left = parseInt($container.css('margin-left'), 10);
        var offset_right = parseInt($container.css('margin-right'), 10);

        $description.css({
            left: -left - 10,
            width: width + offset_left + offset_right
        });
    }

    function close_description() {
        if ($current_item) {
            if ($current_item.hasClass('item-preview')) { // if clicked again, close the preview
                $current_item.removeClass('item-preview');
                if ($item_on_next_row) {
                    $item_on_next_row.removeClass('first_item_on_next_row');
                    $item_on_next_row = null;
                }
                $current_item = null;
                lazyload_images();
                return false;
            }
        }
    }

    function reinit_infinite_scroll() {
        if (!navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|IEMobile|Opera Mini|webOS/i)) {
            var $pagination = $('.pagination').removeClass('item').hide();
            var $container = $('#container').data('jscroll', null);
            if ($pagination.length) {
                $container.jscroll({
                    loadingHtml: '<small>Loading...</small>',
                    padding: 100,
                    contentSelector: '#container .grid,#container .list',
                    nextSelector: '.next_page:last',
                    pagingSelector: '.pagination',
                    callback: function() {
                        $('.pagination').removeClass('item').hide();
                        lazyload_images();
                    }
                });
            }
        }
    }

    $(function() {

        reinit_infinite_scroll();

        $('#map-list-link').click(function() {
            location.href = $(this).attr('href') + location.hash;
            return false;
        });

        $('#container').on('contextmenu taphold', '.item>a', function(e) {
            e.preventDefault();

            var $clicked_item = $(this).closest('.item');

            // if the same item clicked, close it
            if ($clicked_item.hasClass('item-preview')) {
                close_description();
                return false;
            // if other item is opened, close it
            } else if ($current_item) {
                close_description();
            }

            // get new current item
            $current_item = $clicked_item;

            var $description = $current_item.find(".description");

            // if description doesn't exist yet, load it
            if (!$.trim($description.text())) {
                $description.load($current_item.data('description-src'), function() {
                    layout_description();
                    if (window.init_share) {
                        window.init_share();
                    }
                });
            // if description already exists, just re-layout it
            } else {
                layout_description();
            }
            return false;
        }).on('click', '.item .cancel', function(e){
            e.preventDefault();
            close_description();
        });
    });

    $(window).bind('smartresize', layout_description);

    $(window).load(function() {
        var $container = $('#container'),
            filters = {};

        if (!$container.length) {
            return;
        }

        var $filters = $('#filters');
        var $filter_summary = $('#filter-summary');

        var url_filters = {};

        var filtering_busy = false;

        $('.panel-collapse', $filters).on('show.bs.collapse', function(event) {
            $.bbq.pushState({filter_section: $(event.target).attr('id').replace(/^filter-/, '')});
        });
        var hash_vars = $.bbq.getState();
        if (hash_vars.filter_section) {
            $('#toggle-list-filter').click();
            $('.btn[data-target="#filter-' + hash_vars.filter_section + '"]', $filters).click();
        }

        // filter buttons
        $('.filter a').on(activation_event, function(e, dont_load_data_yet){
            e.preventDefault();
            if (filtering_busy && !dont_load_data_yet) {
                return;
            }
            filtering_busy = true;
            var $this = $(this);
            var $li = $this.closest('li');

            var $optionSet = $this.closest('.option-set');
            // store filter value in object
            // i.e. filters.category = ['.cat_history']
            var group = $optionSet.attr('data-filter-group');
            filters[group] = filters[group] || [];
            var filter_value = $this.attr('data-filter-value');
            var single_selection = $optionSet.attr('data-single-selection');
            var hierarchical = $optionSet.attr('data-hierarchical');
            var level = parseInt($li.attr('data-level'), 10);
            var children_selector = $this.attr('data-level-1-at');
            var target_child = $this.attr('data-target');
            var $children;
            if (children_selector) {
                $children = $(children_selector);
            } else if (level === 1) {
                $children = $this.closest('.level-1-container');
            }
            var param = $li.data('param');
            var value = $li.data('value');

            if (filter_value) {
                if ($li.hasClass('active')) {
                    //$this.removeClass('selected');
                    $li.removeClass('active');
                    if ($children && level === 0) {
                        $('li.active>a', $children).trigger(activation_event, [true]);
                        $('ul.in', $children).removeClass('in');
                    }
                    filters[group] = $.grep(filters[group], function(v) {
                        return v !== filter_value;
                    });
                    // remove the corresponding item from filter summary
                    $('li[data-param="' + param + '"]', $filter_summary).remove();
                    if ($filter_summary.children().length === 1) {
                        $filter_summary.empty();
                    }
                    url_filters[param] = false;
                } else {
                    if (hierarchical) {
                        if (single_selection) {
                            // unselect previously selected
                            // and collect filters
                            if (level === 0) {
                                $('li.active>a', $optionSet).trigger(activation_event, [true]);
                                if ($children) {
                                    $('ul.in', $children).removeClass('in');
                                }
                                filters[group] = [filter_value];
                            } else {
                                if ($children) {
                                    $('li.active>a', $children).trigger(activation_event, [true]);
                                }
                                filters[group].push(filter_value);
                            }
                        } else {
                            filters[group].push(filter_value);
                        }
                    } else {
                        if (single_selection) {
                            // unselect previously selected
                            // and collect filters
                            $('li.active>a', $optionSet).trigger(activation_event, [true]);
                            filters[group] = [filter_value];
                        } else {
                            filters[group].push(filter_value);
                        }
                    }
                    url_filters[param] = value;
                    // change selected class
                    $li.addClass('active');
                    if ($children) {
                        $(target_child, $children).addClass('in');
                    }
                    var $filter_summary_li;
                    if ($filter_summary.text().trim() === "") {
                        $filter_summary_li = $('<li><b>' + window.str_filter_selection + ':</b></li>');
                        $filter_summary.append($filter_summary_li);
                    }
                    $filter_summary_li = $('<li data-filter-group="' + group + '" data-filter-value="' + filter_value + '" data-param="' + param + '" data-value="' + value + '"><a href="">' + $this.text() + '</a></li>');
                    $filter_summary.append($filter_summary_li);
                    $filter_summary.css('display', 'block');  // hack for Safari
                }
            }

            // convert object into array
    //        var http_state_filters = [];
            var map_filters = [];
            for (var prop in filters) {
    //            http_state_filters.push(filters[prop].join(''));
                for (var i=0; i<filters[prop].length; i++) {
                    var cat = filters[prop][i].replace(/\./, '');
                    map_filters.push(cat);
                }
            }

            url_filters['page'] = ""; // reset pagination
            var url = '?' + window.append_to_get(url_filters, true);
            window.history.pushState({}, document.title, url);
            if (!dont_load_data_yet) {
                if ($('#container').jscroll.destroy) {
                    $('#container').jscroll.destroy();
                }
                $('#container').load(url + ' #container>*', function() {
                    reinit_infinite_scroll();
                    setTimeout(function() { // waiting for the ad to load
                        lazyload_images();
                        filtering_busy = false;
                    }, 500);
                });
            } else {
                filtering_busy = false;
            }
            $container.trigger("map_filter", { filter: map_filters});
            return false;
        });

        $filter_summary.on(activation_event, 'a', function(e) {
            e.preventDefault();
            var $li = $(this).closest('li');
            var param = $li.data('param');
            var value = $li.data('value');
            if (!param) {
                // trigger the clicks on all selected filters
                $('li.active>a', $filters).trigger(activation_event);
            } else {
                // trigger the click on corresponding filter
                $('li.active[data-param="' + param + '"][data-value="' + value + '"]>a', $filters).trigger(activation_event);
            }
        });

        $('#filter-reset').on(activation_event, function(e) {
            e.preventDefault();
            // for each active link from the last till the first, click to deactivate
            $($('li.active>a', $filters).get().reverse()).trigger(activation_event, [true]);
            if ($('#container').jscroll.destroy) {
                $('#container').jscroll.destroy();
            }
            $('#container').load('? #container>*', function() {
                reinit_infinite_scroll();
                lazyload_images();
            });
        });

    //    if (window.location.hash) {
    //        // get options object from hash
    //        var options = window.location.hash ? $.deparam.fragment(window.location.hash, true) : {};
    //        // apply options from hash
    //        if (options.filter) {
    //            $(options.filter.split('.')).each(function() {
    //                if (!this) {
    //                    return;
    //                }
    //                $('a[data-filter-value=".' + this + '"]', $filters).click();
    //            });
    //        }
    //    }
    });

    $(window).load(function() {
        setTimeout(function() {
            $('body').removeClass('no-transition');
        }, 1000);
    });

}(jQuery));