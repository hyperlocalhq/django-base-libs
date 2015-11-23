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
        me.$button = $('.fa-search', me.$main);
        me.$layer = $('#search-layer');
        me.$search = $('.fa-search', me.$layer);
        me.$close = $('.fa-close', me.$layer);
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
    
    
    
    /**
     * Handles the header part of a page.
     *
     * @param   $main   the main jquery tag
     */
    function Header($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.$image = $('img', me.$main).not('.info img');
        me.$info = $('.info', me.$main);
        me.$info_container = $('.info > .container', me.$main);
        me.$menu = $('.menu', me.$main);
        me.$menu_header = $('.header', me.$menu);
        me.$menu_navi = $('.navi', me.$menu);
        me.$nav = $('nav', me.$menu);
        me.$list = $('ul', me.$nav);
        me.$lists = $('li', me.$nav);
        me.$window = $(window);
        me.$body = $('body');
        
        me.$info_menu_space = null;
        me.$info_toggle_button = null;
        me.animating = false;
        me.$prev = null;
        me.$next = null;
        me.left_nav = 0;
        
        if ($('h1.on-top', $main).length) me.$main.addClass('headline-on-top');
        if (me.$image.length) me.$main.addClass('has-image');
        if (me.$image.length || me.$info.length) me.$main.addClass('has-content');
        if (me.$menu.length) me.$main.addClass('has-menu');
        if (me.$menu.hasClass('tabs')) me.$main.addClass('has-tabs');
        
        me.$image.load(function() {me.styleImage();});
        me.$window.resize(function() {me.onResize();});
        me.$window.scroll(function() {me.checkFixedPosition();});
        $('img').load(function() {me.checkFixedPosition();});
        me.onResize();
    }
    
    /**
     * Styles the image part of the header.
     */
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
    
    /**
     * Styles the info part of the header.
     */
    Header.prototype.styleInfo = function() {
        
        var me  = this.me;
        
        if (!me.$info.length) return;
        
        if (!me.$info_menu_space && me.$menu.length) {
            
            me.$info_menu_space = $('<div class="info-menu-space"></div>');
            me.$info.append(me.$info_menu_space);
        }
        
        if (!me.$info_toggle_button) {
         
            me.$info_toggle_button = $('<div class="toggle fawesome"></div>');
            me.$info_toggle_button.click(function() {me.infoToggle();});
            me.$info.append(me.$info_toggle_button);
        }
        
    }
    
    /**
     * Styles the navi/menu part of the header.
     */
    Header.prototype.styleNavi = function() {
        
        var me = this.me;
        
        if (!me.$nav.length) return;
        
        
        var header_position = me.$menu_header.position();
        me.$menu_navi.css('left', (header_position.left + me.$menu_header.width() + 20) + 'px');
        
        var navi_offset = me.$menu_navi.offset();
        var right_margin = 10;
        if (!me.$body.hasClass('is-xs')) right_margin = 40;
        if (me.$info.hasClass('closed') && !me.$main.hasClass('fixed')) {
            if (me.$body.hasClass('is-xs')) right_margin += 40;
            else right_margin += 56;
        }
        me.$menu_navi.width(me.$window.width() - right_margin - navi_offset.left);
        
        
        
        me.$list.css('width', '');
        me.$lists.css('left', '');
        
        var left = 0;
        var margin = (me.$body.hasClass('is-xs')) ? 40 : 60 ;
        me.$lists.each(function() {
            
            var $list = $(this);
            
            var width = $list.width();
            $list.data('left', left);
            $list.data('width', width);
            left += width + margin;
            
        });
        
        me.$list.width(left);
        
        me.$lists.each(function() {
            
            var $list = $(this);
           
            $list.css('left', $list.data('left') + 'px');
        });
        
        if (!me.$prev) {
            
            me.$prev = $('<div class="fawesome fa-left prev disabled"><span class="sr-only">previous</span></div>');
            me.$next = $('<div class="fawesome fa-right next disabled"><span class="sr-only">next</span></div>');
            
            me.$nav.after(me.$prev);
            me.$nav.after(me.$next);
            
            me.$prev.click(function() {me.prev();});
            me.$next.click(function() {me.next();});
            
            me.$nav.on("swiperight", function() {me.prev();});
            me.$nav.on("swipeleft", function() {me.next();});
        }
        
        
        var $left_nav = $(me.$lists.get(me.left_nav));
        me.$list.css('left', '-' + $left_nav.data('left') + 'px');
        
        me.checkNextPrev();
    }
    
    /**
     * Checks if the next/prev button of the navi/menu should be visible.
     */
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
            if (nav_width >= width || me.left_nav == me.$lists.length - 1) {
                me.$next.addClass('disabled');
            }
            
        }
    }
    
    /**
     * Moves to the next menu item.
     */
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
    
    /**
     * Moves to the previous menu item.
     */
    Header.prototype.prev = function() {
     
        var me = this.me;
        
        if (me.left_nav > 0) {
            me.left_nav--;   
            me.styleNavi();
        }
    }
        
    /**
     * Checks if the navi/menu has reached its fixed position at the top of the page.
     */
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
        
        me.styleNavi();
    }
    
    /**
     * Toggles the height of the info part.
     */
    Header.prototype.infoToggle = function() {
        
        var me = this.me;
        
        if (me.animating) return;
        me.animating = true;
        
        if (me.$info.hasClass('closed')) {
            
            me.$info.removeClass('closed');     
            me.$info_container.css('height', '');
            me.$info_container.css('display', '');
            
            var height = me.$info_container.height();
            var padding = 0;
            
            me.$info_container.height(0);
            me.$info_container.animate({
                height: height
            }, 400, function() {
                me.animating = false;
                me.$info_container.css('height', '');
                $('.slider', me.$info).data('me').styleIt();
                me.checkFixedPosition();
            });
            
        } else {
            
            me.$info.addClass('closed');   
            me.$info_container.css('height', '');
            me.$info_container.css('display', '');
            
            var height = me.$info_container.height();
            
            me.$info_container.height(height);
            me.$info_container.animate({
                height: 0
            }, 400, function() {
                me.animating = false;
                me.$info_container.css('display', 'none');
                me.$info_container.css('height', '');
                me.checkFixedPosition();
            });
            
        }
    }
    
    /**
     * The page got resized.
     */
    Header.prototype.onResize = function() {
        
        var me = this.me;
        
        me.styleImage();
        me.styleInfo();
        me.styleNavi();
        me.checkFixedPosition();
        
        setTimeout(function() {me.checkFixedPosition();}, 300);
    }
    
    $('.header').each(function() {
        new Header($(this)); 
    });
    
    
    
    function FaPercentage($main) {
        
        var me = this;
        this.me = me;
        
        me.$main = $main;
        me.canvas = $main.get(0);
        me.context = (me.canvas.getContext) ? me.canvas.getContext("2d") : null;
        
        me.value = parseInt(me.$main.attr('data-value'));
        me.color_active = me.$main.attr('data-color-active');
        me.color_inactive = me.$main.attr('data-color-inactive');
        
        me.$main.data('me', me);
        
        $(window).resize(function() {me.draw();});
        me.draw();
    }
    
    FaPercentage.prototype.draw = function() {
        
        var me = this.me;
        
        if (!me.context) return;
        
        me.$main.attr('width', '');
        me.$main.attr('height', '');
        
        var width = me.$main.width();
        var height = me.$main.height();
        var radius = (width < height) ? width/2 : height/2;
        var line = radius * 0.4;
        
        me.$main.attr('width', width);
        me.$main.attr('height', height);

        me.context.translate(width - radius, height - radius);
        me.context.lineWidth = line;
        radius -= line/2;
        
        me.context.clearRect(0,0,width,height);
        
        me.context.beginPath();
        me.context.arc(0, 0, radius, 0 , 2*Math.PI);
        me.context.strokeStyle = me.color_inactive;
        me.context.stroke();
        
        me.context.beginPath();
        me.context.arc(0, 0, radius, -Math.PI/2 , 2*Math.PI * (me.value / 100) -Math.PI/2);
        me.context.strokeStyle = me.color_active;
        me.context.stroke();
    }
    
    $('canvas.fawesome.fa-percentage').each(function() {
        new FaPercentage($(this)); 
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