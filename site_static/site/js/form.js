/**
 * Handles form functionality and styling.
 *
 * @author Daniel Lehmann
 */

$(document).ready(function() {
    
    
    // the input prefix highlighting
    $('.input-field input[type="text"]').each(function() {
        
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
    $('.input-field textarea').each(function() {
        
        var $field = $(this);
        
        var onChange = function($field, delay) {
            
            if (typeof delay != "undefined") {
                setTimeout(function() {var $me=$field; onChange($me);}, delay);
            }
            
            $field.css('height', '');
            $field.height($field.get(0).scrollHeight - 30);            
        }
        
        $field.change(function() {onChange($(this));});
        $field.on('cut paste drop keydown', function() {onChange($(this), 0);});
        
        onChange($field);
        onChange($field, 100);
    });
    
    $(window).resize(function() {
        $('.input-field textarea').each(function() {
            var $field = $(this);
            $field.css('height', '');
            $field.height($field.get(0).scrollHeight - 30); 
        });
    });
    
});