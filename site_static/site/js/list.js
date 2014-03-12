/* jshint unused:false, eqnull:false, sub:true */
/* global self: false */
/* global jQuery: false */
/* global lazyload_images: false */
/* global isotope_list: false */

function redo_description() {
    var $container = $('#container');
    var $current_item = $('#item-preview');
    if (!$current_item.length) { return; }
    var $description = $current_item.find(".description");

    // define position for the description
    var left = $current_item.position().left;
    var width = $container.width();
    var offset_left = parseInt($container.css('margin-left'), 10);
    var offset_right = parseInt($container.css('margin-right'), 10);

    $description.css({left: -left, width: width + offset_left + offset_right});
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
                debug: true,
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

    $('#container .item > a').click(function() {
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
                $('#container .item .cancel').click(function(){
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

    // filter buttons
    $('.filter a').click(function(e){
        e.preventDefault();
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
        var param = $this.data('param');
        var value = $this.data('value');

        if (filter_value) {
            if ($this.hasClass('selected')) {
                $this.removeClass('selected');
                $li.removeClass('selected');
                if ($children && level === 0) {
                    $children.find('a.selected').click();
                    $children.find('ul.in').removeClass('in');
                }
                filters[group] = jQuery.grep(filters[group], function(v) {
                    return v !== filter_value;
                });
                // remove the corresponding item from filter summary
                $('li[data-filter-group="' + group + '"][data-filter-value="' + filter_value + '"]', $filter_summary).remove();
                if ($filter_summary.children().length === 1) {
                    $filter_summary.empty();
                }
                url_filters[param] = false;
                if (param === "category") {
                    url_filters['subcategory'] = false;
                }
            } else {
                if (hierarchical) {
                    if (single_selection) {
                        // unselect previously selected
                        // and collect filters
                        if (level === 0) {
                            $optionSet.find('a.selected').click();
                            if ($children) {
                                $children.find('ul.in').removeClass('in');
                            }
                            filters[group] = [filter_value];
                        } else {
                            if ($children) {
                                $children.find('a.selected').click();
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
                        $optionSet.find('a.selected').click();
                        filters[group] = [filter_value];
                    } else {
                        filters[group].push(filter_value);
                    }
                }
                url_filters[param] = value;
                // change selected class
                $this.addClass('selected');
                $li.addClass('selected');
                if ($children) {
                    $children.find(target_child).addClass('in');
                }
                
                if ($filter_summary.text() === "") {
                    $li = $('<li><b>' + window.str_filter_selection + ':</b></li>');
                    $filter_summary.append($li);
                }
                $li = $('<li data-filter-group="' + group + '" data-filter-value="' + filter_value + '"><a href="">' + $this.text() + '</a></li>');
                $filter_summary.append($li);
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
        $('#container').load(url + ' #container>*', function() {
            reinit_infinite_scroll();
            isotope_list();
            lazyload_images();
        });
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

        return false;
    });

    $filter_summary.on('click', 'a', function() {
        var $this = $(this).closest('li');
        var param = $this.data('param');
        var value = $this.data('value');
        if (!param) {
            // trigger the clicks on all selected filters
            $('a.selected', $filters).click();
        } else {
            // trigger the click on corresponding filter
            $('a[data-param="' + param + '"][data-value="' + value + '"]', $filters).click();
        }
        return false;
    });

    $('#filter-reset').on('click', function() {
        $('a.selected', $filters).click();
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