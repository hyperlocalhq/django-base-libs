/**
 * Handles form functionality and styling.
 *
 * @author Daniel Lehmann
 */

 
window.addToFormInit = function(func) {
    window.addToFormInit.functions.push(func);   
}
window.addToFormInit.functions = [];
 
 
$(document).ready(function() {
    
    
    // adds the functionality of all form elements
    // add the class "dont-add-form-functionality" to an element or one of its parents to not add form functionality to it
    function initFormElementsFunctionality($scope) {
        
    
        $('.input-field input[type="text"], .input-field input[type="password"], .input-field input[type="email"], .input-field input[type="url"], .input-field input[type="search"], .input-field input[type="tel"], .input-field input[type="number"], .input-field input[type="file"]', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new Prefix($element); 
        });
        
        
        $('.toggle-visibility', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new ToggleVisibility($element); 
        });
        
        $('.radio-toggle', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new RadioToggle($element); 
        });
    
        $('.dynamic-entries', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new DynamicEntries($element); 
        });
    
        $('.input-field textarea', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new TextArea($element); 
        });
        
        $('.input-field.box', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new InputBox($element); 
        });
    
        $('.input-field input[type="file"]', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new InputFile($element); 
        });

        $('.input-field input[placeholder="http://"]', $scope).each(function() {

            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);

            if (!dont) new URLField($element);
        });

        $('.input-field select', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new SelectBox($element); 
        });
        
        $('.fieldset', $scope).each(function() {
            
            var $element = $(this);
            var dont = $element.hasClass('dont-add-form-functionality');
            if (!dont) dont = ($element.closest('.dont-add-form-functionality').length);
            
            if (!dont) new Fieldset($element); 
        });
    
        $('#filter_form', $scope).each(function() {
            
            var $element = $(this);
            new Filter($element); 
        });
    
        $('#sorting_form', $scope).each(function() {
            
            var $element = $(this);
            new Sorting($element); 
        });
        
        
    
        for (var i=0, length = window.addToFormInit.functions.length; i<length; i++) {
            window.addToFormInit.functions[i]();   
        }   
    }
    
    
    
    
    
    // the input prefix highlighting
    function Prefix($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        
        var $prefix = me.$main.parent().prev('.input-prefix');
        
        if ($prefix.length) {
         
            me.$main.data('$prefix', $prefix);
            
            var onFocus = function() {
                var $field = $(this);
                var css_class = ($field.prop('readonly')) ? 'focus-readonly' : 'focus';
                $field.data('$prefix').addClass(css_class);
            }
            
            var onBlur = function() {
                var $field = $(this);
                $field.data('$prefix').removeClass('focus-readonly focus');
            }
            
            me.$main.focus(onFocus);
            me.$main.blur(onBlur);
        }
    }
    
    
    // toggle visibility functionality
    function ToggleVisibility($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        
        me.show = me.$main.attr('data-toggle-show');
        me.hide = me.$main.attr('data-toggle-hide');
        
        $(me.show).each(function() {
            
            var $element = $(this);
            if (!$element.hasClass('toggle-check')) $element = $('.toggle-check', $element);
            
            if ($element.length) {
                if ($element.val()) {
                    me.onClick();
                    return false;
                }
            }
        });
        
        me.$main.click(function() {me.onClick(); return false;});
    }
    
    ToggleVisibility.prototype.onClick = function() {
        
        var me = this.me;
        
        $(me.hide).removeClass('hidden').css('display', 'none');
        $(me.show).removeClass('hidden').css('display', '');
    }
    
    
    // toggle visibility depending on the status of a radio button group
    function RadioToggle($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        
        me.radio_name = me.$main.attr('data-radio-name');
        me.radio_indexes = me.$main.attr('data-radio-index').split(',');
        me.$radio = $('input[name="'+me.radio_name+'"]');
        
        me.$radio.change(function() {me.toggle();});
        
        me.toggle();
    }
    
    RadioToggle.prototype.toggle = function() {
     
        var me = this;
        
        var checked = -1;
        me.$radio.each(function(index) {
           
            var $this = $(this);
            
            if ($this.prop('checked')) {
                checked = index;
                return false;
            }
            
        });
        
        var display = 'none';
        for (var i=0, length=me.radio_indexes.length; i<length; i++) {
            if (me.radio_indexes[i] == checked) {
                display = '';
                break;
            }
        }
        
        me.$main.css('display', display);
        
    }
    
    
    // handles forms with a dynamic amount of entries
    function DynamicEntries($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.id = me.$main.attr('id');
        me.$empty = $('#'+me.id+'_empty .entry');
        me.$entries = $('.entry', me.$main);
        me.$total = $('#id_'+me.id+'-TOTAL_FORMS');
        
        me.buttons = [];
        
        me.total = me.$total.val();
        me.initial = $('#id_'+me.id+'-INITIAL_FORMS').val();
        me.min = $('#id_'+me.id+'-MIN_NUM_FORMS').val();
        me.max = $('#id_'+me.id+'-MAX_NUM_FORMS').val();
        
        if (!me.total) me.total = me.$entries.length;
        if (!me.initial) me.initial = 0;
        if (!me.min) me.min = 0;
        if (!me.max) me.max = 1000;
        
        $('input, select, textarea', me.$empty).prop('disabled', true);
        
        me.addButtons();
    }
    
    DynamicEntries.prototype.add = function() {
        
        var me = this.me;
        
        var $new = me.$empty.clone(true, true);
        $('input, select, textarea', $new).prop('disabled', false);
        
        me.$entries.last().after($new);
        
        me.$entries = $('.entry', me.$main);
        me.renumber();
        me.addButtons();
        
        initFormElementsFunctionality($new);
    }
    
    DynamicEntries.prototype.remove = function($button) {
     
        var me = this.me;
        
        var $entry = $button.closest('.entry');
        var $delete = $('.delete-entry input', $entry);
        $delete.prop('checked', true);
        $entry.addClass('deleted');
        
        //$entry.remove();
        //me.$entries = $('.entry', me.$main);
        //me.renumber();
        //me.addButtons();
    }
    
    DynamicEntries.prototype.addButtons = function() {
     
        var me = this.me;
        
        for (var i=0, length = me.buttons.length; i<length; i++) {
            me.buttons[i].remove();
        }
        
        me.buttons = [];
        
        me.$entries.each(function(index) {
           
            var $entry = $(this);
            var $button = $('<button class="dynamic-button fawesome button form fa-minus negative"></button>');
            $button.click(function() {me.remove($(this)); return false;});
            
            if (me.$entries.length > me.min) {
                $entry.append($button);
                me.buttons.push($button);
            }
            
        });
        
        if (me.$entries.length < me.max) { 
            var $button = $('<button class="dynamic-button fawesome button form fa-plus positive"></button>');
            $button.click(function() {me.add(); return false;});
            var $wrapper = $('<div class="add-button-wrapper"></div>');
            $wrapper.append($button);
            me.$main.append($wrapper);
            me.buttons.push($wrapper);
        }
        
    }
    
    DynamicEntries.prototype.renumber = function() {
     
        var me = this.me;
        
        me.$entries.each(function(index) {
            
            var $entry = $(this);
            
            $entry.find('input, select, textarea').each(function() {
                
                var $field = $(this);
                
                if ($field.attr("id")) {
                    $field.attr("id", $field.attr("id").replace(/-(\d+)-/, "-" + index + "-"));
                    $field.attr("id", $field.attr("id").replace(/-(__prefix__)-/, "-" + index + "-"));
                }
                
                if ($field.attr("name")) {
                    $field.attr("name", $field.attr("name").replace(/-(\d+)-/, "-" + index + "-"));
                    $field.attr("name", $field.attr("name").replace(/-(__prefix__)-/, "-" + index + "-"));
                }
            });
            
            $entry.find('label').each(function() {
                
                var $field = $(this);
                if ($field.attr("for")) {
                    $field.attr("for", $field.attr("for").replace(/-(\d+)-/, "-" + index + "-"));
                    $field.attr("for", $field.attr("for").replace(/-(__prefix__)-/, "-" + index + "-"));
                }
            });
            
        });
        
        me.$total.val(me.$entries.length);
        me.total = me.$entries.length;
    }
    
    
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
    
    function URLField($main) {

        var me = this;
        this.me = me;
        me.$main = $main;

        me.$main.on('change', function() {
            var value = me.$main.val();
            if (value && !value.match(/^https?:\/\//)) {
                me.$main.val('http://' + value);
            }
        })

        me.$main.data('URLField', me);
    }

    InputBox.prototype.checkHeight = function() {
     
        var me = this.me;
        
        me.$main.css('min-height', (me.$label.height() + me.padding) + 'px');
    }
    
    
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
    
    
    
    // styling and functionality of select boxes
    function SelectBox($main) {
        
        var me = this;
        this.me = me;
        
        // the top + bottom padding of a .select-option
        me.option_padding = 14;
        // the size of the top + bottom border of the .select-dropdown
        me.dropdown_border = 2;
        
        me.$main = $main;
        
        // making sure that there is an empty option at the beginning
        var $first_option = $('option', me.$main).first();
        var first_html = $first_option.html();
        $first_option.html('');
        var first_val = $first_option.attr('value');
        $first_option.html(first_html);
        if (first_val && first_val != "") {
            $first_option.before($('<option>--------</option>'));   
        }
        
        
        
        me.$body = $('#body');
        me.$window = $(window);
        
        me.disabled = me.$main.prop('disabled');
        me.readonly = me.$main.hasClass('readonly');
        me.autoload = me.$main.hasClass('autoload');
        me.multiple = me.$main.prop('multiple');
        me.required = me.$main.prop('required');
        
        if (me.autoload && me.multiple) {
            me.autoload_multiple = true;
            me.multiple = false;
            me.autoload_multiple_options = [];
        } else {
            me.autoload_multiple = false;
        }
        
        me.$main.parents('fieldset').each(function() {
            if ($(this).prop('disabled')) me.disabled = true;
        });
        
        if (me.autoload) {
            
            me.multiple = false;
            
            me.load_url = me.$main.attr('data-load-url');
            me.load_start = parseInt(me.$main.attr('data-load-start'));
            me.load_limit = parseInt(me.$main.attr('data-load-max'));
            if (!me.load_start) me.load_start = 2;
            if (me.load_start < 1) me.load_start = 1;
            if (!me.load_limit) me.load_limit = 20;
            
            me.loading = false;
            me.loading_value = '';
            me.loading_timeout = null;
            me.loading_cache = [];
            
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
        
  
        
        
        var disabled = (me.autoload) ? '' : ' disabled="disabled"';
        me.$wrapper = $('<div class="select-display-wrapper"></div>');
        me.$display = $('<input type="text" class="select-display"'+disabled+'/>');
        me.$dropdown_wrapper = $('<div class="select-dropdown-wrapper"></div>');
        me.$dropdown = $('<div class="select-dropdown" style="display:none;"></div>');
        
        me.$display.attr('placeholder', me.$main.attr('placeholder'));
        
        if (me.autoload_multiple) {
            me.$autoload_multiple = $('<div class="autoload-multiple"></div>');
            me.writeAutoloadMultipleValues();
        }
        
        if (me.autoload) {
            me.$main.prop('multiple', false);
        }
        
        
        if (!me.disabled && !me.readonly) {
            me.fillDropdown();
        }
        
        
        if (me.readonly || me.multiple) {
            var $options = $('option', me.$main);
            $options.each(function(index) {
                var $option = $(this);
                if ($option.prop('selected')) me.option_selected[index] = true;
                else me.option_selected[index] = false;
            });
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
            me.$dropdown_wrapper.addClass('autoload');
            me.$display.attr('autocomplete', 'nope');
            me.$display.attr('autocorrect', 'off');
            me.$display.attr('autocapitalize', 'off');
        }
        
        me.$main.addClass('select-hide');
        
        
        me.$wrapper.append(me.$display);
        me.$main.after(me.$wrapper);
        if (me.autoload_multiple) {
            me.$main.before(me.$autoload_multiple);
        }
        
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
            me.$main.keyup(function(e) {return me.onSelectKeyup(e);});
            me.$main.keydown(function(e) {return me.onSelectKeydown(e);});
            me.$display.keydown(function(e) {return me.onInputKeydown(e);});
            
            me.$display.keyup(function() {me.onInputChange();});   
            me.$display.blur(function() {me.onSelectBlur();});
        }
        
        
        me.$window.resize(function() {me.onResize();});
        
        
        me.$main.closest('form').submit(function() {me.onFormSubmit();});
        
        
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
                
            } else {
                
                me.writeAutoloadMultipleValues();
                me.toggleDropdown();
                
                if (me.autoload_multiple) {
                    me.$display.val('');
                }
                
            }
            
            return false;
        }
        
        return true;
    }
    
    /**
     * A key of a autoload select field got pressed.
     * Checking if the up key was pressed to switch the focus to the input field.
     */
    SelectBox.prototype.onSelectKeyup = function(event) {
        
        var me = this.me;
        
        if (me.autoload) {
         
            if (event.which == 38) {
            
                var $option = $('option', me.$main).first();
                if ($option.prop('selected')) {
                
                    event.stopPropagation();
                    event.preventDefault();
                
                    me.$display.val(me.loading_value);
                    me.$display.focus();
                    me.openDropdown();
                
                    return false;
                }
            }
        }
    }
    
    /**
     * A key of a autoload select field got pressed.
     * Checking if the down key was pressed to switch the focus to the input field.
     */
    SelectBox.prototype.onSelectKeydown = function(event) {
        
        var me = this.me;
        
        if (me.autoload) {
         
            if (event.which == 40) {
            
                var $options = $('option', me.$main);
                var $option = $options.last();
                if ($option.prop('selected')) {
                
                    $options.first().prop('selected', true);
                    
                    event.stopPropagation();
                    event.preventDefault();
                
                    me.$display.val(me.loading_value);
                    me.$display.focus();
                    me.openDropdown();
                
                    return false;
                }
            }
        }
    }
    
    /**
     * A key of a autoload input field got pressed.
     * Checking if the down or up key was pressed to switch the focus to the dropdown.
     */
    SelectBox.prototype.onInputKeydown = function(event) {
        
        var me = this.me;
        
        if (me.autoload && !me.loading) {
         
            if (event.which == 38 || event.which == 40) {
            
                event.stopPropagation();
                event.preventDefault();
                
                var $option = (event.which == 40) ? $($('option', me.$main).get(1)) : $('option', me.$main).last();
                $option.prop('selected', true);
                me.onSelectChange();
                me.$main.focus();
                
                return false;
            }
        }
        
        
        if (event.which == 13) {
            
            event.stopPropagation();
            event.preventDefault();
            
            return false;
        }
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
            var text = ($option.attr('data-display')) ? $option.attr('data-display') : $option.text();
            var $element = $('<div class="select-option select-index-'+index+multiple+'">'+text+'</div>');
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
        if (typeof dropdown_display == "undefined") dropdown_display = "none";
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
     * and scrolls the dropdown so that the option is visible in the dropdown.
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
            
            if ($display_option) {
                $display_option.addClass('focus');
                
                // make sure the focused option is visible in the dropdown
                var dropdown_height = me.$dropdown.height();
                var scroll_top = me.$dropdown.scrollTop();
                var option_height = $display_option.height() + me.option_padding;
                var option_position = $display_option.position();
                
                if (option_position) {
                    var option_top = $display_option.position().top;
                    
                    if (option_top + option_height > dropdown_height) {
                        scroll_top =  option_top - dropdown_height + option_height + scroll_top;
                    } else if (option_top < 0) {
                        scroll_top += option_top;
                    }
                    
                    if ($display_option.css('display') != 'none') me.$dropdown.scrollTop(scroll_top);
                    
                    me.option_focused = me.option_focus;
                }
            }
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
          
        me.writeAutoloadMultipleValues();
        
        var $options = $('option', me.$main)
        
        var $first_option = $options.first();
        var first_html = $first_option.html();
        $first_option.html('');
        
        if (me.autoload) {
            var first_val = $first_option.attr('value');
            if (!first_val) {
                $first_option.attr('value', '');
                $first_option.val('');            
            }
            
            // input field is empty -> unselect everything
            if (!me.autoload_multiple && me.$display.val() == "") {
                $options.prop('selected', false);
            }
        }
        
        // unselecting a possible selected empty first option
        var first_val = $first_option.attr('value');
        $first_option.html(first_html);
        if (!(first_val && first_val != "") && $first_option.prop('selected')) {
            $first_option.prop('selected', false);
        }
        
        
        me.loading_value = "";
        me.$dropdown.css('display', 'none');
        me.$main.trigger('closed');
    }
    
    /**
     * The form gets submited
     */
    SelectBox.prototype.onFormSubmit = function() {
     
        var me = this;
        
        if (me.closing_dropdown) {
            clearTimeout(me.closing_dropdown);
            me.closing_dropdown = null;
        }
        
        me.closeDropdown();
        me.setAutoloadMultipleValues();
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
            
            //console.log(options);
            
            me.loading_cache[me.loading_value] = options;
            
            me.$main.html('');
            
            var lines = options.split("\n");
            var has_entry = false;
            var value = false;
            for (var i=0, length=lines.length; i<length; i++) {
                var entry = lines[i].split("|");   
                
                if (entry[0].length >= 1) {
                    if (entry.length == 1) entry[1] = entry[0];
                    
                    if (me.autoload_multiple) {
                        for (var o=0, o_length=me.autoload_multiple_options.length; o<o_length; o++) {
                            var $option = me.autoload_multiple_options[o];
                            if (entry[1] == $option.attr('value')) break;
                        }
                        if (o < o_length) continue;
                    }
                    
                    var display = entry[0];
                    if (entry[2]) display += "<br>" + entry[2];
                    var $option = $('<option>'+entry[0]+'</option>');
                    $option.attr('value', entry[1]);
                    $option.attr('data-display', display);
                    me.$main.append($option);
                    
                    if (entry[0] == me.loading_value) value = entry[1];
                    has_entry = true;
                }
            }
            
            if (has_entry) {
                if (value === false) me.$main.prepend($('<option>'+me.loading_value+'</option>'));
                else me.$main.prepend($('<option value="'+value+'">'+me.loading_value+'</option>'));
            }
            
            me.fillDropdown();
            
            if (has_entry) {
                //me.$main.focus();
                me.openDropdown();
            }
            
            
            me.$display.val(me.loading_value);
            //me.$display.focus();
            
            me.loading = false;
            me.$wrapper.removeClass('loading spin');
            
        }
        
        var onError = function() {
            
            console.log('error');
            
            me.loading = false;
            me.$wrapper.removeClass('loading spin');
        }
        
        var load = function() {
            
            window.clearTimeout(me.loading_timeout);
            me.loading_timeout = null;
            
            me.loading = true;
            
            me.closeDropdown();
            me.loading_value = value;
            
            if (typeof me.loading_cache[value] != "undefined") {
                
                onSuccess(me.loading_cache[value]);
                
            } else {
            
                me.$wrapper.addClass('loading');
                setTimeout(function() {me.$wrapper.addClass('spin');}, 10);
            
                $.ajax({
                    type: "GET", 
                    url: me.load_url, 
                    data: { 
                        q:value, 
                        limit:me.load_limit, 
                        cache:Math.round(Math.random()*1000000) 
                    }, 
                    cache: false, 
                    async: true
                    
                }).done(function(options) {onSuccess(options);}).fail(function() {onError();});
                
            }
            
        }
        
        
        
        if (me.loading) {
            me.$display.get(0).value = me.loading_value;
        }
        
        var value = me.$display.get(0).value;
        if (value.length >= me.load_start && !me.loading) {    
            
            if (me.loading_value == value) return;
                
            if (me.loading_timeout) {
                window.clearTimeout(me.loading_timeout);   
            }
            
            me.loading_timeout = window.setTimeout(function() {load();}, 800);
        }
    }
    
    /**
     * Writes the selected values of a multiple autoload field above the select box.
     */
    SelectBox.prototype.writeAutoloadMultipleValues = function() {
     
        var me = this.me;
        
        if (!me.autoload_multiple) return;
        
        me.$autoload_multiple.html('');
        
        var $options = $('option', me.$main);
        $options.each(function(index) {
            var $option = $(this);
            
            if (index == 0) {
                var html = $option.html();
                $option.html('');
                var value = $option.attr('value');
                $option.html(html);
                if (!value) return true;
            }
            
            if ($option.prop('selected')) {
                
                for (var o=0, length=me.autoload_multiple_options.length; o<length; o++) {
                    if (me.autoload_multiple_options[o].attr('value') == $option.attr('value')) break;
                }
                if (o == length) me.autoload_multiple_options.push($option);
                
                $option.detach();
            }
        });
        
        for (var i=0, length=me.autoload_multiple_options.length; i<length; i++) {
         
            var $option = me.autoload_multiple_options[i];
            
            var $link = $('<a href="javascript:void(0);" data-index="'+i+'" class="fawesome">'+$option.html()+'</a>');
            $link.click(function() {me.removeAutoloadMultipleValue($(this));});
            me.$autoload_multiple.append($link);
        }
        
        //me.$display.val('');
    }
    
    /**
     * Removes an item of a multiple autoload field from the list of selected items.
     * 
     * @param   $link   the jQuery object of the link representing the item
     */
    SelectBox.prototype.removeAutoloadMultipleValue = function($link) {
     
        var me = this.me;
        
        var index = $link.attr('data-index');
        
        me.autoload_multiple_options.splice(index, 1);
        
        me.writeAutoloadMultipleValues();
    }
    
    /**
     * Sets the selected values in the actual select box.
     */
    SelectBox.prototype.setAutoloadMultipleValues = function() {
     
        var me = this.me;
        
        if (!me.autoload_multiple) return;
        
        me.writeAutoloadMultipleValues(); 
        me.$main.prop('multiple', true);
        
        for (var i=0, length=me.autoload_multiple_options.length; i<length; i++) {
            var $option = me.autoload_multiple_options[i];
            $option.prop('selected');
            me.$main.append($option);
        };
    }
    
    
    
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
    
    /**
     * Initialises the fieldset.
     * Checks if the fieldset wrapper has the attribute 'data-edit-url' for loading the editable content into an iframe.
     * Also checks for .edit-links inside the fieldset which are used to load editable content into an iframe.
     *
     * Creates a connection between the Fieldset class inside an iframe and the Fieldset class which created the iframe.
     */
    Fieldset.prototype.init = function() {
     
        var me = this.me;
        
        me.$fieldset = $('fieldset', me.$main);
        me.$files = $('.input-field input[type="file"]', me.$fieldset);
        me.$selects = $('.input-field select', me.$fieldset);
        me.$collapse_selects = $('.row.collapse > * select', me.$fieldset);
        me.$textareas = $('.input-field textarea', me.$fieldset);
        
        me.iframe_buttons = $('.edit-link', me.$main);
        me.iframe_buttons.click(function() {return me.onOpenIFrame($(this));});
        
        me.iframe_id = -1;
        me.has_main_iframe = false;
        me.parent = window.frameElement;
        
        if (me.parent) {
            // creating a possible connection between an iframe and its parent
            var id = me.parent.id.split("-")[1];
            if (window.parent.iframe_fieldset) {
                me.parent = window.parent.iframe_fieldset[id];
                me.parent.child = me;
                window.setInterval(function() {me.checkHeight();}, 100);
            } else me.parent = null;
        }
        
        
        if (me.parent && me.$fieldset.prop('disabled')) {
            // the fieldset is in an iframe and is not editable which means it is a new markup for the parent
            
            me.parent.replaceMainMarkup(me.$main.html());
            
        } else {
                
            if (me.$main.hasClass('editable')) me.editable();
            
        }
    }
    
    /**
     * Does the necessary stuff for editable fieldsets.
     * Creates the iframe if the fieldset wrapper has the 'data-edit-url' attribute.
     * Also creates the edit button for switching between editing and not editing view.
     */
    Fieldset.prototype.editable = function() {
        
        var me = this.me;
        
        var button = 'close';
        if (me.$fieldset.prop('disabled')) {
            button = 'edit';
            me.$main.addClass('disabled');
        }
        
        
        // the toggle is done by loading the editable content
        // into an iframe, not by switching style classes
        if (me.$main.attr('data-edit-url')) {
            me.has_main_iframe = true;
            me.createIFrame(me.$main.attr('data-edit-url'));
        }
        
        me.edit_button = $('<button class="edit-button button fawesome fa-'+button+' smaller primary"><span class="sr-only">'+trans[button]+'</span></button>');
        me.edit_button.click(function(e) {me.toggle(); return false;});
        $('.cancel', me.$main).click(function(e) {me.toggle(true); return false;});
        
        
        if (me.$main.hasClass('switch')) me.$main.prepend(me.edit_button);
        
        me.onResize();
    }
    
    /**
     * Creates an iframe with editable content.
     *
     * @param   url     the src of the iframe
     */
    Fieldset.prototype.createIFrame = function(url) {
        
        var me = this.me;
            
        if (me.$iframe) {
            me.$iframe.remove();
            window.iframe_fieldset[me.iframe_id] = null;
        }
        
        me.iframe_id = Fieldset.iframe_counter;
        Fieldset.iframe_counter++;
        
        me.child = null;
        me.$iframe = $('<iframe src="'+url+'" class="iframe-edit" id="fieldset-'+me.iframe_id+'" frameborder="0" scrolling="no"></iframe>');
        me.$main.after(me.$iframe);   
        
        if (!window.iframe_fieldset) window.iframe_fieldset = [];
        window.iframe_fieldset[me.iframe_id] = me;
    }
    
    /**
     * A link got clicked which is supposed to open an iframe with editable content.
     * The links are marked with the class 'edit-link'.
     * The link has to have the src of the iframe in the attribute 'data-edit-url'.
     * Works only if the fieldset wrapper itself doesn't have an attribute 'data-edit-url' for a main iframe.
     */
    Fieldset.prototype.onOpenIFrame = function($link) {
     
        var me = this.me;
        
        var url = $link.attr('data-edit-url');
        if (!url) return true;
        
        me.createIFrame(url);
        
        me.$iframe.css('display', 'block');
        me.$main.css('display', 'none');
        
        var interval = window.setInterval(function() {
            if (me.child) {
                window.clearInterval(interval);
                me.child.sizeParentIFrame();
            }
        }, 100);
        
        return false;
    }
    
    /**
     * Switches the edit view on/off.
     * 
     * param    disable         true for "off" otherwise "on"
     * param    iframe_call     the call came from the child iframe
     */
    Fieldset.prototype.toggle = function(disable, iframe_call) {
        
        var me = this;
        
        // you are in an iframe
        // let the parent do the work
        if (me.parent) {
            me.parent.toggle(true, true);
            return;
        }
            
        // your editable content is in an iframe
        // toggle display of iframe and its parent
        if (me.has_main_iframe || iframe_call) {
            
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
    
    /**
     * Checks if the height of the window changed.
     * Calls onResize().
     */
    Fieldset.prototype.checkHeight = function() {
     
        var me = this.me;
        
        if (me.height != me.$body.height()) {
            me.height = me.$body.height();
            me.onResize();
        }
    }
    
    /**
     * Sets the height of the iframe.
     */
    Fieldset.prototype.sizeIFrame = function(height) {
        
        var me = this.me;
        
        if (!me.$iframe) return;
        
        me.$iframe.height(height);
    }
    
    /**
     * If the fieldset is the iframe, calls parent.sizeIFrame().
     */
    Fieldset.prototype.sizeParentIFrame = function() {
     
        var me = this.me;
        
        if (me.parent) {
            me.parent.sizeIFrame(me.$body.height());
        }   
    }
    
    /**
     * A child iframe safed its data successfuly and sends the new markup for the parent fieldset.
     */
    Fieldset.prototype.replaceMainMarkup = function(markup) {
     
        var me = this.me;
        
        me.$main.html(markup);
        me.init();
        me.toggle(true, true);
    }
    
    /**
     * Collapses columns in disabled view if so defined.
     */
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
    
    /**
     * Resets the style if necessary at a resize of the window.
     */
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
    
    function Filter($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$submit = $('#submit-id-submit', me.$main);
        me.$links = $('a', me.$main);
        me.$checks = $('input[type="checkbox"]', me.$main);
        
        me.init();
    }
    
    Filter.prototype.init = function() {
     
        var me = this;
        
        me.$submit.css('display', 'none');
        
        me.$checks.change(function() {me.onCheck();});
        me.$links.click(function(e) {me.onClick(e, $(this));});
    }
    
    Filter.prototype.onCheck = function() {
        
        var me = this;
        
        me.$submit.click();
    }
    
    Filter.prototype.onClick = function(event, $link) {
        
        event.preventDefault();
        
        var me = this;
        
        var value = $link.attr('data-value');
        var $li = $link.closest('li.accordion-inside');
        var name = $li.attr('id');
        
        var $input = $('input', $li);
        $input.val(value);
        
        me.$submit.click();
        
        return false;
    }
    
    function Sorting($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$submit = $('button', me.$main);
        me.$select = $('select', me.$main);
        
        me.value = me.$select.val();
        
        me.init();
    }
    
    Sorting.prototype.init = function() {
     
        var me = this;
        
        me.$submit.css('display', 'none');
        me.$select.on('closed', function() {me.onChange();});
    }
    
    Sorting.prototype.onChange = function() {
     
        var me = this;
        
        var value = me.$select.val();
        
        if (value != me.value) {
            me.$submit.click();
        }
    }
    
    function EditIframe($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.id = me.$main.attr('id');
        me.$wrapper = $('.'+me.id);
        me.iframe_id = -1;
        me.$window = $(window);
        me.width = -1;
        
        $(window).resize(function() {me.onResize();});
        
        me.init();
    }
    
    EditIframe.prototype.init = function() {
     
        var me = this;
        
        me.$wrapper.each(function() {
           
            var $this = $(this);
            var url = $this.attr('data-edit-url');
            
            if (url) {
                
                $this.addClass('editable');
                $this.off().click(function() {me.onEdit(url);});
                
            } else {
                
                $('*[data-edit-url]', $this).each(function() {
                    var $link = $(this);
                    var url = $link.attr('data-edit-url');
                    if (url) {
                        $this.addClass('editable');
                        $link.click(function() {me.onEdit(url);});
                    }
                });
                
            }
        });
        
    }
    
    EditIframe.prototype.onEdit = function(url) {
                    
        var me = this;
        
        if (me.$iframe) {
            me.$iframe.remove();
            me.child = null;
            window.iframe_fieldset[me.iframe_id] = null;
        }
        
        me.iframe_id = Fieldset.iframe_counter;
        Fieldset.iframe_counter++;
        
        me.$iframe = $('<iframe src="'+url+'" class="iframe-edit" id="fieldset-'+me.iframe_id+'" frameborder="0" scrolling="no"></iframe>');
        me.$main.append(me.$iframe);   
        
        if (!window.iframe_fieldset) window.iframe_fieldset = [];
        window.iframe_fieldset[me.iframe_id] = me;
        
        me.toggle();
    }
    
    EditIframe.prototype.toggle = function(disable) {
        
        var me = this;
            
        if (me.$iframe) {
            if (disable) {
                me.$iframe.css('display', '');
            } else {
                me.$iframe.css('display', 'block');
                window.setTimeout(function() {me.sizeChild();}, 50);
            }
        }
    }
    
    EditIframe.prototype.sizeChild = function() {
     
        var me = this;
        
        if (me.child) {
            me.child.sizeParentIFrame();
        } else {
            window.setTimeout(function() {me.sizeChild();}, 50);
        }
    }
    
    EditIframe.prototype.sizeIFrame = function(height) {
        
        var me = this.me;
        
        if (me.$iframe) {
            me.$iframe.height(height);
        }
    }
    
    EditIframe.prototype.replaceMainMarkup = function(markup) {
        
        var me = this.me;
        
        var $html = $(markup);
        var $replacements = $('.replace', $html);
        
        $replacements.each(function() {
            
            var $replacement = $(this);
            var id = $replacement.attr('id');
            
            $('#'+id, me.$wrapper).each(function() {
            
                var $old = $(this);
                $old.after($replacement);
                $old.remove();
            
            });
        });
        
        me.init();
        me.toggle(true);
    }
    
    EditIframe.prototype.onResize = function() {
     
        var me = this.me;
        
        if (me.width == me.$window.width()) return;
        me.width = me.$window.width();
        
        if (me.$iframe) {
            me.$iframe.css('width', '');
            me.$iframe.width(me.$iframe.width() - 10);
        }
    }
    
    $('.edit-iframe').each(function() {
        
        var $element = $(this);
        new EditIframe($element); 
    });
    
    
    initFormElementsFunctionality();
});

