/**
 * Handles form functionality and styling.
 *
 * @author Daniel Lehmann
 */

$(document).ready(function() {
    
    
    // the input prefix highlighting
    $('.input-field input[type="text"], .input-field input[type="password"], .input-field input[type="email"], .input-field input[type="url"], .input-field input[type="search"], .input-field input[type="tel"], .input-field input[type="number"], .input-field input[type="file"]').each(function() {
        
        var $field = $(this);
        var $prefix = $field.parent().prev('.input-prefix');
        
        if ($prefix.length) {
         
            $field.data('$prefix', $prefix);
            
            var onFocus = function() {
                var $field = $(this);
                var css_class = ($field.prop('readonly')) ? 'focus-readonly' : 'focus';
                $field.data('$prefix').addClass(css_class);
            }
            
            var onBlur = function() {
                var $field = $(this);
                $field.data('$prefix').removeClass('focus-readonly focus');
            }
            
            $field.focus(onFocus);
            $field.blur(onBlur);
        }
    });
    
    
    // auto size of textareas
    function TextArea($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        
        me.$main.on('change cut paste drop keydown', function() {me.resize(0);});
        $(window).resize(function() {me.resize();});
        
        me.resize();
        me.resize(100);
        
        me.$main.data('TextArea', me);
    }
    
    TextArea.prototype.resize = function(delay) {
     
        var me = this.me;
            
        if (typeof delay != "undefined") {
            setTimeout(function() {me.resize();}, delay);
        }
        
        var disabled = me.$main.prop('disabled');     
        me.$main.parents('fieldset').each(function() {
            if ($(this).prop('disabled')) disabled = true;
        });
        
        var padding = disabled ? 0 : 30;
        me.$main.css('height', '');
        me.$main.height(me.$main.get(0).scrollHeight - padding); 
    }
    
    $('.input-field textarea').each(function() {
        new TextArea($(this)); 
    });
    
    
    // making sure the label height fits for a check box or radio button
    function InputBox($main) {
        
        var me = this;
        this.me = me;
        
        // the top + bottom padding of the label
        me.padding = 16;
        
        me.$main = $main;
        me.$label = $('label', me.$main);
        
        me.checkHeight();
        $(window).resize(function() {me.checkHeight();});
        
        me.$main.data('InputBox', me);
    }
    
    InputBox.prototype.checkHeight = function() {
     
        var me = this.me;
        
        me.$main.css('min-height', (me.$label.height() + me.padding) + 'px');
    }
    
    $('.input-field.box').each(function() {
        new InputBox($(this)); 
    });
    
    
    // styling and functionality of file inputs
    function InputFile($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.disabled = me.$main.prop('disabled');
        me.readonly = me.$main.prop('readonly');
        me.only_button = me.$main.hasClass('only-button');
        
        me.$main.parents('fieldset').each(function() {
            if ($(this).prop('disabled')) me.disabled = true;
        });
        
        me.$wrapper = $('<div class="input-file-display-wrapper"></div>');
        me.$display = $('<input type="text" class="input-file-display" disabled="disabled"/>');
        me.$button = $('<div class="button input-file-button">'+trans["Choose"]+'</div>');
        
        
        if (me.$main.hasClass('default')) me.$button.addClass('default');
        else if (me.$main.hasClass('primary')) me.$button.addClass('primary');
        else if (me.$main.hasClass('success')) me.$button.addClass('success');
        else if (me.$main.hasClass('warning')) me.$button.addClass('warning');
        else if (me.$main.hasClass('danger')) me.$button.addClass('danger');
        if (me.only_button) me.$button.addClass('only-button');
        
        
        me.$display.attr('placeholder', me.$main.attr('placeholder'));
        
        var value = me.$main.attr('value');
        value = (value) ? value.split('\\').pop().split('/').pop() : '';
        me.$display.attr('value', value);
        
        if (me.$main.hasClass("error")) me.$display.addClass('error');
        if (me.readonly) me.$display.addClass('readonly');
        if (me.disabled) {
            me.$display.addClass('disabled');
            me.$wrapper.addClass('disabled');
        }
        if (me.$main.is(":focus")) me.$display.addClass('focus');
        
        me.$main.addClass('input-file-hide');
        
        
        me.$wrapper.append(me.$display);
        if (!me.only_button) me.$main.after(me.$wrapper);
        if (!me.disabled && !me.readonly) me.$main.after(me.$button);
        
        
        me.$main.click(function(e) {return me.onFileClick(e);});
        me.$main.change(function() {me.onFileChange();});
        me.$main.focus(function() {me.onFocus();});
        me.$main.blur(function() {me.onBlur();});
        
        if (!me.disabled) {
            me.$button.click(function() {me.onClick();});
            me.$wrapper.click(function() {me.onClick();});
        }
        
        me.$main.data('InputFile', me);
    }
    
    InputFile.prototype.setDisabled = function(value) {
        
        var me = this.me;
        
        me.disabled = value;
        
        if (value) {
            
            me.$display.addClass('disabled');
            me.$wrapper.addClass('disabled');
            me.$button.remove();
            me.$wrapper.off();
            
        } else {
            
            me.$display.removeClass('disabled');
            me.$wrapper.removeClass('disabled');
            me.$main.after(me.$button);
            me.$button.off().click(function() {me.onClick();});
            me.$wrapper.off().click(function() {me.onClick();});
        }
    }
    
    InputFile.prototype.onFileClick = function(event) {
        
        var me = this.me;
        
        if (me.readonly) {
            event.stopPropagation();
            event.preventDefault();
            return false;
        }
        
        return true;
    }
    
    InputFile.prototype.onFileChange = function() {
     
        var me = this.me;
        
        var value = me.$main.get(0).value.split('\\').pop().split('/').pop();
        me.$display.attr('value', value);
    }
    
    InputFile.prototype.onClick = function() {
     
        var me = this.me;
        
        me.$main.focus();
        me.$main.trigger('click');
    }
    
    InputFile.prototype.onFocus = function() {
     
        var me = this.me;
        me.$display.addClass('focus'); 
        me.$button.addClass('focus');
    }
    
    InputFile.prototype.onBlur = function() {
        
        var me = this.me;
        me.$display.removeClass('focus');
        me.$button.removeClass('focus');
    }
    
    $('.input-field input[type="file"]').each(function() {
        new InputFile($(this)); 
    });
    
    
    
    // styling and functionality of select boxes
    function SelectBox($main) {
        
        var me = this;
        this.me = me;
        
        // the top + bottom padding of a .select-option
        me.option_padding = 14;
        // the size of the top + bottom border of the .select-dropdown
        me.dropdown_border = 2;
        
        me.$main = $main;
        me.$body = $('#body');
        me.$window = $(window);
        
        me.disabled = me.$main.prop('disabled');
        me.readonly = me.$main.hasClass('readonly');
        me.autoload = me.$main.hasClass('autoload');
        me.multiple = me.$main.prop('multiple');
        me.required = me.$main.prop('required');
        
        me.$main.parents('fieldset').each(function() {
            if ($(this).prop('disabled')) me.disabled = true;
        });
        
        if (me.autoload) {
            
            me.multiple = false;
            me.$main.prop('multiple', false);
            
            me.load_url = me.$main.attr('data-load-url');
            me.load_start = parseInt(me.$main.attr('data-load-start'));
            if (!me.load_start) me.load_start = 2;
            if (me.load_start < 1) me.load_start = 1;
            
            me.loading = false;
            me.loading_value = '';
            
            if (me.readonly || me.disabled) {
                me.autoload = false;
                me.$main.removeClass('autoload');
            }
        }
        
        
        me.size = me.$main.attr('size');
        if (!me.size) me.size = 5;
        me.$main.attr('size', 2);
        
        me.option_height = 0;
        me.option_selected = [];
        me.option_focus = 0;
        me.option_focused = -1;
        me.closing_dropdown = null;
        me.required_adapted = false;
        
        
        if (me.readonly) {
            var $options = $('option', me.$main);
            $options.each(function(index) {
                var $option = $(this);
                if ($option.prop('selected')) me.option_selected[index] = true;
                else me.option_selected[index] = false;
            });
        }
        
        
        var disabled = (me.autoload) ? '' : ' disabled="disabled"';
        me.$wrapper = $('<div class="select-display-wrapper"></div>');
        me.$display = $('<input type="text" class="select-display"'+disabled+'/>');
        me.$dropdown_wrapper = $('<div class="select-dropdown-wrapper"></div>');
        me.$dropdown = $('<div class="select-dropdown"></div>');
        
        me.$display.attr('placeholder', me.$main.attr('placeholder'));
        
        if (!me.disabled && !me.readonly) {
            me.fillDropdown();
        }
        
        me.$display.attr('value', me.getValue());
        
        if (me.$main.hasClass("error")) me.$display.addClass('error');
        if (me.readonly) {
            me.$display.addClass('readonly');
            me.$wrapper.addClass('readonly');
        }
        if (me.disabled) {
            me.$display.addClass('disabled');
            me.$wrapper.addClass('disabled');
        }
        if (me.$main.is(":focus")) me.$display.addClass('focus');
        if (me.autoload) {
            me.$display.addClass('autoload');
            me.$wrapper.addClass('autoload');
        }
        
        me.$main.addClass('select-hide');
        
        
        me.$wrapper.append(me.$display);
        me.$main.after(me.$wrapper);
        
        me.$dropdown_wrapper.append(me.$dropdown);
        if (!me.disabled && !me.readonly) {
            me.$main.after(me.$dropdown_wrapper);
        }
        
        
        me.$main.click(function(e) {return me.onSelectClick(e);});
        me.$main.keypress(function(e) {return me.onSelectKeypress(e);});
        
        me.$main.change(function(e) {me.onSelectChange(e);});
        me.$main.focus(function() {me.onSelectFocus();});
        me.$main.blur(function() {me.onSelectBlur();});
        
        if (!me.disabled) {
            me.$wrapper.click(function() {me.onClick();});
        }
        
        if (me.autoload) {
            me.$display.keyup(function() {me.onInputChange();});   
        }
        
        
        me.$window.resize(function() {me.onResize();});
        
        
        me.$main.data('SelectBox', me);
    }
    
    /**
     * Set/unset the disabled status of the select box.
     */
    SelectBox.prototype.setDisabled = function(value) {
        
        var me = this.me;
        
        me.disabled = value;
        
        if (value) {
            
            me.$display.addClass('disabled');
            me.$wrapper.addClass('disabled');
            me.$dropdown_wrapper.remove();
            me.$wrapper.off();
            
        } else {
            
            me.$display.removeClass('disabled');
            me.$wrapper.removeClass('disabled');
            
            me.fillDropdown();
            me.$main.after(me.$dropdown_wrapper);
            me.$wrapper.off().click(function() {me.onClick();});
        }
    }
    
    /**
     * The actual select box got clicked.
     * Cancels the event if readonly is set.
     */
    SelectBox.prototype.onSelectClick = function(event) {
        
        var me = this.me;
        
        if (me.readonly) {
            event.stopPropagation();
            event.preventDefault();
            return false;
        }
        
        return true;
    }
    
    /**
     * A key got pressed.
     * Checking for "enter" to close the dropdown.
     */
    SelectBox.prototype.onSelectKeypress = function(event) {
        
        var me = this.me;
        
        if (me.readonly) {
            event.stopPropagation();
            event.preventDefault();
            return false;
        }
        
        if (event.which == 13) {
            
            event.stopPropagation();
            event.preventDefault();
            
            if (me.multiple) {
                
                me.openDropdown();
                
                $('option', me.$main).each(function(index) {
                    if ($(this).prop('selected')) {
                        me.onOptionClick($('.select-index-'+index, me.$dropdown));
                        return false;
                    }
                });
                
            } else me.toggleDropdown();
            
            return false;
        }
        
        return true;
    }
    
    /**
     * The value of the actual select box changed.
     */
    SelectBox.prototype.onSelectChange = function(event) {
     
        var me = this.me;
        
        var $options = $('option', me.$main);
        
        if (me.multiple) {
            $options.each(function(index) {
                if ($(this).prop('selected')) {
                    me.option_focus = index;
                    return false;
                }
            });
        }
        
        if (me.readonly) {
            $options.each(function(index) {
                $(this).prop('selected', me.option_selected[index]);
            });            
        }
        
        me.$display.attr('value', me.getValue());
        
        me.selectSelectedOptions();
    }
    
    /**
     * The actual select box got focus.
     */
    SelectBox.prototype.onSelectFocus = function() {
     
        var me = this.me;
        me.$display.addClass('focus'); 
        
        me.openDropdown();
        
        
        // removes the empty option on a required selection at first focus of the box
        if (me.required && !me.required_adapted) {
            
            me.required_adapted = true;
            
            var $options = $('option', me.$main);
            var $first = $options.first();
            var nothing_selected = $first.prop('selected');
            
            $first.remove();
            if (nothing_selected) $($options.get(1)).prop('selected', true);
            
            me.fillDropdown();
            me.$display.attr('value', me.getValue());
        }
    }
    
    /**
     * The actual select box lost focus.
     */
    SelectBox.prototype.onSelectBlur = function() {
        
        var me = this.me;
        me.$display.removeClass('focus');
        
        
        // if multiple, select the marked options
        if (me.multiple) {
            
            var $options = $('option', me.$main);
            
            $options.each(function(index) {
            
                if (me.option_selected[index]) $(this).prop('selected', true);
                else $(this).prop('selected', false);
            });
        }
        
        
        me.closing_dropdown = setTimeout(function() {me.closeDropdown();}, 400);
    }
    
    /**
     * The input field of the pseudo select box got clicked.
     */
    SelectBox.prototype.onClick = function() {
     
        var me = this.me;
        
        if (!me.autoload) {
            me.$main.focus();
            me.$main.trigger('click');
        }
    }
    
    /**
     * Mouse hovers over an option.
     */
    SelectBox.prototype.onOptionHover = function() {
        
        var me = this.me;
        
        $('.select-option', me.$dropdown).removeClass('focus');
    }
    
    /**
     * An option in the dropdown of the pseudo select box got clicked.
     */
    SelectBox.prototype.onOptionClick = function($option) {
        
        var me = this.me;
        
        me.$main.focus();
        if (me.closing_dropdown) {
            clearTimeout(me.closing_dropdown);
            me.closing_dropdown = null;
        }
        
        
        
        var $options = $('option', me.$main);
        var $first = $options.first();
        
        // figuring out which option got clicked
        $options.each(function(index) {
            
            // got the option
            if ($option.hasClass('select-index-'+index)) {
                
                if (!me.multiple) {
                    
                    // if it isn't multiple, just select the option
                    
                    $(this).prop('selected', true); 
                    me.closeDropdown();
                    
                } else {
                    
                    // if mulitple, mark the now to be selected options in me.option_selected
                    
                    me.option_focus = index;
                    
                    // counting the currently selected options
                    var selected = 0;
                    for (var i=0, length=me.option_selected.length; i<length; i++) {
                        if (me.option_selected[i]) selected++;   
                    }
                    
                    // if not the last selected option got unselected
                    if (selected > 1 || !me.option_selected[index]) {
                        
                        // if empty option got selected, unselect all the other
                        if (index == 0 && !$first.attr('value')) {
                            
                            me.option_selected[0] = true;
                            for (var i=1, length=me.option_selected.length; i<length; i++) {
                                me.option_selected[i] = false;
                            }
                            
                        } else {
                            
                            // toggle the selection
                            
                            if (!$first.attr('value')) me.option_selected[0] = false;
                            if (me.option_selected[index]) me.option_selected[index] = false;
                            else me.option_selected[index] = true;
                        }
                        
                    } else {
                     
                        // if the empty option got unselected, mark all the other as selected
                        if (index == 0 && !$first.attr('value')) {
                            
                            me.option_selected[0] = false;
                            for (var i=1, length=me.option_selected.length; i<length; i++) {
                                me.option_selected[i] = true;
                            }
                            
                        } else if (!$first.attr('value')) {
                            
                            // if we have an empty first option, mark it and unselect the choice
                            // otherwise do nothing and prohibit the unselection of the last selected option
                            // since it is then a required selection box
                            
                            me.option_selected[0] = true;
                            me.option_selected[index] = false;
                        }
                        
                    }
                
                }
            }
        });
        
        
        
        me.$display.attr('value', me.getValue());
        
        me.selectSelectedOptions();
    }
    
    /**
     * Returns the currently selected values to display in the input field.
     */
    SelectBox.prototype.getValue = function() {
     
        var me = this.me;
        
        var $options = $('option', me.$main);
        
        var first = true;
        var values = [];
        $options.each(function(index) {
           
            var $option = $(this);
            if ((!me.multiple && $option.prop('selected')) || (me.multiple && me.option_selected[index])) {
                if (first && !me.required_adapted) values.push('');
                else values.push($option.text());
            }
            
            first = false;
        });
        
        return values.join(', ');
    }
    
    /**
     * Returns a calculated width of the displayed value in pixels based on a fixed letter width.
     */
    SelectBox.prototype.getValueWidth = function() {
     
        var me = this.me;
        
        var font_size = parseInt(me.$display.css('font-size'));
        var value = me.$display.attr('value');
        
        if (!value) value = me.$display.attr('placeholder');
        
        return value.length * font_size;
    }
    
    /**
     * Creates the dropdown of the pseudo select box.
     */
    SelectBox.prototype.fillDropdown = function() {
     
        var me = this.me;
        if (me.readonly) return;
        
        var $options = $('option', me.$main);
        
        me.$dropdown.html('');
        $options.each(function(index) {
            
            var $option = $(this);
            var multiple = (me.multiple) ? ' multiple' : '';
            var $element = $('<div class="select-option select-index-'+index+multiple+'">'+$option.text()+'</div>');
            me.$dropdown.append($element);
            
            $element.click(function() {me.onOptionClick($(this));});
            $element.mouseenter(function() {me.onOptionHover();});
        });
        
        me.option_selected = [];
        me.option_focus = 0;
        setTimeout(function() {me.positionDropdown();}, 0);
    }
    
    /**
     * Positions the dropdown depending on window size and scroll position of the window.
     * Sets the max-height of the dropdown.
     */
    SelectBox.prototype.positionDropdown = function() {
        
        var me = this.me;
        if (me.readonly) return;
        
        var dropdown_display = me.$dropdown.css('display');
        me.$dropdown.css('display', 'block');
        
        
        me.option_height = 1000;
        $('.select-option', me.$dropdown).each(function() {
            var height = $(this).height();
            if (height != 0 && height < me.option_height) me.option_height = height;
        });        
        
        
        me.$dropdown.css('top', '');
        me.$dropdown.css('bottom', '');
        me.$dropdown.css('max-height', Math.ceil(me.size * (me.option_height + me.option_padding) + me.dropdown_border) + 'px');
        
        
        var body_top = me.$body.offset().top;
        var body_height = me.$body.height();
        var display_top = me.$display.offset().top;
        var display_height = me.$display.height();
        var dropdown_height = me.$dropdown.height();
        var window_height = me.$window.height();
        var scroll_top = me.$window.scrollTop();
        
        var dropdown_top_space = Math.floor(display_top - body_top);
        var dropdown_bottom_space = Math.floor(body_height - dropdown_top_space - display_height);
        
        var window_top_space = Math.floor(display_top - scroll_top);
        var window_bottom_space = Math.floor(window_height - window_top_space - display_height);
        
        //console.log('dropdown_height: ' + dropdown_height);
        //console.log('dropdown_top_space: ' + dropdown_top_space);
        //console.log('dropdown_bottom_space: ' + dropdown_bottom_space);
        //console.log('window_top_space: ' + window_top_space);
        //console.log('window_bottom_space: ' + window_bottom_space);
        
        var top = false;
        if (display_top + display_height + dropdown_height > window_height + scroll_top && window_top_space > window_bottom_space) {
            top = true;
        }
        
        //console.log(top);
        
        if (top) {
            if (dropdown_top_space < dropdown_height && dropdown_top_space < dropdown_bottom_space) top = false;
        } else {
            if (dropdown_bottom_space < dropdown_height && dropdown_bottom_space < dropdown_top_space) top = true;
        }
        
        //console.log(top);
        
        if (top) {
            if (dropdown_top_space < dropdown_height) me.$dropdown.css('max-height', dropdown_top_space+'px');
        } else {
            if (dropdown_bottom_space < dropdown_height) me.$dropdown.css('max-height', dropdown_bottom_space+'px');
        }
        
        dropdown_height = me.$dropdown.height();
        
        if (top) {
            if (window_top_space < dropdown_height) me.$dropdown.css('max-height', window_top_space+'px');
        } else {
            if (window_bottom_space < dropdown_height) me.$dropdown.css('max-height', window_bottom_space+'px');
        }
        
        
        if (top) {
            me.$dropdown.css('top', '-' + (dropdown_height) + 'px');
        } else {
            me.$dropdown.css('bottom', '-' + (dropdown_height + display_height + 2) + 'px');
        }
        
        
        me.selectSelectedOptions();
        me.$dropdown.css('display', dropdown_display);
    }
    
    /**
     * Marks the selected options in the dropdown of the pseudo select box.
     * Also adds the focus class to the currently active option in the droppdown
     * and scrolls the dropdown, so that the option is visible in the dropdown.
     */
    SelectBox.prototype.selectSelectedOptions = function() {
        
        var me = this.me;
        if (me.readonly) return;
        
        var $options = $('option', me.$main);
        
        // mark selected options in the dropdown
        var selected = 0;
        $options.each(function(index) {
            
            var $display_option = $('.select-index-'+index, me.$dropdown);
            if ($display_option.length) {
                
                var old_selection = me.option_selected[index];
                
                var $option = $(this);
                if ((!me.multiple && $option.prop('selected')) || (me.multiple && old_selection)) {
                    $display_option.addClass('selected');
                    me.option_selected[index] = true;
                    selected++;
                } else {
                    $display_option.removeClass('selected');
                    me.option_selected[index] = false;
                }
                
                if (!me.multiple && old_selection != me.option_selected[index] && me.option_selected[index]) me.option_focus = index;
            }
        });
        
        
        if (!selected) {
            
            me.option_focus = 0;
            me.option_selected[0] = true;
            var $display_option = $('.select-index-0', me.$dropdown);
            $display_option.addClass('selected');
            $options.first().prop('selected', true);
        }
        
        
        // if the focused option changed
        if (me.option_focus != me.option_focused) {
            
            // setting focus to the newly changed option
            $('.select-option', me.$dropdown).removeClass('focus');
            var $display_option = $('.select-index-'+me.option_focus, me.$dropdown);
            $display_option.addClass('focus');
            
            // make sure the focused option is visible in the dropdown
            var dropdown_height = me.$dropdown.height();
            var scroll_top = me.$dropdown.scrollTop();
            var option_height = $display_option.height() + me.option_padding;
            var option_top = $display_option.position().top;
            
            if (option_top + option_height > dropdown_height) {
                scroll_top =  option_top - dropdown_height + option_height + scroll_top;
            } else if (option_top < 0) {
                scroll_top += option_top;
            }
            
            me.$dropdown.scrollTop(scroll_top);
            
            me.option_focused = me.option_focus;
        }
    }
    
    /**
     * Toggles the visibility of th dropdown.
     */
    SelectBox.prototype.toggleDropdown = function() {
        
        var me = this.me;
        if (me.readonly) return;
        
        if (me.$dropdown.css('display') == 'none') {
            
            if (me.closing_dropdown) {
                clearTimeout(me.closing_dropdown);
                me.closing_dropdown = null;
            }
        
            me.$dropdown.css('display', 'block');
            me.positionDropdown();
            
        } else {
            me.$dropdown.css('display', 'none');
            me.$main.trigger('closed');
        }
    }
    
    /**
     * Opens the dropdown.
     */
    SelectBox.prototype.openDropdown = function() {
     
        var me = this.me;
        if (me.readonly) return;
        
        if (me.closing_dropdown) {
            clearTimeout(me.closing_dropdown);
            me.closing_dropdown = null;
        }
        
        me.$dropdown.css('display', 'block');
        me.positionDropdown();
    }
    
    /**
     * Calls the Avengers ... what do you think ;-)
     */
    SelectBox.prototype.closeDropdown = function() {
     
        var me = this.me;
        if (me.readonly) return;
        me.$dropdown.css('display', 'none');
        me.$main.trigger('closed');
    }
    
    /**
     * The window got resized.
     */
    SelectBox.prototype.onResize = function() {
     
        var me = this.me;
        
        if (!me.disabled && !me.readonly) {
            setTimeout(function() {me.positionDropdown();});
        }
    }
    
    
    /**
     * The input field got values for autoload.
     */
    SelectBox.prototype.onInputChange = function() {
        
        var me = this.me;
        
        if (!me.load_url) return;
        
        
        var onSuccess = function(options) {
            
            // TODO: repopulate the selection box and call me.fillDropdown();
            
            me.loading = false;
            me.$wrapper.removeClass('loading spin');
            
            var value = me.$display.get(0).value;
            if (value != me.loading_value) me.onInputChange();
            
        }
        
        var onError = function() {
            
            me.loading = false;
            me.$wrapper.removeClass('loading spin');
            
            var value = me.$display.get(0).value;
            if (value != me.loading_value) me.onInputChange();
        }
        
        var value = me.$display.get(0).value;
        
        if (value.length >= me.load_start && !me.loading) {
            
            // checking if the value is actual a chosen option
            var exists = false;
            var $options = $('option', me.$main);
            $options.each(function(index) {
                if ($(this).text() == value) {
                    exists = true;
                    return false;
                }
            });
            
            if (exists) return;
            
            
            me.loading = true;
            me.loading_value = value;
            
            me.$wrapper.addClass('loading');
            setTimeout(function() {me.$wrapper.addClass('spin');}, 10);
		
		    $.ajax({type: "POST", url: me.load_url, data: { value:value, cache:Math.round(Math.random()*1000000) }, cache: false, async: true}).done(onSuccess).fail(onError);
        }
    }
    
    $('.input-field select').each(function() {
        new SelectBox($(this)); 
    });
    
    
    
    // fieldset functionalities
    function Fieldset($main) {
        
        var me = this;
        this.me = me;
        
        // a value for correction of the calculated displayed value width of collapsed columns in disabled view
        // since all the letters usely don't have the same fixed letter width
        me.font_size_correction = 0.65;
        
        me.$main = $main;
        me.$body = $('body');
        me.$window = $(window);
        me.width = -1;
        me.height = -1;
        me.child = null;
        
        me.init();
        
        $(window).resize(function() {me.onResize();});
    }
    
    Fieldset.iframe_counter = 0;
    
    Fieldset.prototype.init = function() {
     
        var me = this.me;
        
        me.$fieldset = $('fieldset', me.$main);
        me.$files = $('.input-field input[type="file"]', me.$fieldset);
        me.$selects = $('.input-field select', me.$fieldset);
        me.$collapse_selects = $('.row.collapse > * select', me.$fieldset);
        me.$textareas = $('.input-field textarea', me.$fieldset);
        
        
        me.iframe_id = -1;
        me.edit_url = me.$main.attr('data-edit-url');
        me.parent = window.frameElement;
        if (me.parent) {
            var id = me.parent.id.split("-")[1];
            if (window.parent.iframe_fieldset) {
                me.parent = window.parent.iframe_fieldset[id];
                me.parent.child = me;
                window.setInterval(function() {me.checkHeight();}, 100);
            } else me.parent = null;
        }
        
        
        if (me.parent && me.$fieldset.prop('disabled')) {
            
            me.parent.replaceMainMarkup(me.$main.html());
            
        } else {
                
            if (me.$main.hasClass('editable')) me.editable();
            
        }
    }
    
    Fieldset.prototype.editable = function() {
        
        var me = this.me;
        
        var button = 'close';
        if (me.$fieldset.prop('disabled')) {
            button = 'edit';
            me.$main.addClass('disabled');
        }
        
        
        // the toggle is done by loading the edit markup
        // into an iframe, not by switching style classes
        if (me.edit_url) {
            
            if (me.$iframe) {
                me.$iframe.remove();
                window.iframe_fieldset[me.iframe_id] = null;
            }
            
            me.iframe_id = Fieldset.iframe_counter;
            Fieldset.iframe_counter++;
            
            me.$iframe = $('<iframe src="'+me.edit_url+'" class="iframe-edit" id="fieldset-'+me.iframe_id+'" frameborder="0" scrolling="no"></iframe>');
            me.$main.after(me.$iframe);   
            
            if (!window.iframe_fieldset) window.iframe_fieldset = [];
            window.iframe_fieldset[me.iframe_id] = me;
            
        }
        
        me.edit_button = $('<button class="edit-button button fawesome fa-'+button+' smaller primary"><span class="sr-only">'+trans[button]+'</span></button>');
        me.edit_button.click(function(e) {me.toggle(); return false;});
        $('.cancel', me.$main).click(function(e) {me.toggle(true); return false;});
        
        
        if (me.$main.hasClass('switch')) me.$main.prepend(me.edit_button);
        
        me.onResize();
    }
    
    Fieldset.prototype.toggle = function(disable) {
        
        var me = this;
        
        // you are in an iframe
        // let the parent do the work
        if (me.parent) {
            me.parent.toggle(true);
            return;
        }
            
        // your edit markup is in an iframe
        // toggle display of iframe and none iframe markup
        if (me.edit_url) {
            
            if (disable) {
                me.$iframe.css('display', '');
                me.$main.css('display', '');
            } else {
                me.$iframe.css('display', 'block');
                me.$main.css('display', 'none');
                window.setTimeout(function() {me.child.sizeParentIFrame();}, 0);
            }
            
            return;
        }
        
        
        // do the toggle by switching style classes
        var disabled = (typeof disable == "undefined") ? me.$fieldset.get(0).disabled : !disable;
        
        if (disabled) {
            
            me.edit_button.removeClass('fa-edit');
            me.edit_button.addClass('fa-close');
            me.$fieldset.prop('disabled', false);
            me.$main.removeClass('disabled');
            $('.sr-only', me.edit_button).text(trans['close']);
            
        } else {
            
            me.edit_button.addClass('fa-edit');
            me.edit_button.removeClass('fa-close');
            me.$fieldset.prop('disabled', true);
            me.$main.addClass('disabled');
            $('.sr-only', me.edit_button).text(trans['edit']);
        }
        
        me.$files.each(function() {
            $(this).data('InputFile').setDisabled(!disabled);  
        })
        
        me.$selects.each(function() {
            $(this).data('SelectBox').setDisabled(!disabled);  
        })
        
        me.$textareas.each(function() {
            $(this).data('TextArea').resize();  
        })
        
        me.collapseColumns();
        
    }
    
    Fieldset.prototype.checkHeight = function() {
     
        var me = this.me;
        
        if (me.height != me.$body.height()) {
            me.height = me.$body.height();
            me.onResize();
        }
    }
    
    Fieldset.prototype.sizeIFrame = function(height) {
        
        var me = this.me;
        
        if (!me.$iframe) return;
        
        me.$iframe.height(height);
    }
    
    Fieldset.prototype.sizeParentIFrame = function() {
     
        var me = this.me;
        
        if (me.parent) {
            me.parent.sizeIFrame(me.$body.height());
        }   
    }
    
    Fieldset.prototype.replaceMainMarkup = function(markup) {
     
        var me = this.me;
        
        me.$main.html(markup);
        me.init();
        me.toggle(true);
    }
    
    Fieldset.prototype.collapseColumns = function() {
     
        var me = this.me;
            
        var disabled = me.$fieldset.get(0).disabled;
        
        if (!disabled) {
                
            me.$collapse_selects.each(function() {
                
                var $select = $(this);
                var SelectBox = $select.data('SelectBox');
                SelectBox.$display.css('width', '');
            });
            
        } else {
                
            me.$collapse_selects.each(function() {
                
                var $select = $(this);
                var SelectBox = $select.data('SelectBox');
                var width = SelectBox.getValueWidth() * me.font_size_correction;
                SelectBox.$display.css('width', width+'px');
            });            
        }
    }
    
    Fieldset.prototype.onResize = function() {
     
        var me = this.me;
        
        me.collapseColumns();
        me.sizeParentIFrame();
        
        if (me.width == me.$window.width()) return;
        me.width = me.$window.width();
        
        if (me.$iframe) {
            me.$iframe.css('width', '');
            me.$iframe.width(me.$iframe.width() - 10);
        }
    }
    
    $('.fieldset').each(function() {
        new Fieldset($(this)); 
    });
});

