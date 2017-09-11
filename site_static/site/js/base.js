/**
 * Base functionality of the page.
 *
 * @author Daniel Lehmann
 */



// checking for css transition support

/*! modernizr 3.2.0 (Custom Build) | MIT *
 * http://modernizr.com/download/?-csstransitions-setclasses !*/
!function(e,n,t){function r(e,n){return typeof e===n}function o(){var e,n,t,o,s,i,a;for(var l in C)if(C.hasOwnProperty(l)){if(e=[],n=C[l],n.name&&(e.push(n.name.toLowerCase()),n.options&&n.options.aliases&&n.options.aliases.length))for(t=0;t<n.options.aliases.length;t++)e.push(n.options.aliases[t].toLowerCase());for(o=r(n.fn,"function")?n.fn():n.fn,s=0;s<e.length;s++)i=e[s],a=i.split("."),1===a.length?Modernizr[a[0]]=o:(!Modernizr[a[0]]||Modernizr[a[0]]instanceof Boolean||(Modernizr[a[0]]=new Boolean(Modernizr[a[0]])),Modernizr[a[0]][a[1]]=o),g.push((o?"":"no-")+a.join("-"))}}function s(e){var n=_.className,t=Modernizr._config.classPrefix||"";if(S&&(n=n.baseVal),Modernizr._config.enableJSClass){var r=new RegExp("(^|\\s)"+t+"no-js(\\s|$)");n=n.replace(r,"$1"+t+"js$2")}Modernizr._config.enableClasses&&(n+=" "+t+e.join(" "+t),S?_.className.baseVal=n:_.className=n)}function i(e,n){return!!~(""+e).indexOf(n)}function a(){return"function"!=typeof n.createElement?n.createElement(arguments[0]):S?n.createElementNS.call(n,"http://www.w3.org/2000/svg",arguments[0]):n.createElement.apply(n,arguments)}function l(e){return e.replace(/([a-z])-([a-z])/g,function(e,n,t){return n+t.toUpperCase()}).replace(/^-/,"")}function f(e,n){return function(){return e.apply(n,arguments)}}function u(e,n,t){var o;for(var s in e)if(e[s]in n)return t===!1?e[s]:(o=n[e[s]],r(o,"function")?f(o,t||n):o);return!1}function d(e){return e.replace(/([A-Z])/g,function(e,n){return"-"+n.toLowerCase()}).replace(/^ms-/,"-ms-")}function c(){var e=n.body;return e||(e=a(S?"svg":"body"),e.fake=!0),e}function p(e,t,r,o){var s,i,l,f,u="modernizr",d=a("div"),p=c();if(parseInt(r,10))for(;r--;)l=a("div"),l.id=o?o[r]:u+(r+1),d.appendChild(l);return s=a("style"),s.type="text/css",s.id="s"+u,(p.fake?p:d).appendChild(s),p.appendChild(d),s.styleSheet?s.styleSheet.cssText=e:s.appendChild(n.createTextNode(e)),d.id=u,p.fake&&(p.style.background="",p.style.overflow="hidden",f=_.style.overflow,_.style.overflow="hidden",_.appendChild(p)),i=t(d,e),p.fake?(p.parentNode.removeChild(p),_.style.overflow=f,_.offsetHeight):d.parentNode.removeChild(d),!!i}function m(n,r){var o=n.length;if("CSS"in e&&"supports"in e.CSS){for(;o--;)if(e.CSS.supports(d(n[o]),r))return!0;return!1}if("CSSSupportsRule"in e){for(var s=[];o--;)s.push("("+d(n[o])+":"+r+")");return s=s.join(" or "),p("@supports ("+s+") { #modernizr { position: absolute; } }",function(e){return"absolute"==getComputedStyle(e,null).position})}return t}function h(e,n,o,s){function f(){d&&(delete z.style,delete z.modElem)}if(s=r(s,"undefined")?!1:s,!r(o,"undefined")){var u=m(e,o);if(!r(u,"undefined"))return u}for(var d,c,p,h,v,y=["modernizr","tspan"];!z.style;)d=!0,z.modElem=a(y.shift()),z.style=z.modElem.style;for(p=e.length,c=0;p>c;c++)if(h=e[c],v=z.style[h],i(h,"-")&&(h=l(h)),z.style[h]!==t){if(s||r(o,"undefined"))return f(),"pfx"==n?h:!0;try{z.style[h]=o}catch(g){}if(z.style[h]!=v)return f(),"pfx"==n?h:!0}return f(),!1}function v(e,n,t,o,s){var i=e.charAt(0).toUpperCase()+e.slice(1),a=(e+" "+b.join(i+" ")+i).split(" ");return r(n,"string")||r(n,"undefined")?h(a,n,o,s):(a=(e+" "+E.join(i+" ")+i).split(" "),u(a,n,t))}function y(e,n,r){return v(e,t,t,n,r)}var g=[],C=[],w={_version:"3.2.0",_config:{classPrefix:"",enableClasses:!0,enableJSClass:!0,usePrefixes:!0},_q:[],on:function(e,n){var t=this;setTimeout(function(){n(t[e])},0)},addTest:function(e,n,t){C.push({name:e,fn:n,options:t})},addAsyncTest:function(e){C.push({name:null,fn:e})}},Modernizr=function(){};Modernizr.prototype=w,Modernizr=new Modernizr;var _=n.documentElement,S="svg"===_.nodeName.toLowerCase(),x="Moz O ms Webkit",b=w._config.usePrefixes?x.split(" "):[];w._cssomPrefixes=b;var E=w._config.usePrefixes?x.toLowerCase().split(" "):[];w._domPrefixes=E;var P={elem:a("modernizr")};Modernizr._q.push(function(){delete P.elem});var z={style:P.elem.style};Modernizr._q.unshift(function(){delete z.style}),w.testAllProps=v,w.testAllProps=y,Modernizr.addTest("csstransitions",y("transition","all",!0)),o(),s(g),delete w.addTest,delete w.addAsyncTest;for(var N=0;N<Modernizr._q.length;N++)Modernizr._q[N]();e.Modernizr=Modernizr}(window,document);


// mobile device sniffer
!function(a){var b=/iPhone/i,c=/iPod/i,d=/iPad/i,e=/(?=.*\bAndroid\b)(?=.*\bMobile\b)/i,f=/Android/i,g=/IEMobile/i,h=/(?=.*\bWindows\b)(?=.*\bARM\b)/i,i=/BlackBerry/i,j=/BB10/i,k=/Opera Mini/i,l=/(?=.*\bFirefox\b)(?=.*\bMobile\b)/i,m=new RegExp("(?:Nexus 7|BNTV250|Kindle Fire|Silk|GT-P1000)","i"),n=function(a,b){return a.test(b)},o=function(a){var o=a||navigator.userAgent,p=o.split("[FBAN");return"undefined"!=typeof p[1]&&(o=p[0]),this.apple={phone:n(b,o),ipod:n(c,o),tablet:!n(b,o)&&n(d,o),device:n(b,o)||n(c,o)||n(d,o)},this.android={phone:n(e,o),tablet:!n(e,o)&&n(f,o),device:n(e,o)||n(f,o)},this.windows={phone:n(g,o),tablet:n(h,o),device:n(g,o)||n(h,o)},this.other={blackberry:n(i,o),blackberry10:n(j,o),opera:n(k,o),firefox:n(l,o),device:n(i,o)||n(j,o)||n(k,o)||n(l,o)},this.seven_inch=n(m,o),this.any=this.apple.device||this.android.device||this.windows.device||this.other.device||this.seven_inch,this.phone=this.apple.phone||this.android.phone||this.windows.phone,this.tablet=this.apple.tablet||this.android.tablet||this.windows.tablet,"undefined"==typeof window?this:void 0},p=function(){var a=new o;return a.Class=o,a};"undefined"!=typeof module&&module.exports&&"undefined"==typeof window?module.exports=o:"undefined"!=typeof module&&module.exports&&"undefined"!=typeof window?module.exports=p():"function"==typeof define&&define.amd?define("isMobile",[],a.isMobile=p()):a.isMobile=p()}(this);





$(document).ready(function() {

    window.redirect = function(url) {
        location.href = url;
    }

    if (isMobile.apple.phone || isMobile.android.phone) {
        $('.fawesome.fa-whatsapp.button').css('display', 'inline-block');
    }


    /**
     * Sniffs for the width of the browser window.
     * Sets the class "is-xs", "is-sm", "is-md" or "is-lg" to the body tag accordingly to the current width.
     */
    var current_width_sniffer = 'is-xs';
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

        if (!new_width_sniffer && window.frameElement) {

            var $parent = $(window.parent.document.body);
            if ($parent.hasClass('is-xs')) {
                new_width_sniffer = 'is-xs';
            } else if ($parent.hasClass('is-sm')) {
                new_width_sniffer = 'is-sm';
            } else if ($parent.hasClass('is-md')) {
                new_width_sniffer = 'is-md';
            } else if ($parent.hasClass('is-lg')) {
                new_width_sniffer = 'is-lg';
            }
        }

        if (new_width_sniffer && new_width_sniffer != current_width_sniffer) {
            var $body = $('body').removeClass(current_width_sniffer);
            current_width_sniffer = new_width_sniffer;
            $body.addClass(new_width_sniffer);
        }
    }
    $(window).resize(widthSniffer);
    widthSniffer();



    /**
     * TinyMCE responsive bug fix.
     */
    var mceEditorResponsiveFix = function() {

        var got_all = true;
        $('.tiny_mce_responsive').each(function() {

            var $textarea = $(this);
            var $editor = $textarea.next('#form_body_parent.mceEditor');

            if ($editor.length) {

                var $layout = $('#form_body_tbl.mceLayout', $editor);
                var width = $layout.width();
                $layout.css('max-width', width+'px').css('width', '100%');

                var $toolbar = $('#form_body_toolbar1');
                $('td', $toolbar).css('float', 'left').css('padding-bottom', '5px');

                $textarea.removeClass('tiny_mce_responsive');

            } else got_all = false;
        });

        if (!got_all) {
            window.setTimeout(mceEditorResponsiveFix, 100);
        }
    };
    mceEditorResponsiveFix();


    /**
     * Simulates a hover state if you tap on a link the first time.
     * The default click action triggers only at the second tap on the link.
     *
     * Mark the link with the class "tap-hover-trigger". If the link is also
     * the element which should recieve the class "hover" at the first tap,
     * give it the class "tap-hover" as well.
     *
     * If a different element (like some parent element) should recieve the
     * class "hover", give this element the class "tap-hover" and assign it
     * to the link element as jQuery object into the data variable "$tap-hover":
     * e.g. $link_element.data("$tap-hover", $hover_element);
     *
     * Now style the (.hover) class to look like the pseudo (:hover) class.
     */

    function TapHover($main) {

        var me = this;
        this.me = me;

        me.$main = $main;
        me.$hover = (me.$main.data('$tap-hover')) ? me.$main.data('$tap-hover') : me.$main;
        me.$all_trigger = $('.tap-hover-trigger');
        me.$all_hover = $('.tap-hover');

        me.$main.on('touchend', function(e) {return me.onTouch(e);});
        me.$main.on('click', function(e) {return me.onClick(e);});

        if (!TapHover.window_set) {
            TapHover.window_set = true;
            $(window).on('click', function() {me.onWindow();});
        }
    }

    TapHover.window_set = false;

    TapHover.prototype.onTouch = function(event) {

        var me = this;

        if (me.$main.hasClass('touch-active')) {
            me.$all_trigger.removeClass('touch-active');
            me.$all_hover.removeClass("hover");
        } else {
            me.$all_trigger.removeClass('touch-active');
            me.$all_hover.removeClass("hover");
            me.$main.addClass('touch-active');
            me.$hover.addClass("hover");
            event.preventDefault();
            return false;
        }
    }

    TapHover.prototype.onClick = function(event) {

        var me = this;

        if (me.$main.hasClass('touch-active')) {
            event.preventDefault();
            return false;
        }
    }

    TapHover.prototype.onWindow = function() {

        var me = this;

        me.$all_trigger.removeClass('touch-active');
        me.$all_hover.removeClass("hover");
    }

    $('.tap-hover-trigger').each(function() {
        new TapHover($(this));
    });


    function Accordion($main) {

        var me = this;
        this.me = me;

        me.$main = $main;
        me.adjustLevel();

        me.$children = $('> .accordion-inside', me.$main);
        me.$parents = me.$main.add(me.$main.parents('.accordion'));
        me.$window = $(window);
        me.is_animating = false;
        me.is_resizing = false;

        me.$children.each(function() {

            var $child = $(this);
            var $children = $child.add($('> *', $child));
            $children.click(function(e) {me.toggle($child, e);});
        });

        me.$main.data('Accordion', me);
        me.$main.data('AccordionChild', me);

        if (me.$main.hasClass('navi-box') || me.$main.hasClass('info-box')) me.initSmallScreen();
        setTimeout(function() {me.init();}, 0);


        if (me.$parents.length == 1) {
            me.width = me.$window.width();
            $(window).resize(function() {me.onResize();});
        }
    }

    Accordion.prototype.initSmallScreen = function() {

        if (!$('body').hasClass('is-xs')) return;

        var me = this.me;

        $('li.accordion-inside', me.$main).first().removeClass('opened');
    }

    Accordion.prototype.adjustLevel = function() {

        var me = this.me;

        if (me.$main.hasClass('adjust-level') && me.$main.hasClass('boxes')) {

            me.$main.removeClass('adjust-level');

            var current_level = 0;
            var $last_li = null;
            var parents = [];
            parents.push(me.$main);

            $('> li', me.$main).each(function() {

                var $li = $(this);
                var $parent = parents[parents.length-1];

                var level = parseInt($li.attr('data-level'));
                if (!level) level = 0;

                if (level > current_level) {

                    current_level = level;
                    $last_li.addClass('accordion-inside accordion-trigger');
                    $('> div.input-field.box', $last_li).addClass('accordion-trigger');

                    var $new_parent = $('<ul class="accordion boxes"></ul>');
                    $last_li.append($new_parent);
                    new Accordion($new_parent);

                    parents.push($new_parent);

                } else if (level < current_level) {

                    current_level = level;
                    parents.pop();

                }

                $last_li = $li;

                $parent = parents[parents.length-1];
                $parent.append($li);
            });
        }
    }

    Accordion.prototype.init = function() {

        var me = this.me;


        var children_initialised = true;
        $('.accordion', me.$children).each(function() {
            var $accordion = $(this);
            if (!$accordion.data('accordion-initialised')) children_initialised = false;
        });

        if (!children_initialised) {
            setTimeout(function() {me.init();}, 10);
            return;
        }



        var offset = 0;
        var is_height_0 = false;
        me.$children.each(function() {

            var $child = $(this);
            $child.data('Accordion', me);

            var $accordion = $('> .accordion', $child);
            var height = $accordion.data('height');
            if (!height) is_height_0 = true;
            if (!$child.hasClass('opened')) offset += height;
        });

        var height = me.$main.height();

        if (is_height_0 || height < offset) {
            setTimeout(function() {me.init();}, 10);
            return;
        }

        height -= offset;

        me.$main.data('height', height);
        me.$main.height(height);


        me.$main.data('accordion-initialised', true);



        if (me.$parents.length == 1) {

            var $all_children = $('.accordion-inside', me.$main);

            $all_children.each(function() {

                var $child = $(this);
                $child.data('accordion-root', me);

                if (!$child.hasClass('opened')) {
                    var $accordion = $('> .accordion', $child);
                    $accordion.height(0);
                }

            });

            setTimeout(function() {me.initDone();}, 100);
        };

    }

    Accordion.prototype.initDone = function() {

        var me = this.me;

        $('input, select, a', me.$main).off('focus').focus(function() {me.onFocus($(this));});
        me.$main.addClass('initialised');
        me.$main.off('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {me.onAnimationDone(e);});


        var check = true;
        var $all_children = $('.accordion-inside', me.$main);
        $all_children.each(function() {

            var $child = $(this);

            var $accordion = $('> .accordion', $child);
            var height = $accordion.data('height');
            $accordion.height('');
            if (height != $accordion.height()) check = false;
            if (!$child.hasClass('opened')) $accordion.height(0);
            else $accordion.height(height);

        });


        me.is_resizing = false;


        if (!check) {
            me.width = 0;
            me.onResize();
        } else {
            me.$main.trigger('initialised');
        }


    }

    Accordion.prototype.animating = function($child, value) {

        if (!Modernizr.csstransitions) return false;

        var root = $child.data('accordion-root');

        if (typeof value != 'undefined') root.is_animating = value;

        return root.is_animating;
    }

    Accordion.prototype.onAnimationDone = function(event) {

        var me = this.me;

        event.stopImmediatePropagation();

        var $target = $(event.target);
        if ($target.hasClass('animating')) {
            $target.removeClass('animating');
            me.is_animating = false;
        }

        me.$main.trigger('animationDone');
    }

    Accordion.prototype.onFocus = function($element) {

        var me = this.me;

        var $parents = $element.parents('.accordion');

        $parents.css('height', '');
        $parents.each(function() {

            var $parent = $(this);
            var $child = $parent.parent('.accordion-inside');

            var height = $parent.height();
            $parent.data('height', height);
            $parent.height(height);

            if ($child) $child.addClass('opened');
        });
    }

    Accordion.prototype.toggle = function($child, event) {

        var me = this.me;

        if (event) event.stopImmediatePropagation();

        var $target = $(event.target);
        if (!$target.hasClass('accordion-trigger')) return;


        if (me.animating($child)) return;
        me.animating($child, true);


        if ($child.hasClass('opened')) {

            var $accordion = $('> .accordion', $child);
            var accordion_height = $accordion.height();
            $accordion.data('height', accordion_height);


            me.$parents.each(function() {
                var $parent = $(this);
                $parent.data('height', $parent.height() - accordion_height);
            });
            me.$parents.each(function() {
                var $parent = $(this);
                $parent.height($parent.data('height'));
            });

            $accordion.addClass('animating');
            $accordion.height(0);
            $child.removeClass('opened');

        } else {

            var $accordion = $('> .accordion', $child);
            var accordion_height = $accordion.data('height');


            me.$parents.each(function() {
                var $parent = $(this);
                $parent.data('height', $parent.height() + accordion_height);
            });
            me.$parents.each(function() {
                var $parent = $(this);
                $parent.height($parent.data('height'));
            });

            $accordion.addClass('animating');
            $accordion.height(accordion_height);
            $child.addClass('opened');
        }
    }

    Accordion.prototype.open = function($child) {

        var me = this.me;

        if (!$child.hasClass('opened')) me.toggle($child);
    }

    Accordion.prototype.close = function($child) {

        var me = this.me;

        if ($child.hasClass('opened')) me.toggle($child);
    }

    Accordion.prototype.onResize = function() {

        var me = this;

        if (me.$window.width() == me.width) return;
        me.width = me.$window.width();

        if (me.is_resizing) return;
        me.is_resizing = true;

        if (me.$parents.length == 1) {

            me.$main.closest('.accordion').removeClass('initialised').height('').data('accordion-initialised', false).data('height', 0);
            $('.accordion', me.$main).removeClass('initialised').height('').data('accordion-initialised', false).data('height', 0);

            var $all_children = $('.accordion-inside', me.$main);

            $all_children.each(function() {

                var $child = $(this);
                var $accordion = $('> .accordion', $child);

                setTimeout(function() {$accordion.data('AccordionChild').init();}, 10);
            });

            setTimeout(function() {me.init();}, 50);

        }

    }

    $('.accordion').each(function() {
        new Accordion($(this));
    });



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
        me.$button = (me.$main.hasClass('fa-search')) ? me.$main : $('.fa-search', me.$main);
        me.$layer = $('#search-layer');
        me.$search = $('.fa-search', me.$layer);
        me.$close = $('.fa-close', me.$layer);
        me.$input = $('input#search_form_input', me.$layer);
        me.$form = $('form', me.$layer);
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
        me.$body.addClass('show-layer').addClass('search-layer');

        me.$search.off().click(function(e) {me.search(e);});
        me.$close.off().click(function() {me.close();});
        me.$layer.off().click(function() {me.close();});
        me.$input.off().keypress(function(e) {
            if(e.which == 13) {
                me.search(e);
            }
        }).click(function(e) {
            e.stopImmediatePropagation();
            e.preventDefault();
        });
        me.$input.focus();
        me.is_open = true;
    };

    Search.prototype.close = function() {

        var me = this.me;

        me.$search.off();
        me.$close.off();
        me.$layer.off();
        me.$input.off();
        me.$body.removeClass('show-layer').removeClass('search-layer');

        me.is_open = false;
    };

    Search.prototype.search = function(event) {

        var me = this.me;

        event.stopImmediatePropagation();
        event.preventDefault();

        $('input.search-form-type', me.$layer).remove();

        var type = me.$button.attr('data-type');
        if (type) {
            var types = type.split(',');
            for (var i=0, length=types.length; i<length; i++) {
                var $type = $('<input type="hidden" name="t"/>');
                $type.val(types[i]);
                me.$input.after($type);
            }
        }

        me.$form.submit();

    };

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
     * Handels the main navigation of the page.
     * Triggers 'navigation-closed' on the body tag if the navigation got closed.
     */
    function Navigation($main) {

        if (!$main.length) return;


        var me = this;
        this.me = me;

        me.$main = $main;
        me.$navi = $('nav', me.$main);
        me.$accordion = $('.accordion', me.$navi).first();
        me.$language = $('#language-navi', me.$main);
        me.$header = $('#header');
        me.$content = $('#body');
        me.$breadcrumbs = $('#breadcrumbs');
        me.$footer = $('#footer');
        me.$body = $('body');
        me.$window = $(window);

        me.$overlay = $('<div class="navigation-overlay"></div>');
        me.$content.append(me.$overlay);

        me.top = 0;
        me.language_value = (me.$language.length) ? me.$language.get(0).value : "de";

        me.$overlay.click(function() {me.$header.data('MainHeader').onNavigation();});
        me.$window.scroll(function() {me.onScroll();});
        me.$window.resize(function() {me.onResize();});
        me.$main.on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {me.onClosed(e);});
        me.$language.on('closed', function() {me.onLanguageChange();});
        me.$accordion.on('initialised animationDone', function() {me.setHeight();});

        $('.accordion').on('initialised', function() {me.setHeight();});

        me.$main.data('Navigation', me);
    }

    Navigation.prototype.open = function() {

        var me = this.me;

        me.$navi.css('height', '');

        me.top = me.getTop();

        me.$navi.css('padding-top', me.top + 'px');
        me.$overlay.css('display', 'block');
        setTimeout(function() {me.$overlay.css('opacity', '1');}, 0);

        me.$body.addClass('navigation-open');

        me.setHeight();
    }

    Navigation.prototype.close = function() {

        var me = this.me;

        if (!Modernizr.csstransitions) {
            setTimeout(function() {
                me.$main.css('height', '');
                me.$main.css('min-height', '');
                me.$content.css('height', '');
                me.$overlay.css('display', '');
                me.$body.trigger('navigation-closed');
            }, 500);
        }

        me.$overlay.css('opacity', '');
        me.$body.removeClass('navigation-open');
    }

    Navigation.prototype.onClosed = function(event) {

        var me = this.me;

        event.stopImmediatePropagation();

        if (!me.$body.hasClass('navigation-open')) {
            me.$main.css('height', '');
            me.$main.css('min-height', '');
            me.$content.css('height', '');
            me.$content.css('min-height', '');
            me.$navi.css('height', 0);
            me.$overlay.css('display', '');
            me.$body.trigger('navigation-closed');
        }
    }

    Navigation.prototype.onScroll = function() {

        var me = this.me;

        if (!me.$body.hasClass('navigation-open')) return;

        var top = me.getTop();

        if (top < me.top) {

            me.top = top;
            me.$navi.css('padding-top', me.top + 'px');
        }

        me.setHeight();
    }

    Navigation.prototype.getTop = function() {

        var me = this.me;

        var header_height = (me.$body.hasClass('is-xs')) ? 70 : (me.$body.hasClass('counselling') ? 110 : 114);
        var scroll_offset = (me.$body.hasClass('is-xs')) ? 25 : (me.$body.hasClass('counselling') ? 50 : 54);
        var scroll_top = me.$window.scrollTop();

        scroll_top -= scroll_offset;
        if (!me.$header.hasClass('fixed')) scroll_top = 0;
        if (scroll_top < 0) scroll_top = 0;

        return scroll_top + header_height;
    }

    Navigation.prototype.setHeight = function() {

        var me = this.me;

        me.$main.css('height', '');
        me.$main.css('min-height', '');
        me.$content.css('height', '');
        me.$content.css('min-height', '');

        var navi_height = me.$main.height() - 21;
        var content_height = me.$content.height();

        //alert(navi_height + ' - ' + content_height);

        if (navi_height > content_height) {
            me.$content.css('min-height', (navi_height + 21) + 'px');
        } else {
            me.$main.height(content_height);
            me.$content.css('min-height', content_height + 'px');
        }

        me.$main.css('min-height', content_height + 'px');

        if (!me.$body.hasClass('is-xs')) {
            var breadcrumbs_height = (me.$breadcrumbs.length) ? me.$breadcrumbs.height() : 0;
            me.$main.css('margin-bottom', breadcrumbs_height + me.$footer.height() + 'px');
        } else {
            me.$main.css('margin-bottom', me.$footer.height() + 'px');
        }

        if (!me.$body.hasClass('navigation-open')) {
            var navigation_min_height = parseInt(me.$main.css('min-height'));
            var content_min_height = parseInt(me.$content.css('min-height'));
            if (navigation_min_height && navigation_min_height != content_min_height) me.$content.css("min-height", navigation_min_height+"px");
        }
    }

    Navigation.prototype.onLanguageChange = function() {

        var me = this;

        if (me.$language.get(0).value != me.language_value) location.href = me.$language.get(0).value;
    }

    Navigation.prototype.onResize = function() {

        var me = this.me;


        me.top = me.getTop();

        me.$navi.css('padding-top', me.top + 'px');
    }

    new Navigation($('#navigation'));



    /**
     * Handles the main header of the page (the black top part with the logo).
     */
    function MainHeader($main) {

        if (!$main.length) return;


        var me = this;
        this.me = me;

        me.$main = $main;
        me.$wrapper = $('.wrapper', me.$main);
        me.$logo = $('.logo', me.$main);
        me.$navi_button = $('.fa-menu', me.$main);
        me.$language = $('#language_navi', me.$main);
        me.$user_menu = $('#avatar_navi', me.$main);
        me.$body = $('body');
        me.$window = $(window);
        me.$navi = $('#navigation');


        me.$wrapper.prepend('<div class="navigation-bg"></div>');

        me.navi_open = false;
        me.language_value = (me.$language.length) ? me.$language.get(0).value : "de";

        me.$navi_button.click(function() {me.onNavigation();});
        me.$user_menu.click(function() {me.onUserMenuToggle();});
        me.$language.click(function() {me.onLanguageMenuToggle();});
        me.$language.on('closed', function() {me.onLanguageChange();});
        me.$window.scroll(function() {me.checkFixedPosition();});


        me.$main.data('MainHeader', me);

        me.$window.resize(function() {me.onResize();});
        me.onResize();
    }

    MainHeader.prototype.onNavigation = function() {

        var me = this;

        me.navi_open = !(me.$body.hasClass('navigation-open'));

        if (!me.navi_open) {

            me.$navi_button.removeClass('fa-close');
            me.$navi_button.addClass('fa-menu');
            me.$navi.data('Navigation').close();

        } else {

            me.$user_menu.addClass('closed');
            me.$language.addClass('closed');
            me.$navi_button.removeClass('fa-menu');
            me.$navi_button.addClass('fa-close');
            me.$navi.data('Navigation').open();
        }
    }

    MainHeader.prototype.onLanguageChange = function() {

        var me = this;

        if (me.$language.get(0).value != me.language_value) location.href = me.$language.get(0).value;
    }

    MainHeader.prototype.onLanguageMenuToggle = function() {

        var me = this;
        me.$user_menu.addClass('closed');
        me.$language.toggleClass('closed');
    }

    MainHeader.prototype.onUserMenuToggle = function() {

        var me = this;

        if (me.navi_open) me.onNavigation();
        me.$language.addClass('closed');
        me.$user_menu.toggleClass('closed');
    }

    MainHeader.prototype.checkFixedPosition = function() {

        var me = this;

        var height = me.$main.height();
        var scroll_top = me.$window.scrollTop();

        if (scroll_top >= height) {
            me.$main.addClass('fixed');
        } else {
            me.$main.removeClass('fixed');
        }
    }

    MainHeader.prototype.onResize = function() {

        var me = this;

        me.checkFixedPosition();
        setTimeout(function() {me.checkFixedPosition();}, 0);
    }

    new MainHeader($('#header'));




    /**
     * Handles the big header part of a page beneath the black top part.
     *
     * @param   $main   the main jquery tag
     */
    function Header($main) {

        var me = this;
        this.me = me;

        me.$main = $main;
        me.$sticky = $('.sticky', me.$main);
        me.$image = $('img', me.$main).not('.info img').not('.profile img').not('.full');
        me.$headline = $('h1', me.$main);
        me.$info = $('.info', me.$main);
        me.$info_container = $('.info > .container', me.$main);
        me.$menu = $('.menu', me.$main);
        me.$menu_header = $('.headline', me.$menu);
        me.$menu_navi = $('.navi', me.$menu);
        me.$nav = $('nav', me.$menu);
        me.$list = $('ul', me.$nav);
        me.$lists = $('li', me.$nav);
        me.$window = $(window);
        me.$body = $('body');

        me.is_sticky = (me.$sticky.length);
        me.$info_menu_space = null;
        me.$info_toggle_button = null;
        me.animating = false;
        me.$prev = null;
        me.$next = null;
        me.left_nav = 0;

        if ($('h1.on-top', $main).length) me.$main.addClass('headline-on-top');
        if (me.$sticky.length) me.$main.addClass('has-sticky');
        if (me.$image.length) me.$main.addClass('has-image');
        if (me.$image.length || me.$info.length) me.$main.addClass('has-content');
        if (me.$menu.length) me.$main.addClass('has-menu');
        if (me.$menu.hasClass('tabs')) me.$main.addClass('has-tabs');

        me.$image.load(function() {me.styleImage();});
        me.$window.resize(function() {me.onResize();});
        me.$window.scroll(function() {me.checkFixedPosition();});
        me.$body.on('navigation-closed', function() {me.styleNavi();});
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

        if (!me.$body.hasClass('is-xs') || me.$body.hasClass('counselling')) {
            var image_height = me.$image.height();
            me.$main.height(image_height);
            me.$sticky.height(image_height);
            me.$image.css('margin-top', '-' + Math.round(image_height/2) + 'px');
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
        //if (me.$body.hasClass('navigation-open')) return;


        var header_position = me.$menu_header.position();
        me.$menu_navi.css('left', (header_position.left + me.$menu_header.width() + 20) + 'px');

        var navi_offset = me.$menu_navi.offset();
        var right_margin = 10;
        if (!me.$body.hasClass('is-xs')) right_margin = 40;
        if (me.$info.hasClass('closed') && !me.$main.hasClass('fixed')) {
            if (me.$body.hasClass('is-xs')) right_margin += 40;
            else right_margin += 56;
        }
        if (!me.$body.hasClass('navigation-open')) me.$menu_navi.width(me.$window.width() - right_margin - navi_offset.left);



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

        if (nav_width >= me.$list.width() && me.left_nav == 0) {

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

        var is_xs = me.$body.hasClass('is-xs');
        if (!me.$menu.length && !me.is_sticky) return;
        if (!me.$menu.length && is_xs) {
            me.$menu.css('top', '');
            me.$sticky.css('top', '');
            me.$main.removeClass('fixed-headline');
            me.$headline.css('width', '');
            return;
        }

        var height = me.$main.height() + me.$main.offset().top + parseInt(me.$main.css('padding-bottom'));

        if (is_xs) {

            var top = 40;
            var menu_height = (me.$menu.length) ? 40 : 0;

            height -= menu_height; // height of menu/tabs
            height -= top; // top position when fixed

        } else {

            var top = 60;
            var menu_height = (me.$menu.length) ? 56 : 0;

            if (me.is_sticky) {
                top += me.$headline.height() + 100;
            }

            height -= menu_height; // height of menu/tabs
            height -= top; // top position when fixed
        }

        var scroll_top = me.$window.scrollTop();
        if (scroll_top >= height) {

            me.$main.addClass('fixed');

            if (me.is_sticky && !is_xs) {
                var menu_height = (me.$menu.length) ? 56 : 0;
                me.$menu.css('top',  top + 'px');
                me.$sticky.css('top', '-' + (me.$sticky.height() - top - menu_height) + 'px');
            } else {
                me.$menu.css('top', '');
                me.$sticky.css('top', '');
            }

        } else {
            me.$main.removeClass('fixed');
            me.$menu.css('top', '');
            me.$sticky.css('top', '');
        }

        if (me.is_sticky) {

            var offset = me.$sticky.offset().top;

            if (!is_xs && scroll_top >= offset) {
                me.$main.addClass('fixed-headline');
                me.$headline.width(me.$headline.parent().width());
            } else {
                me.$main.removeClass('fixed-headline');
                me.$headline.css('width', '');
            }
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



    function ImagePopup($main) {

        var me = this;
        this.me = me;

        me.$main = $main;
        me.$layer = $('#image-layer');
        me.$wrapper = $('.wrapper', me.$layer);
        me.$image = $('.image', me.$layer);
        me.$caption = $('.caption', me.$layer);
        me.$navi = $('.navi', me.$layer);
        me.$close = $('.fa-close', me.$layer);
        me.$body = $('body');
        me.$window = $(window);

        me.popup = me.$main.attr('data-popup-image-src').toLowerCase();
        me.caption = me.$main.next('h5.caption').text();
        me.gallery = me.$main.attr('data-popup-image-gallery');

        me.is_open = false;
        me.index = 0;
        me.$current_image = null;

        me.is_animating = false;
        me.$next = null;
        me.$prev = null;


        if (me.gallery) {
            if (typeof ImagePopup.popups[me.gallery] == "undefined") ImagePopup.popups[me.gallery] = [];
            ImagePopup.popups[me.gallery].push({'popup':me.popup, 'caption':me.caption});
        }


        me.$main.click(function() {me.is_open = true; me.setIndex(); me.open();});
        me.$window.resize(function() {me.open();});
    }

    ImagePopup.popups = [];

    ImagePopup.prototype.setIndex = function() {

        var me = this.me;

        if (!me.gallery) return;

        var gallery = ImagePopup.popups[me.gallery];
        for (var i=0, length=gallery.length; i<length; i++) {
            if (gallery[i].popup == me.popup) break;
        }

        me.index = i;
    }

    ImagePopup.prototype.setImage = function(popup, caption) {

        var me = this.me;

        me.$wrapper.css('opacity', 0);
        me.$current_image = $('<img src="'+popup+'" />');
        me.$current_image.css('visibility', 'hidden');
        me.$current_image.load(function() {me.open();});
        me.$image.html('').append(me.$current_image);

        me.$caption.css('display', 'none');

        me.$caption.html('');
        if (caption && caption != '') me.$caption.text(caption);
    }

    ImagePopup.prototype.open = function() {

        var me = this.me;
        if (!me.is_open) return;

        me.close(me.$current_image);

        if (!me.$current_image) {

            me.setImage(me.popup, me.caption);

            me.$navi.html('');
            if (me.gallery) {

                 var gallery = ImagePopup.popups[me.gallery];

                 if (gallery.length > 1) {
                    me.$next = $('<a href="javascript:void(0);" class="fawesome fa-right-bold big button"></a>');
                    me.$prev = $('<a href="javascript:void(0);" class="fawesome fa-left-bold big button"></a>');

                    me.$next.click(function(e) {me.next(e);});
                    me.$prev.click(function(e) {me.prev(e);});

                    me.$navi.append(me.$next);
                    me.$navi.append(me.$prev);
                 }
            }
            me.$navi.off();
            me.$navi.on("swiperight", function(e) {me.prev(e);});
            me.$navi.on("swipeleft", function(e) {me.next(e);});
            me.$navi.click(function() {me.close();});
        }


        var window_top = me.$window.scrollTop();
        me.$layer.css('top', window_top + 'px');
        me.$body.addClass('show-layer').addClass('image-layer');


        // resetting the style values of the image
        me.$current_image.css('width', '');
        me.$current_image.css('height', '');
        me.$current_image.css('margin-top', '');


        // setting the initial dimensions of the image
        if (me.$current_image.width() > me.$image.width()) {
            me.$current_image.width(me.$image.width());
        }
        if (me.$current_image.height() > me.$image.height()) {
            me.$current_image.css('width', '');
            me.$current_image.height(me.$image.height());
        }


        // setting the width of the caption
        me.$caption.width(me.$current_image.width());
        // center the image verticaly
        me.$current_image.css('margin-top', Math.round((me.$image.height() - me.$current_image.height() - me.$caption.height()) / 2) + 'px');


        // show caption if image is loaded already
        if (me.$current_image.height()) me.$caption.css('display', '');


        var image_position = me.$current_image.offset();
        var image_height = me.$current_image.height();
        var caption_top = (image_position.top - window_top + image_height + 35);
        var caption_bottom = caption_top + me.$caption.height();

        // checking if the caption runs out of the bottom window -> adjusting the height of the image
        if (caption_bottom > me.$window.height()) image_height -= caption_bottom - me.$window.height();

        // setting the final height of the image
        me.$current_image.css('width', '');
        me.$current_image.height(image_height);

        // setting the position of the caption and its final width
        image_position = me.$current_image.offset();
        me.$caption.css('top', (image_position.top - window_top + image_height + 35) + 'px');
        me.$caption.css('left', image_position.left + 'px');
        me.$caption.width(me.$current_image.width());

        // show the image if it is loaded alreadey
        if (me.$current_image.height()) me.$current_image.css('visibility', '');


        me.$close.off().click(function() {me.close();});

        me.is_open = true;


        // animate in the image if it is loaded already
        if (me.$current_image.height()) {
            me.$wrapper.animate({
                opacity: 1
            }, 600, function() {
                me.animating = false;
            });
        }
    }

    ImagePopup.prototype.close = function($current_image) {

        var me = this.me;

        me.$body.removeClass('show-layer').removeClass('image-layer');
        me.$current_image = $current_image;

        me.is_open = false;
    }

    ImagePopup.prototype.next = function(event) {

        var me = this.me;

        if (event) event.stopImmediatePropagation();

        if (!me.gallery) return;
        if (me.animating) return;

        var gallery = ImagePopup.popups[me.gallery];
        if (gallery.length <= 1) return;

        me.animating = true;

        me.$wrapper.animate({
            opacity: 0
        }, 300, function() {
            me.index++;
            if (me.index >= gallery.length) me.index = 0;
            me.setImage(gallery[me.index].popup, gallery[me.index].caption);
            me.open();
        });
    }

    ImagePopup.prototype.prev = function(event) {

        var me = this.me;

        if (event) event.stopImmediatePropagation();

        if (!me.gallery) return;
        if (me.animating) return;

        var gallery = ImagePopup.popups[me.gallery];
        if (gallery.length <= 1) return;

        me.animating = true;

        me.$wrapper.animate({
            opacity: 0
        }, 300, function() {
            me.index--;
            if (me.index < 0) me.index = gallery.length-1;
            me.setImage(gallery[me.index].popup, gallery[me.index].caption);
            me.open();
        });
    }

    $('img[data-popup-image-src]').each(function() {
        new ImagePopup($(this));
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
