/* jshint unused:false, eqnull:false, sub:true */
/* global $:false */
/* global lazyload_images:false */
/* global isotope_list:false */

(function($, undefined) {
    var activation_event = "click";
    if (navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|IEMobile|Opera Mini|webOS/i)) {
        activation_event = "touchstart";
    }

    function redo_description() {
        var $container = $('#container');
        var $current_item = $('#item-preview');
        if (!$current_item.length) {
            return;
        }
        var $description = $current_item.find(".description");

        // define position for the description
        var left = $current_item.position().left;
        var width = $container.width();
        var offset_left = parseInt($container.css('margin-left'), 10);
        var offset_right = parseInt($container.css('margin-right'), 10);

        $description.css({
            left: -left,
            width: width + offset_left + offset_right
        });
        isotope_list();
    }

    function reinit_infinite_scroll() {
        if (!navigator.userAgent.match(/Android|BlackBerry|iPhone|iPad|iPod|IEMobile|Opera Mini|webOS/i)) {
            var $pagination = $('.pagination').removeClass('item').hide();
            var $container = $('#container').data('jscroll', null);
            if ($pagination.length) {
                $container.jscroll({
                    loadingHtml: '<small>Loading...</small>',
                    // padding: 30,
                    contentSelector: '#container .isotope',
                    nextSelector: '.next_page:last',
                    pagingSelector: '.pagination',
                    callback: function() {
                        $('.pagination').removeClass('item').hide();
                        isotope_list();
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

        $('#container').on('click', '.item>a', function() {
            var $current_item = $(this).closest('.item');
            redo_description();

            if ($current_item.attr('id')) { // if clicked again, close the preview
                $('#item-preview').attr("id", "");
                isotope_list();
                lazyload_images();
                return false;
            }

            $('#item-preview').attr("id", ""); // close the previous preview
            $current_item.attr("id","item-preview"); // open the new preview

            var $description = $current_item.find(".description");

            // if description doesn't exist yet, load it
            if (!$.trim($description.text())) {
                $description.load($current_item.data('description-src'), function() {
                    $('#container .item .cancel').on('click', function(){
                        $('#item-preview').attr("id","");
                        isotope_list();
                        lazyload_images();
                    });

                    redo_description();

                    if (window.init_share) {
                        window.init_share();
                    }
                });
            } else {
                isotope_list();
            }
            return false;
        });
    });

    $(window).bind('smartresize', redo_description);

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
                        $('li.active>a', $children).trigger('click', [true]);
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
                                $('li.active>a', $optionSet).trigger('click', [true]);
                                if ($children) {
                                    $('ul.in', $children).removeClass('in');
                                }
                                filters[group] = [filter_value];
                            } else {
                                if ($children) {
                                    $('li.active>a', $children).trigger('click', [true]);
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
                            $('li.active>a', $optionSet).trigger('click', [true]);
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
            var isoFilters = [];
    //        var http_state_filters = [];
            var map_filters = [];
            for (var prop in filters) {
    //            http_state_filters.push(filters[prop].join(''));
                for (var i=0; i<filters[prop].length; i++) {
                    var cat = filters[prop][i].replace(/\./, '');
                    map_filters.push(cat);
    //                isoFilters.push('[data-filter-categories~="' + cat + '"]');
                }
            }

            var url = '?' + window.append_to_get(url_filters, true);
            window.history.pushState({}, document.title, url);
            if (!dont_load_data_yet) {
                if ($('#container').jscroll.destroy) {
                    $('#container').jscroll.destroy();
                }
                $('#container').load(url + ' #container>*', function() {
                    reinit_infinite_scroll();
                    setTimeout(function() { // waiting for the ad to load
                        isotope_list();
                        lazyload_images();
                    }, 500);
                });
            }
    //        var selector = isoFilters.join('');

    //        $.bbq.pushState({filter: http_state_filters.join('')});

    //        $container.isotope({filter: '.item' + selector});

    //        if ( !$container.data('isotope').$filteredAtoms.length ) {
    //            $container.addClass('empty');
    //            $("#empty-container").addClass("on");
    //        } else {
    //            $container.removeClass('empty');
    //            $("#empty-container").removeClass("on");
    //        }

    //        lazyload_images();
    //        $(".isotope-item:not(.isotope-hidden) .img", $container).trigger("appear");

            $container.trigger("map_filter", { filter: map_filters});

            filtering_busy = false;
            return false;
        });

        $filter_summary.on(activation_event, 'a', function() {
            var $li = $(this).closest('li');
            var param = $li.data('param');
            var value = $li.data('value');
            if (!param) {
                // trigger the clicks on all selected filters
                $('li.active>a', $filters).click();
            } else {
                // trigger the click on corresponding filter
                $('li.active[data-param="' + param + '"][data-value="' + value + '"]>a', $filters).click();
            }
            return false;
        });

        $('#filter-reset').on(activation_event, function() {
            // for each active link from the last till the first, click to deactivate
            $($('li.active>a', $filters).get().reverse()).trigger('click', [true]);
            if ($('#container').jscroll.destroy) {
                $('#container').jscroll.destroy();
            }
            $('#container').load('? #container>*', function() {
                reinit_infinite_scroll();
                isotope_list();
                lazyload_images();
            });
            return false;
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