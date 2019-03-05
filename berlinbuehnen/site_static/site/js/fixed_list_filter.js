/**
 * Initiates event list filters on the page.
 *
 * The filter is catching all clicks of its a-tags and loads the content of the href using ajax.
 * Its replacing then the list belonging to the filter with the newly loaded list.
 *
 * The list belonging to this filter has to have the id resampling the first part of the filter id up to "_" and adding "_list".
 * E.g.: the filter with the id "main_filter" would belong to the list with the id "main_list".
 *
 * To attach a date slider to the filter, the slider has to have the id resampling the first part of the filter id up to "_" and adding "_dateslider".
 * The filter id has to end on "_filter".
 * E.g.: the filter with the id "main_filter" would be attached to the date slider with the id "main_dateslider".
 *
 * If no list is found, the filter links behave normal without ajax loading.
 *
 * @author Daniel Lehmann
 * @editor Aidas Bendoraitis
 */

(function() {


    function Filter($main) {

        var me = this;
        this.me = me;

        me.loading = false;

        me.$main = $main;
        me.$body = $('body');
        var connect_id = me.$main.attr('id').split('_', 2);
        me.connect_id = connect_id[0];
        me.date = null;

        me.$list = $('#'+me.connect_id+'_list');
        me.$dateslider = $('#'+me.connect_id+'_dateslider');


        me.$options_wrapper = $('.filter-options-wrapper', me.$main);
        me.$search_wrapper = $('.filter-search-wrapper', me.$main);
        me.$set_wrapper = $('.filter-set-wrapper', me.$main);

        me.$dropdowns = $('.filter-option-wrapper', me.$options_wrapper);
        me.$dropdown_triggers = $('.filter-option', me.$dropdowns);
        me.$dropdown_bodies = $('.filter-option-dropdown', me.$dropdowns);
        me.dropdown_opening = null;

        me.$singletons = $('.singleton',  me.$options_wrapper);

        me.$dropdown_triggers.click(function(event) {me.openDropdown($(this), event)});
        $('button.delete', me.$dropdown_bodies).click(function() {me.closeAllDropdowns();});
        $('a', me.$main).click(function(event) {me.onLinkClicked(event);});
        $(window).click(function(event) {me.closeAllDropdowns(event);});

        me.search_filter_interval = null;
        $('.filter-option-dropdown-search', me.$main).change(function() {me.searchFilter($(this));}).focus(function() {me.onSearchFilterFocus($(this));}).blur(function() {me.onSearchFilterBlur();});

        me.$main.data('filter', me);

        me.setMainCategoriesStyle();
    }

    /**
     * Reinitialises the connected components of the filter set
     * after new content got loaded.
     *
     * Gets called internaly.
     */
    Filter.prototype.reinitFilterSet = function() {

        if (this.me) var me = this.me;
        else var me = this;

        $('.filter-set-wrapper a', me.$main).click(function(event) {me.onLinkClicked(event);});

        me.setMainCategoriesStyle();
    }

    /**
     * Sets the class of the main category links (dropdown opener) eather active or not
     * depending if a subcategory is active or not.
     */
    Filter.prototype.setMainCategoriesStyle = function() {

        if (this.me) var me = this.me;
        else var me = this;

        me.$dropdowns.each(function() {

            var $this = $(this);
            var set = false;
            $('a', $this).each(function() {
                if ($(this).hasClass('active')) set = true;
            });

            if (set) $('.filter-option', $this).addClass('active');
            else $('.filter-option', $this).removeClass('active');
        });
    }

    /**
     * Resets the date.
     * It's called internaly (e.g. from the connected dateslider)
     *
     * @param   date    the new date object
     */
    Filter.prototype.resetDate = function(date) {

        if (this.me) var me = this.me;
        else var me = this;

        var year = date.getFullYear();
        var month = date.getMonth()+1;
        var day = date.getDate();
        if (month < 10) month = "0"+month;
        if (day < 10) day = "0"+day;
        var date_string = year+'-'+month+'-'+day;

        me.date = date_string;
    }

    /**
     * Opens a dropdown.
     *
     * @param   $trigger    the jquery object which triggers the opening of the dropdown
     * @param   event       the click event
     */
    Filter.prototype.openDropdown = function($trigger, event) {

        event.preventDefault();
        event.stopImmediatePropagation();

        var me = this;

        var $dropdown = $trigger.parents('.filter-option-wrapper');
        var $dropdown_body = $('.filter-option-dropdown', $dropdown);

        me.closeAllDropdowns();
        me.$body.addClass('filter-option-dropdown-open');
        $trigger.addClass('open');
        $dropdown_body.addClass('preopen');

        window.setTimeout(function() {
            $dropdown_body.addClass('open');
        }, 0);
    }

    /**
     * Closes all dropdowns.
     *
     * @param   event   the click event which might have triggered the closing (optional)
     */
    Filter.prototype.closeAllDropdowns = function(event) {

        if (event && $(event.target).parents('.filter-option-wrapper').length) return;

        var me = this;

        if (me.dropdown_opening) window.clearTimeout(me.dropdown_opening);
        me.dropdown_opening = null;

        me.$body.removeClass('filter-option-dropdown-open');
        me.$dropdown_triggers.removeClass('open');
        me.$dropdown_bodies.removeClass('open preopen');
    }

    /**
     * Starts an interval of calling searchFilter() for the given input field.
     * It's called on focus of the input field.
     *
     * @param   $input  the jquery object of the search input field
     */
    Filter.prototype.onSearchFilterFocus = function($input) {

        var me = this;

        me.onSearchFilterBlur();

        var callSearchFilter = function() {

            var $my_input = $input;
            return function() {me.searchFilter($my_input)};
        }

        me.search_filter_interval = window.setInterval(callSearchFilter(), 300);
    }

    /**
     * Stops the current interval of calling searchFilter().
     * It's called on blur of an search filter input field.
     */
    Filter.prototype.onSearchFilterBlur = function() {

        var me = this;

        if (me.search_filter_interval) window.clearInterval(me.search_filter_interval);
        me.search_filter_interval = null;
    }

    /**
     * Filters the visible links in a dropdown.
     *
     * @param   $input  the jquery object of the search input field
     */
    Filter.prototype.searchFilter = function($input) {

        var me = this;

        var value = $input.val().trim();
        var regexp = new RegExp(value, "gi");
        var $links = $('a', $input.parents('.filter-option-dropdown')).not('.parent');

        if (value.length) {

            $links.each(function() {

                $this = $(this);
                var check = $this.text();

                var found = false;
                var text = '';
                var position = check.search(regexp);
                while (position >= 0) {
                    found = true;

                    text += check.substr(0, position)+"<b>"+check.substr(position, value.length)+"</b>";
                    check = check.substr(position+value.length);

                    position = check.search(regexp);
                }
                text += check;

                $this.html(text);

                if (found) $this.parent().removeClass('hide');
                else $this.parent().addClass('hide');
            });

        } else {

            $links.parent().removeClass('hide');
            $links.each(function() {
                $this = $(this);
                $this.html($this.text());
            });
        }

    }

    /**
     * A link got clicked.
     * Handels the reloading of the content.
     *
     * @param   event   the jQuery click event
     */
    Filter.prototype.onLinkClicked = function(event) {

        if ($(event.delegateTarget).hasClass('filter-option')) {
            location.href = $(event.delegateTarget).attr('href');
            return true;
        }

        if (this.me) var me = this.me;
        else var me = this;
        if (!me.$list.length) return true;

        event.preventDefault();

        if (me.loading) return false;
        me.loading = true;

        var $this = $(event.target);


        //setting the style/class for the clicked link
        //gonna be set/exchanged again when the new page with the new link elements got loaded
        if ($this.hasClass('parent')) $('a', $this.parents('.parent-child')).removeClass('active');
        if ($this.parents('.filter-option-dropdown').length) $this.toggleClass('active');
        if ($this.parents('.singleton').length) $this.toggleClass('active');
        if ($this.hasClass('delete') && $this.attr('data-value')) $this.addClass('hide');


        var href = $this.attr('href');

        if (me.$list.jscroll.destroy) me.$list.jscroll.destroy();



        // converting the query string into an object
        var hash = href.split('#', 2);
        href = hash[0];
        hash = (hash.length === 2) ? hash = hash[1] : '';

        var search = href.split('?', 2);
        href = search[0];
        search = (search.length === 2) ? search[1].split('&') : '';

        var params = {};
        for (var i=0, length=search.length; i<length; i++) {

            var param = search[i].split('=', 2);

            if (params.hasOwnProperty(param[0])) {

                if (typeof params[param[0]] !== "object") {
                    params[param[0]] = [params[param[0]]];
                }

                params[param[0]].push(param[1]);

            } else {

                params[param[0]] = param[1];
            }
        }
        //console.log(params);



        // handling parent(all)/child relations
        // removes the children if a parent(all) is selected
        // removes the parent(all) if a child is selected
        var $root = $this.closest('.parent-child');
        if ($root.length) {

            var $remove = [];

            if ($this.hasClass('parent') && $this.hasClass('remover')) {
                $remove = $('.child', $root);
            }

            if ($this.hasClass('child') && $this.hasClass('remover')) {
                $remove = $('.parent', $root);
            }

            if ($remove.length) {
                $remove.each(function() {

                    var $link = $(this);
                    var query = $link.attr('data-query');
                    var pk = $link.attr('data-pk');

                    var param = params[query];

                    if (typeof param === "object") {
                        for (var p=0; p<param.length; p++) {
                            if (param[p] === pk) {
                                param[p] = '';
                                break;
                            }
                        }
                    } else {
                        if (param === pk) {
                            params[query] = '';
                        }
                    }

                });
            }
        }



        // handling a full reset
        if (params['reset']) {

            $('.filter-set a.delete', me.$set_wrapper).each(function() {

                $this = $(this);
                var value = $this.data('value').split("=");
                delete params[value[0]];
            });
        }


        // save the date
        if (!me.date && params['date']) me.date = params['date'];



        // removing page, date and the reset marker
        delete params['page'];
        delete params['date'];
        delete params['reset'];


        // creating the new query string
        var query = "?";
        for (var param in params) {

            if (typeof params[param] == "object") {
                for (var i=0, length = params[param].length; i<length; i++) {
                    if (params[param][i] !== '') query += param+"="+params[param][i]+"&";
                }
            } else {
                if (params[param] !== '') query +=  param+"="+params[param]+"&";
            }
        }

        var clean_query = query.substr(1, query.length-2);
        if (me.date) query += 'date='+me.date+'&';
        query = query.substr(0, query.length-1);

        href += query;
        if (hash) href += '#' + hash;


        // loading the new content
        var onContentLoaded = function(response, status, xhr) {
            var i, $new_option, $old_option;

            if (status === "error") {
                var msg = "Error loading filtered list: ";
                alert( msg + xhr.status + " " + xhr.statusText );
                me.loading = false;
                return false;
            }

            // replacing the old filter with the newly loaded
            var $response = $(response);
            var $new_main = $('#' + me.$main.attr('id'), $response);

            // resetting the classes and href of the old elements with the corresponding new elements
            var $new_options_wrapper = $('.filter-options-wrapper', $new_main);
            var $old_options = $('.filter-option-dropdown-scroll a, .singleton a', me.$options_wrapper);
            var $new_options = $('.filter-option-dropdown-scroll a, .singleton a', $new_options_wrapper);

            for (i=0, length = $new_options.length; i<length; i++) {

                $new_option = $($new_options.get(i));
                $old_option = $($old_options.get(i));

                $old_option.attr('class', $new_option.attr('class'));
                $old_option.attr('href', $new_option.attr('href'));
            }

            var $old_headline = $('.filter-headline', me.$main);
            var $new_headline = $('.filter-headline', $new_main);

            for (i=0, length = $new_headline.length; i<length; i++) {

                $new_option = $($new_headline.get(i));
                $old_option = $($old_headline.get(i));

                $old_option.attr('class', $new_option.attr('class'));
            }

            $('.filter-set', me.$main).html($('.filter-set', $new_main).html());
            $('.filter-set-wrapper', me.$main).attr('class', $('.filter-set-wrapper', $new_main).attr('class'));
            $('.filter-reset-button', me.$main).attr('href', $('.filter-reset-button', $new_main).attr('href'));
            me.reinitFilterSet();


            me.$list.data('list').reinitByFilter();
            if (me.$dateslider.length) me.$dateslider.data('dateslider').reinitByFilter(clean_query);

            me.loading = false;
        };


        if (href === '') href = '?';
        if (history.pushState) {
            history.pushState({}, document.title, href);
        }
        me.$list.load(href + " #" + me.connect_id + '_list', onContentLoaded);
    };

    function init() {

        $('.filter').each(function() {
            new Filter($(this));
        });

    }

    $(document).ready(init);


})();
