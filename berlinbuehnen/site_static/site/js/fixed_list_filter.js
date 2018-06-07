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
    
    /**
     * The constructor.
     * Gets the jQuery object of the filter.
     *
     * @param   $main   the jQuery object of the filter
     */
    function Filter($main) {
        
        var me = this;
        this.me = me;
        
        me.loading = false;
        
        me.$main = $main;
        var connect_id = me.$main.attr('id').split('_', 2);
        me.connect_id = connect_id[0];
        me.date = null;
        
        me.$list = $('#'+me.connect_id+'_list');    
        me.$dateslider = $('#'+me.connect_id+'_dateslider');
        
        me.reinit();
        me.$suboptions.addClass('closed');
        
        me.$main.data('filter', me);
    }
    
    /**
     * Reinitialises the connected components of the filter
     * after new content got loaded.
     * 
     * Gets called internaly.
     */
    Filter.prototype.reinit = function() {
        
        if (this.me) var me = this.me;
        
        me.$options_wrapper = $('.filter-options-wrapper', me.$main);
        me.$search_wrapper = $('.filter-search-wrapper', me.$main);
        me.$set_wrapper = $('.filter-set-wrapper', me.$main);
        
        me.$options = $('.filter-option', me.$options_wrapper);
        me.$suboptions = $('.filter-suboptions', me.$options_wrapper);
        me.$singletons = $('.singleton',  me.$options_wrapper);
        
        me.$options.click(function() {me.onOptionClicked($(this));});
        $('a', me.$main).click(function(event) {me.onLinkClicked(event);});
        
    }
    
    /**
     * Resets the date.
     * It's called internaly (e.g. from the connected dateslider)
     *
     * @param   date    the new date object
     */
    Filter.prototype.resetDate = function(date) {
        
        if (this.me) var me = this.me;
            
        var year = date.getFullYear();
        var month = date.getMonth()+1;
        var day = date.getDate();
        if (month < 10) month = "0"+month;
        if (day < 10) day = "0"+day;
        var date_string = year+'-'+month+'-'+day;
        
        me.date = date_string;
    }
    
    /**
     * An option got clicked.
     * Handels additional styling related to the click.
     *
     * @param   $this   the jQuery option clicked
     */
    Filter.prototype.onOptionClicked = function($this) {
        
        if (this.me) var me = this.me;
        
        me.$options.removeClass('active');
        $this.addClass('active');

        var $target = $($this.data('target'), me.$main);
        var is_closed = $target.hasClass('closed');
       
        if (is_closed) {
            me.$suboptions.addClass('closed');
            $target.removeClass('closed');
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
        if (!me.$list.length) return true;

        event.preventDefault();
        
        if (me.loading) return false;
        me.loading = true;
        
        var $this = $(event.target);
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
        console.log(params);
        
        // handling parent/child relations
        // removes the children if a parent is selected
        // removes the parent if a child is selected
        var $root = $this.closest('.filter-suboptions');
        if ($root.length) {
            
            var remove = [];
            var root = $root.get(0);
            
            var $parent = $this.closest('.parent', root);
            if ($parent.length && !$parent.hasClass('active')) {
                $('.child.active', $root).each(function() {
                    remove.push($(this).data('value'));
                });
            }
            
            var $child = $this.closest('.child', root);
            if ($child.length && !$child.hasClass('active')) {
                $('.parent.active', $root).each(function() {
                    remove.push($(this).data('value')); 
                });
            }
            
            for (var i=0, length=remove.length; i<length; i++) {
                
                var value = remove[i].split('=');
                var param = params[value[0]];
                
                if (typeof param === "object") {
                    for (var p=0; p<param.length; p++) {
                        if (param[p] === value[1]) {
                            param[p] = '';
                            break;
                        }
                    }
                } else {
                    if (param === value[1]) {
                        params[value[0]] = '';
                    }
                }
            }
        }
        
        
        // handling a full reset
        if (params['reset']) {
            
            $('.active', me.$suboptions).each(function() {
                
                $this = $(this);
                var value = $this.data('value').split("=");
                delete params[value[0]];
            });
            
            me.$singletons.each(function() {
                
                $this = $(this);
                if ($this.hasClass('active')) {
                    var value = $this.data('value').split("=");
                    delete params[value[0]];
                }
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
            
                // resetting the classes of the new elements with the corresponding old elements
            var $new_options_wrapper = $('.filter-options-wrapper', $new_main);
            var $new_options = $('.filter-option', $new_options_wrapper);
            var $new_suboptions = $('.filter-suboptions', $new_options_wrapper);
            
            for (i=0, length = $new_options.length; i<length; i++) {
                
                $new_option = $($new_options.get(i));
                $old_option = $(me.$options.get(i));
                
                $new_option.attr('class', $old_option.attr('class'));
            }
            
            for (i=0, length = $new_suboptions.length; i<length; i++) {
                
                $new_option = $($new_suboptions.get(i));
                $old_option = $(me.$suboptions.get(i));
                
                $new_option.attr('class', $old_option.attr('class'));
            }
            
            // the actual replacing
            me.$main.html($new_main.html());
            me.reinit();
            
            
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