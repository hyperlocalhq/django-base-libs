/**
 * Handles the sorting order of the Leadership, Authorship and Involvement fields in the form frontend.
 * The class assumes that the form is build with crispy forms (naming of the elements is important).
 * The order field has to be set to be a hidden field.
 * A change in the height of the wrapper has to indicate that an element got removed or added.
 *
 * @author Daniel Lehmann
 */

 
/**
 * The constructor.
 * E.g.: new SortingByOrder('leaderships', 'leadership', 'sort_order');
 *
 * @param   wrapper_id      the id of the wrapper element for all the formsets of the to be ordered category
 * @param   formset_class   the class of all formsets which wrap one item of the to be ordered category
 * @param   order_field     the name of the database order field
 */
function SortingByOrder(wrapper_id, formset_class, order_field) {
    
    if (!SortingByOrder.prototype.interval) {
        SortingByOrder.prototype.interval = window.setInterval(SortingByOrder.prototype.onInterval, 200);
    }
    
    var me = this;
    me.$wrapper = $('#'+wrapper_id);
    me.formset_class = formset_class;
    me.order_field = order_field;
    
    me.wrapper_height = me.$wrapper.height();
    me.dont_order = false;
    
    me.$current_position = null;
    me.$current_drag = null;
    me.current_drag = null;
    me.drag_position = null;
    me.drop_zones = null;
    
    $(document).ready(function() {me.setOrder();});
    $('body').mousemove(function(event) {me.onMouseMove(event);}).mouseup(function(event) {me.onMouseUp(event);});
    
    SortingByOrder.prototype.instances.push(me);
}


/**
 * Static function and variables which are checking all instances of the class
 * for removed or new elements and trigger the reordering.
 */
SortingByOrder.prototype.instances = [];
SortingByOrder.prototype.interval = null;
SortingByOrder.prototype.onInterval = function() {
    
    for (var i=0, length=SortingByOrder.prototype.instances.length; i<length; i++) {
    
        var instance = SortingByOrder.prototype.instances[i];
        var height = instance.$wrapper.height();
        if (height == instance.wrapper_height) continue;
        
        instance.wrapper_height = height;
        instance.setOrder();
    }
}


/**
 * Fills the order fields with the current order numbers.
 */
SortingByOrder.prototype.setOrder = function() {
    
    var me = this;
    
    if (me.dont_order) return;
    
    
    var counter = 0;
    var $formsets = $('.'+me.formset_class, me.$wrapper);
    
    $formsets.each(function() {
        
        var $formset = $(this);
        if ($formset.css('display') == 'none') return true;
        
        $formset.off('mousedown');
        $formset.mousedown(function(event) {me.onMouseDown(event);});
        
        $('.form_hidden', $formset).each(function() {
           
            var $hidden = $(this);
            var id = $hidden.attr('id');
            var split = id.split('-');
            if (split.pop() == me.order_field) {
                $hidden.attr('value', counter);
                counter++;
                return false;
            }
            
        }); 
    });
    
    $formsets.addClass('dragable').removeClass('draging');
}

SortingByOrder.prototype.onMouseDown = function(event) {
    
    var me = this;
    
    if (event.target.tagName.toLowerCase() == "input") {
        me.current_drag = null;
        me.drag_position = null;
        $('body').removeClass('dragzone');
        me.dont_order = false;
        return;
    }
    
    me.current_drag = event.delegateTarget;
    me.drag_position = [event.pageX, event.pageY];
}

SortingByOrder.prototype.onMouseUp = function(event) {
    
    var me = this;
    
    me.current_drag = null;
    me.drag_position = null;
    $('body').removeClass('dragzone');
    me.dont_order = false;
    
    if (!me.$current_drag) return;
    
    
    var $drop = $(event.target);
    if ($drop.hasClass('dropzone')) {
        $drop.after(me.$current_drag);
        me.setOrder();
    } else {
        me.$current_position.after(me.$current_drag);
    }
    
    $('.dropzone', me.$wrapper).remove();
    me.$current_position.remove();
    
    me.$current_drag = null;
    me.$current_position = null;
    
    var $formsets = $('.'+me.formset_class, me.$wrapper);
    $formsets.addClass('dragable').removeClass('draging');
    
}

SortingByOrder.prototype.onMouseMove = function(event) {
    
    var me = this;
    
    if (!me.current_drag || me.$current_drag) return;
    if (Math.sqrt(Math.pow(event.pageX - me.drag_position[0], 2) + Math.pow(event.pageY - me.drag_position[1], 2)) < 5) return;
    
    me.dont_order = true;
    
    me.$current_drag = $(me.current_drag);
    me.$current_position = $('<div style="visibility:hidden; height:1px;"></div>');
    me.$current_drag.after(me.$current_position);
    me.$current_drag.detach();
    
    $('body').addClass('dragzone');
    
    var $formsets = $('.'+me.formset_class, me.$wrapper);
    var $formset = null;
    $formsets.each(function() {
        
        $formset = $(this);
        if ($formset.css('display') == 'none') return true;
        
        $formset.before('<div class="dropzone">DROPZONE</div>');
    });
    if ($formset) {
        $formset.after('<div class="dropzone">DROPZONE</div>');
    }
    
    $formsets.removeClass('dragable').addClass('draging');
    
    
    var top = me.$current_position.offset().top;
    var height = $(window).height();
    
    $(window).scrollTop(top-Math.round(height/2));
}


