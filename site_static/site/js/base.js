/**
 * Base functionality of the page.
 *
 * @author Daniel Lehmann
 */

$(document).ready(function() {
    
    
    
    var current_width_sniffer = 'is-nothing';
    var widthSniffer = function() {
       
        var new_width_sniffer = false;
        $('.width-sniffer').each(function() {
            
            var $this = $(this);
            if ($this.css('display') == 'block') {
                
                if ($this.hasClass('visible-xs')) {
                    new_width_sniffer = 'is-xs';
                } else if ($this.hasClass('visible-sm')) {
                    new_width_sniffer = 'is-sm';
                } else if ($this.hasClass('visible-md')) {
                    new_width_sniffer = 'is-md';
                } else if ($this.hasClass('visible-lg')) {
                    new_width_sniffer = 'is-lg';
                }
                
                return false;
            }
        }); 
        
        if (new_width_sniffer && new_width_sniffer != current_width_sniffer) {
            var $body = $('body').removeClass(current_width_sniffer);
            current_width_sniffer = new_width_sniffer; 
            $body.addClass(new_width_sniffer);
        }        
    }
    $(window).resize(widthSniffer);
    widthSniffer();
    
    
    
    
    
    function Tooltip($element) {
     
        var me = this;
        this.me = me;
        
        me.$element = $element;
        me.$body = $('body');
        
        if (!Tooltip.$tooltip) {
            Tooltip.$tooltip = $('<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-content"></div></div>');
            me.$body.append(Tooltip.$tooltip);
        }
        
        me.$element.mouseenter(function() {me.show();})
        me.$element.mouseleave(function() {me.hide();})
    }
    
    Tooltip.$tooltip = null;
    
    Tooltip.prototype.show = function() {
        
        var me = this.me;
        var $element = me.$element;
        var $tooltip = Tooltip.$tooltip;
        var $content = $('.tooltip-content', $tooltip);
        var $arrow = $('.tooltip-arrow', $tooltip);
        
        $content.html(me.$element.attr('data-tooltip'));
        
        $tooltip.removeClass('top').removeClass('bottom').removeClass('left').removeClass('right');
        $tooltip.css('visibility', 'hidden');
        $tooltip.css('display', 'block');
        
        var offset = $element.offset();
        var top = offset.top - $tooltip.height() - 5;
        var left = Math.round(offset.left + ($element.width() / 2) - ($tooltip.width() / 2));
        var position = "top";
        
        if (top < me.$body.scrollTop() + 5) {
            top = offset.top + $element.height() + 5;
            position = "bottom";
        }
        
        $arrow.css('left', '50%');
        var tooltip_width = $tooltip.width();
        var window_width = $(window).width();
        var original_left = left;
        
        if (left < 0) {
            var left_offset = original_left * (-1) + 5;
            left = 5;
            var middle = (tooltip_width / 2) - left_offset;
            $arrow.css('left', (middle / tooltip_width * 100) + "%");
        } else if (left + tooltip_width + 5 > window_width) {
            var left_offset = original_left - (window_width - tooltip_width - 5);
            left = window_width - tooltip_width - 5;
            var middle = (tooltip_width / 2) + left_offset;
            $arrow.css('left', (middle / tooltip_width * 100) + "%");
        }
        
        $tooltip.css('top', top+'px');
        $tooltip.css('left', left+'px');
        $tooltip.addClass(position);
        
        
        var top = offset.top - $tooltip.height() - 5;
        var position = "top";
        
        if (top < me.$body.scrollTop() + 5) {
            top = offset.top + $element.height() + 5;
            position = "bottom";
        }
        
        $tooltip.css('top', top+'px');
        $tooltip.addClass(position);
        
        
        $tooltip.css('visibility', 'visible');
    }
    
    Tooltip.prototype.hide = function() {
        
        var me = this.me;
        var $tooltip = Tooltip.$tooltip;
        
        $('.tooltip-content', $tooltip).html('');
        
        $tooltip.css('display', 'none');
    }
    
    $('*[data-tooltip]').each(function() {
        new Tooltip($(this)); 
    });
    
    
    
    function Search($main) {
     
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$button = $('.search', me.$main);
        me.$layer = $('#search-layer');
        me.$search = $('.search', me.$layer);
        me.$close = $('.close', me.$layer);
        me.$input = $('input', me.$layer);
        me.$body = $('body');
        me.$window = $(window);
        
        me.is_open = false;
        
        me.$button.click(function() {me.is_open = true; me.open();});
        me.$window.resize(function() {me.open();});
    }
    
    Search.prototype.open = function() {
        
        var me = this.me;
        if (!me.is_open) return;
        
        me.close();
       
        me.$layer.css('top', me.$window.scrollTop() + 'px');
        me.$body.addClass('show-layer');
        
        me.$search.off().click(function() {me.search();});
        me.$close.off().click(function() {me.close();});
        me.$input.keypress(function(e) {
            if(e.which == 13) {
                me.search();
            }
        });
        
        me.is_open = true;
    }
    
    Search.prototype.close = function() {
        
        var me = this.me;
        
        me.$body.removeClass('show-layer');
        
        me.is_open = false;
    }
    
    Search.prototype.search = function() {
        
        var me = this.me;
        
        alert('implement search action in base.js');
        
    }
    
    $('.header-search').each(function() {
        new Search($(this)); 
    });
    
    
    
    
    function BodyClassButton($button) {
        
        var me = this;
        this.me = me;
        
        me.$button = $button;
        me.$body = $('body');
        me.my_class = me.$button.attr('data-body-class');
        me.my_group = me.$button.attr('data-body-class-group');
        me.toggle = me.$button.attr('data-body-class-toggle');
        
        if (me.my_group) {
            if (typeof BodyClassButton.classes[me.my_group] == "undefined") BodyClassButton.classes[me.my_group] = [];
            BodyClassButton.classes[me.my_group].push({'my_class':me.my_class, '$button': me.$button});
        } else {
            if (typeof BodyClassButton.classes['body-classes'] == "undefined") BodyClassButton.classes['body-classes'] = [];
            BodyClassButton.classes['body-classes'].push({'my_class':me.my_class, '$button': me.$button});
        }
        
        me.$button.click(function() {me.click();});
    }
    
    BodyClassButton.classes = [];
    
    BodyClassButton.prototype.click = function() {
        
        var me = this.me;
        
        var classes = (me.my_group) ? BodyClassButton.classes[me.my_group] : BodyClassButton.classes['body-classes'];
        var has_class = me.$body.hasClass(me.my_class);
        
        for (var i=0, length=classes.length; i<length; i++) {
            me.$body.removeClass(classes[i].my_class);
            classes[i].$button.removeClass('active');
        }
        
        if (me.toggle) {
            if (!has_class) {
                me.$body.addClass(me.my_class);
                me.$button.addClass('active');
            }
        } else {
            me.$body.addClass(me.my_class);
            me.$button.addClass('active');
        }
    }
    
    $('*[data-body-class]').each(function() {
        new BodyClassButton($(this)); 
    });
    
    
    
    
    function Header($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$image = $('img', me.$main);
        me.$menu = $('.menu', me.$main);
        me.$nav = $('nav', me.$menu);
        me.$list = $('ul', me.$nav);
        me.$lists = $('li', me.$nav);
        me.$window = $(window);
        me.$body = $('body');
        
        me.$prev = null;
        me.$next = null;
        me.left_nav = 0;
        
        if (me.$image.length) me.$main.addClass('has-image');
        
        me.$image.load(function() {me.styleImage();});
        me.$window.resize(function() {me.onResize();});
        me.$window.scroll(function() {me.checkFixedPosition();});
        me.onResize();
    }
    
    Header.prototype.styleImage = function() {
        
        var me = this.me;
        
        if (!me.$image.length) return;
        
        me.$main.css('height', '');
        
        if (!me.$body.hasClass('is-xs')) {
            me.$main.height(me.$image.height());
            me.$image.css('margin-top', '-' + Math.round(me.$image.height()/2) + 'px');
        }
        
        me.checkFixedPosition();
    }
    
    Header.prototype.styleNavi = function() {
        
        var me = this.me;
        
        if (!me.$nav.length) return;
        
        me.$list.css('width', '');
        me.$lists.css('left', '');
        
        var left = 0;
        me.$lists.each(function() {
            
            var $list = $(this);
            
            var width = $list.width();
            $list.data('left', left);
            $list.data('width', width);
            left += width + 60;
            
        });
        
        me.$list.width(left);
        
        me.$lists.each(function() {
            
            var $list = $(this);
           
            $list.css('left', $list.data('left') + 'px');
        });
        
        if (!me.$prev) {
            
            me.$prev = $('<div class="fawesome left prev disabled"><span class="sr-only">previous</span></div>');
            me.$next = $('<div class="fawesome right next disabled"><span class="sr-only">next</span></div>');
            
            me.$nav.after(me.$prev);
            me.$nav.after(me.$next);
            
            me.$prev.click(function() {me.prev();});
            me.$next.click(function() {me.next();});
            
            me.$nav.on("swiperight", function() {me.prev();});
            me.$nav.on("swipeleft", function() {me.next();});
        }
        
        var nav_pos = me.$nav.offset();
        
        if (nav_pos.left + me.$nav.width() + 25 > me.$window.width()) {
            me.$next.addClass('squeezed');   
        } else {
            me.$next.removeClass('squeezed');
        }
        
        var $left_nav = $(me.$lists.get(me.left_nav));
        me.$list.css('left', '-' + $left_nav.data('left') + 'px');
        
        me.checkNextPrev();
    }
    
    Header.prototype.checkNextPrev = function() {
        
        var me = this.me;
        
        var nav_width = me.$nav.width();
        
        if (nav_width >= me.$list.width()) {
            
            me.$prev.addClass('disabled');  
            me.$next.addClass('disabled');   
            
        } else {
            
            me.$prev.removeClass('disabled');  
            me.$next.removeClass('disabled');   
            
            if (me.left_nav == 0) {
                me.$prev.addClass('disabled');
            }
            
            var $left_nav = $(me.$lists.get(me.left_nav));
            var $right_nav = $(me.$lists.get(me.$lists.length - 1));
            var width = $right_nav.data('left') + $right_nav.width() - $left_nav.data('left');
            if (nav_width >= width) {
                me.$next.addClass('disabled');
            }
            
        }
    }
    
    Header.prototype.next = function() {
     
        var me = this.me;
            
        var $left_nav = $(me.$lists.get(me.left_nav));
        var $right_nav = $(me.$lists.get(me.$lists.length - 1));
        var width = $right_nav.data('left') + $right_nav.width() - $left_nav.data('left');
        if (me.$nav.width() < width) {
            me.left_nav++;
            me.styleNavi();
        }   
    }
    
    Header.prototype.prev = function() {
     
        var me = this.me;
        
        if (me.left_nav > 0) {
            me.left_nav--;   
            me.styleNavi();
        }
    }
        
    Header.prototype.checkFixedPosition = function() {
        
        var me = this.me;
        
        if (!me.$menu.length) return;
        
        var height = me.$main.height() + me.$main.offset().top + parseInt(me.$main.css('padding-bottom'));
        
        if (me.$body.hasClass('is-xs')) {
            height -= 40;
            height -= 70;
        } else {
            height -= 56;
            height -= 114;
        }
        
        if (me.$window.scrollTop() >= height) {
            me.$main.addClass('fixed');   
        } else {
            me.$main.removeClass('fixed');
        }
    }
    
    Header.prototype.onResize = function() {
        
        var me = this.me;
        
        me.styleImage();
        me.styleNavi();
        me.checkFixedPosition();
    }
    
    $('.header').each(function() {
        new Header($(this)); 
    });
    
    
    
    
    /*
    function lazyload_images() {
        $(".img img:in-viewport").lazyload({
            load : function(element, el_left, settings){
                $(this).closest('.img').addClass('loaded');
            }
        });
    }
    $(window).bind('scrollstop smartresize', lazyload_images);
    */
    
});