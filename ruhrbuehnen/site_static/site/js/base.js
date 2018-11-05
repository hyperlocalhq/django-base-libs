/**
* @Author: Daniel Lehmann
* @Date:   2018/09/09
* @Email:  code@dreammedia.info
* @Last modified by:   Daniel Lehmann
* @Last modified time: 2018/11/05
* @copyright Daniel Lehmann (code@dreammedia.info)
*/

var image_cache = new Array();


function lazyload_images() {
    $(".img img:in-viewport").lazyload({
        load : function(element, el_left, settings){
            $(this).closest('.img').addClass('loaded');
        }
    });
}


u.ready(function() {

    u.window = u(window);
    u.html = u('html');
    u.body = u('body');

    u("a[href^='http://']").attr("target","_blank");

	if (typeof $ != "undefined" && $.tooltip && $("[data-toggle=tooltip]").length) {
        $("[data-toggle=tooltip]").tooltip({
        });
    }


    /**
     * Sniffs for the width of the browser window and its orientation.
     * Sets the class "is-xs", "is-sm", "is-md" or "is-lg" to the body and html tag accordingly to the current width.
     * Sets "is-vertical" or "is-horizontal"  to the body and html tag accordingly to the page dimensions.
     * Assumes that the body and html tag has the classes "is-xs" and "is-vertical" to begin with.
     */
    var current_width_sniffer = 'is-xs';
    var current_orientation_sniffer = 'is-vertical';
    var widthSniffer = function(first_sniff) {

        var new_width_sniffer = false;
        var reset_images = false;

        u('.width-sniffer').each$(function() {

            var u_node = u(this);
            if (u_node.css('display') == 'block') {

                if (u_node.hasClass('visible-xs')) {
                    new_width_sniffer = 'is-xs';
                } else if (u_node.hasClass('visible-sm')) {
                    new_width_sniffer = 'is-sm';
                } else if (u_node.hasClass('visible-md')) {
                    new_width_sniffer = 'is-md';
                } else if (u_node.hasClass('visible-lg')) {
                    new_width_sniffer = 'is-lg';
                } else if (u_node.hasClass('visible-xl')) {
                    new_width_sniffer = 'is-xl';
                }

                return false;
            }
        });

        if (!new_width_sniffer && window.frameElement) {

            var u_parent = u(window.parent.document.body);
            if (u_parent.hasClass('is-xs')) {
                new_width_sniffer = 'is-xs';
            } else if (u_parent.hasClass('is-sm')) {
                new_width_sniffer = 'is-sm';
            } else if (u_parent.hasClass('is-md')) {
                new_width_sniffer = 'is-md';
            } else if (u_parent.hasClass('is-lg')) {
                new_width_sniffer = 'is-lg';
            } else if (u_parent.hasClass('is-xl')) {
                new_width_sniffer = 'is-xl';
            }
        }

        if (new_width_sniffer && new_width_sniffer != current_width_sniffer) {
            u.html.removeClass(current_width_sniffer);
            u.body.removeClass(current_width_sniffer);
            current_width_sniffer = new_width_sniffer;
            u.html.addClass(new_width_sniffer);
            u.body.addClass(new_width_sniffer);
            reset_images = true;
        }


        var new_orientation_sniffer = false;
        var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        var height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

        if (width > height) new_orientation_sniffer = 'is-horizontal';
        else new_orientation_sniffer = 'is-vertical';

        if (new_orientation_sniffer && new_orientation_sniffer != current_orientation_sniffer) {
            u.html.removeClass(current_orientation_sniffer);
            u.body.removeClass(current_orientation_sniffer);
            current_orientation_sniffer = new_orientation_sniffer;
            u.html.addClass(new_orientation_sniffer);
            u.body.addClass(new_orientation_sniffer);
            reset_images = true;
        }

        if (reset_images && first_sniff !== true) imageResponsiveLoader();
    }
    u.window.resize(widthSniffer);
    widthSniffer(true);


    /**
     * Sniffs if the cms is in edit mode. Adds "cms-edit" to the body tag.
     */
    var cmsSniffer = function() {

        var search = location.search.substr(1);
        search = search.split("&");
        for (var i=0; i<search.length; i++) {
            var item = search[i].split("=");
            if (item[0] == "edit") break;
        }
        if (i != search.length) u.body.addClass('cms-edit');
    }
    cmsSniffer();


    /**
     * Loads images depending on the width and orientation of the screen.
     * Set up an image tag like this:
     *
     * <img class="responsive-xs" data-responsive-src="image/path" src="about:blank" style="display:none;" />
     *
     * If the screen is in xs mode, the image path will be transfered to the src attribute and the display style will be removed.
     * If the screen is not in xs mode, the src will be set to "about:blank" and the display style to "none" (if not already).
     * Bundle multiple image tags with different responsive classes together to provide images for every screen size.
     *
     * Possible responsive classes are:
     * responsive-[xs,sm,md,lg,xl]
     * responsive-[xs,sm,md,lg,xl]-[horizontal,vertical]
     *
     * You can add multiple responsive classes to one image tag.     *
     * Fires the events "imageSet" and "imageUnset" with the image node as second parameter each time an image src gets set or unset.
     *
     * PS: This function works in collaboration with the widhtSniffer function.
     */
    var imageResponsiveLoader = function() {

        var size = false;
        if (u.body.hasClass("is-xl")) size = "responsive-xl";
        if (u.body.hasClass("is-lg")) size = "responsive-lg";
        if (u.body.hasClass("is-md")) size = "responsive-md";
        if (u.body.hasClass("is-sm")) size = "responsive-sm";
        if (u.body.hasClass("is-xs")) size = "responsive-xs";

        var orientation = "";
        if (u.body.hasClass("is-horizontal")) orientation = "-horizontal";
        if (u.body.hasClass("is-vertical")) orientation = "-vertical";

        if (size) {
            u('img[data-responsive-src]').each(function(node) {

                var u_node = u(node);

                var exists = false;
                if (u_node.hasClass(size)) exists = true;
                else if (u_node.hasClass(size+orientation)) exists = true;

                var current_src = u_node.attr('src');
                if (exists) {
                    var src = u_node.attr("data-responsive-src");
                    if (current_src != src) {
                        u_node.attr('src', src);
                        var image = new Image();
                        image.src = src;
                        image_cache.push(image);
                        u_node.trigger('imageSet', node);
                    }
                    u_node.css('display', '');
                } else {
                    u_node.css('display', 'none');
                    if (current_src != 'about:blank') {
                        u_node.attr('src', 'about:blank');
                        u_node.trigger('imageUnset', node);
                    }
                }

            });
        }

    };
    window.setTimeout(imageResponsiveLoader, 1);
    u('.endless-loader').on('endlessLoader', function(e, u_nodes) {imageResponsiveLoader();});


    /**
     * Bunch if initialisation stuff.
     */
    u('.burger-button').click(function() {
        u.body.toggleClass('nav-open');
        u('#header .dropdown.user-menu').removeClass('open');
    });
    u('*[data-dropdown]').each(function(node) {
        var u_node = u(node);
        u_node.click(function() {
            u(u(this).attr('data-dropdown')).toggleClass('open');
        });
    });

    /**
     * Takes care of same date issue of endless loader
     * and puts the first newly loaded element into view.
     */
    u('.endless-loader').on('endlessLoader', function(e, u_children) {

        if (!EndlessLoader.anchor) EndlessLoader.anchor = 0;
        EndlessLoader.anchor++;
        var u_anchor = u('<a name="el'+EndlessLoader.anchor+'"></a>');

        var u_first = u(u_children.first());
        var u_last = u_first.previous();

        if (!u_last.length) return;

        var last = new Date();
        var first = new Date();
        last.setTime(parseInt(u_last.attr('data-date')) * 1000 );
        first.setTime(parseInt(u_first.attr('data-date')) * 1000 );

        last.setHours(0, 0, 0, 0);
        first.setHours(0, 0, 0, 0);

        if (last.getTime() == first.getTime()) {

            u_first.remove();
            var u_next = u(u_children.nodes[1]);
            u_next.children().each(function(node, index) {
                if (index == 0) u_last.append(u_anchor);
                u_last.append(node);
            });
            u_next.remove();

        } else {
            u_first.before(u_anchor);
            u_first.before('<div class="space"></div>');
        }

        window.location.hash = "#el"+EndlessLoader.anchor;
    });

    /**
     * Toggles dates view.
     */
    u('.grid-dates, .list-dates').each(function(node) {

        var u_node = u(node);

        u('a.more-dates', node).click(function() {
            u_node.removeClass('more');
        });
        u('a.less-dates', node).click(function() {
            u_node.addClass('more');
        });
    });





    /**
     * Handels the header image functionality.
     */
    function HeaderImage(u_main) {

        var me = this;
        me.u_main = u_main;
        me.u_children = u_main.children().not('.overlay');
        me.overlay = u('.overlay', u_main.first());
        me.top = me.u_children.css('top');

        if (parseInt(me.top) != 0) me.top = "50vh";

        me.resize();
        me.scroll();

        u.window.resize(function() {me.resize();});
        u.window.on('scroll', function() {me.scroll();});
        u('img', u_main.first()).on('load', function() {me.resize();});


        if (me.u_children.hasClass('slider') && me.overlay.length) {
            me.overlay.swipeOn().swipe(function(e, direction) {
                me.u_children.trigger('swipe', direction);
            });
        }
    }

    HeaderImage.prototype.scroll = function() {

        var me = this;

        var offset = window.pageYOffset;

        me.u_children.css('top', 'calc('+me.top+' - '+(offset/2)+'px)');

        if (me.overlay.length) {
            var overlay_height = me.overlay.height();
            if (overlay_height > 0) {
                var window_height = u.window.height();
                var top = (overlay_height - window_height) * (offset/window_height) *2;
                me.overlay.css('top', "-"+top+"px");
            }
        }
    }

    HeaderImage.prototype.resize = function() {

        var me = this;

        var image_width = 0;
        var image_height = 0;
        me.u_children.each$(function() {
            var u_image = u(this);
            if (u_image.css('display') == 'block') {
                image_width = u_image.width();
                image_height = u_image.height();
                return false;
            }
        });

        var window_width = u.window.width();
        var window_height = u.window.height();

        var width = image_width/window_width;
        var height = image_height/window_height;

        if (width > height) me.u_main.addClass('vertical');
        else me.u_main.removeClass('vertical');
    }

    u('.header-image').each(function(node) {
        new HeaderImage(u(node));
    });



    function HeightOffset(u_main) {

        var me = this;
        me.u_main = u_main;

        me.resize();
        u.window.resize(function() {me.resize();});
    }

    HeightOffset.prototype.resize = function() {

        var me = this;
        me.u_main.css('margin-bottom', '-'+me.u_main.height()+'px');
    }

    u('.height-offset').each(function(node) {
        new HeightOffset(u(node));
    });


    /**
     * Sticks an element beneath another as soon as it reaches the bottom of the other element.
     * The other element needs to be positioned "fixed" or has to have the class "glue".
     * Make sure the other element is fixed to the viewport or at least scrolls slower than the sticky element
     * otherwise it can't be reached.
     *
     * To define a sticky element add the attribute data-stick with the CSS selector of the other target element.
     * You can define multiple target elements by seperating the CSS selectors by comma. If the display of a target
     * is "none" or the postion is eather not "fixed" or does not have the class "glue", the next target will be used.
     *
     * As soon as the element gets sticked to the other it becomes postion fixed and so can be used as a target as well.
     * It also gets the class "sticky" and the width is set to its pre sticky width.
     *
     * If you have many elements sticked always at the same position and only the top one needs to be shown, you can group
     * these elements by giving them the same heap id with the attribute data-stick-heap. That way only the last sticked
     * of the group will be shown in its sticky state. You have to create the grouped Stick objects (new Stick(..)) in the
     * order the elements appear in the html code or, in other words, become sticky.
     */
    function Stick(u_main) {

        var me = this;
        me.u_main = u_main;
        me.u_placeholder = null;
        me.window_height = u.window.height();

        me.u_stick = null;
        var data_stick = me.u_main.attr('data-stick').split(',');
        for (var i=0; i<data_stick.length; i++) {
            if (!me.u_stick) me.u_stick = u(data_stick[i]);
            else me.u_stick = me.u_stick.add(data_stick[i]);
        }
        if (!me.u_stick) return;

        me.heap_index = -1;
        me.heap_name = me.u_main.attr('data-stick-heap');
        me.heap = null;
        if (me.heap_name) {
            if (!Stick.heap[me.heap_name]) {
                Stick.heap[me.heap_name] = [];
                Stick.heap_last[me.heap_name] = -1;
            }
            me.heap = Stick.heap[me.heap_name];
            me.heap_index = me.heap.length;
            me.heap[me.heap_index] = me;
            me.heap_display = me.u_main.css('display');
            me.u_main.addClass("heap-"+me.heap_index);
        }

        me.scroll_event = function() {me.scroll();}
        me.scroll();

        u.window.resize(function() {me.resize();});
        u.window.on2('scroll', me.scroll_event);
    }

    Stick.heap = [];
    Stick.heap_last = [];

    Stick.prototype.scroll = function(resize) {

        var me = this;


        // element removed
        if (!me.u_main || !me.u_main.parent().length) {
            if (me.u_placeholder) {
                me.u_placeholder.remove();
                me.u_placeholder = null;
            }
            me.u_main = null;

            if (me.heap) {
                for (var h=me.heap_index+1, hl=me.heap.length; h<hl; h++ ) {
                    me.heap[h].heap_index--;
                    me.heap[h-1] = me.heap[h];
                }
                me.heap.length = me.heap.length-1;
                if (me.heap_index < me.heap.length) me.heap[me.heap_index].scroll();
                me.heap = null;
            }
            return;
        }


        // element buried in the heap
        if (!resize && me.heap && me.heap_index != Stick.heap_last[me.heap_name] && me.heap_index != Stick.heap_last[me.heap_name]+1) return;


        var u_main = (me.u_placeholder) ? me.u_placeholder : me.u_main;
        var main_size = u_main.size();


        // element out of sight
        if (!resize) {
            if (me.u_main.hasClass('sticky')) {
                if (main_size.bottom < 0) return;
            } else {
                if (main_size.top > me.window_height) return;
            }
        }


        var u_stick = null;
        me.u_stick.each$(function() {
            var u_note = u(this);
            if (u_note.css('display') != "none" && (u_note.hasClass('glue') || u_note.css('position') == 'fixed')) {
                u_stick = u_note;
                return false;
            }
        });

        var offset = window.pageYOffset;
        var stick_size = (u_stick) ? u_stick.size() : null;

        if (u_stick && main_size.top <= stick_size.bottom) {
            me.u_main.css('position', 'fixed');
            me.u_main.css('top', stick_size.bottom+'px');
            me.u_main.addClass('sticky');
            if (!me.u_placeholder) {
                me.u_placeholder = u('<div></div>');
                me.u_placeholder.height(Math.round(me.u_main.height()));
                me.u_main.after(me.u_placeholder);
                me.u_main.width(Math.round(me.u_placeholder.width()));
            }

            // adding to heap (making it current last)
            if (me.heap && me.heap_index == Stick.heap_last[me.heap_name]+1) {
                if (Stick.heap_last[me.heap_name] >= 0) {
                    me.heap[Stick.heap_last[me.heap_name]].u_main.css('display', 'none');
                    u.window.off('scroll', me.heap[Stick.heap_last[me.heap_name]].scroll_event);
                }
                Stick.heap_last[me.heap_name]++;
                me.heap[Stick.heap_last[me.heap_name]].scroll(resize);
            }
        } else {
            me.u_main.css('position', '');
            me.u_main.css('top', '');
            me.u_main.removeClass('sticky');
            if (me.u_placeholder) {
                me.u_placeholder.remove();
                me.u_placeholder = null;
                me.u_main.css('width', '');
            }

            // removing from heap (making previous element current last)
            if (me.heap && me.heap_index == Stick.heap_last[me.heap_name]) {
                me.u_main.css('display', me.heap_display);

                Stick.heap_last[me.heap_name]--;
                if (Stick.heap_last[me.heap_name] >= 0) {
                    me.heap[Stick.heap_last[me.heap_name]].u_main.css('display', me.heap[Stick.heap_last[me.heap_name]].heap_display);
                    u.window.off('scroll', me.heap[Stick.heap_last[me.heap_name]].scroll_event);
                    u.window.on2('scroll', me.heap[Stick.heap_last[me.heap_name]].scroll_event);
                    me.heap[Stick.heap_last[me.heap_name]].scroll(resize);
                }
            }
        }
    }

    Stick.prototype.resize = function() {

        var me = this;
        me.window_height = u.window.height();

        if (me.u_placeholder) {
            if (me.heap && me.heap_index < Stick.heap_last) me.u_main.css('display', me.heap_display);
            me.u_placeholder.height(Math.round(me.u_main.height()));
            if (me.heap && me.heap_index < Stick.heap_last) me.u_main.css('display', 'none');
            me.u_main.width(Math.round(me.u_placeholder.width()));
        }

        me.scroll(true);
    }

    Stick.initiate = function(u_nodes) {

        u_nodes.each(function(node) {
            var u_node = u(node);
            if (u_node.attr('data-stick')) new Stick(u_node);
            u('*[data-stick]', node).each(function(node) {
                new Stick(u(node));
            });
        });
    }

    u('.endless-loader').on('endlessLoader', function(e, u_nodes) {Stick.initiate(u_nodes);});
    Stick.initiate(u('body'));



    /**
     * A slider.
     * Define a slider with the class "slider" and its slides with "slide".
     *
     * Add the attribute data-rotate="true" to have the slider rotate.
     * To have the slider slide autmaticly add the attribute data-interval with the slide interval in milliseconds.
     */
    function Slider(u_main) {

        var me = this;
        me.u_main = u_main;
        me.u_slides = u('.slide', me.u_main.first());
        me.length = me.u_slides.length;

        me.fullscreen = me.u_main.hasClass('fullscreen');

        me.rotate = me.u_main.attr('data-rotate');
        me.rotate = !(!(me.rotate && me.rotate !== "0" && me.rotate !== 0 && me.rotate.toLowerCase() !== "false"));
        me.interval = parseInt(me.u_main.attr('data-interval'));
        me.interval = (!me.interval || me.interval < 0) ? 0 : me.interval;
        me.timeout = null;

        me.current_slide = 0;
        me.next_slide = 0;
        me.final_slide = 0;
        me.skip_ending = false;
        me.animation_objects = [];
        me.is_animating = false;

        u(me.u_slides.first()).addClass('current');

        me.resize();
        u.window.resize(function() {me.resize();});

        u('img', me.u_main.first()).on('load imageSet', function() {me.resize();});


        if (me.u_slides.length > 1) {
            me.u_left = u('<div class="slide-left"></div>');
            me.u_right = u('<div class="slide-right"></div>');

            me.u_left.click(function() {me.interval = 0; me.slideToRight();});
            me.u_right.click(function() {me.interval = 0; me.slideToLeft();});

            me.u_main.append(me.u_left);
            me.u_main.append(me.u_right);

            me.checkButtons();

            me.u_main.swipeOn().swipe(function(event, direction) {me.swipe(direction);});
        }

        if (me.interval) me.timeout = u.setTimeout(function() {me.slideToLeft();}, me.interval);
    }

    Slider.prototype.slideTo = function(slide_nr) {

        var me = this;

        if (me.timeout) u.clearTimeout(me.timeout);
        me.timeout = null;

        if (me.is_animating) return;

        me.skip_ending = false;

        if (slide_nr >= me.length) {

            if (!me.rotate) {
                me.interval = 0;
                if (me.current_slide == me.length-1) me.checkButtons();
                else {
                    me.final_slide = me.length-1;
                    me.animate();
                }
            } else {
                me.skip_ending = true;
                me.final_slide = slide_nr-me.length;
                me.animate();
            }

        } else if (slide_nr < 0) {

            if (!me.rotate) {
                me.interval = 0;
                if (me.current_slide == 0) me.checkButtons();
                else {
                    me.final_slide = 0;
                    me.animate();
                }
            } else {
                me.skip_ending = true;
                me.final_slide = slide_nr+me.length;
                me.animate();
            }

        } else {

            me.final_slide = slide_nr;
            me.animate();
        }
    }

    Slider.prototype.slideToLeft = function() {

        var me = this;
        me.slideTo(me.current_slide+1);
    }

    Slider.prototype.slideToRight = function() {

        var me = this;
        me.slideTo(me.current_slide-1);
    }

    Slider.prototype.swipe = function(direction) {

        var me = this;

        if (direction == "left") {
            me.interval = 0;
            me.slideToLeft();
        }
        if (direction == "right") {
            me.interval = 0;
            me.slideToRight();
        }
    }

    Slider.prototype.checkButtons = function() {

        var me = this;

        if (me.u_slides.length < 2) return;

        if (me.rotate) {

            me.u_left.addClass('active').removeClass('inactive');
            me.u_right.addClass('active').removeClass('inactive');

        } else {

            if (me.current_slide == 0) {
                me.u_left.addClass('inactive').removeClass('active');
                me.u_right.addClass('active').removeClass('inactive');
            } else if (me.current_slide == me.length-1) {
                me.u_left.addClass('active').removeClass('inactive');
                me.u_right.addClass('inactive').removeClass('active');
            } else {
                me.u_left.addClass('active').removeClass('inactive');
                me.u_right.addClass('active').removeClass('inactive');
            }
        }
    }

    Slider.prototype.animate = function() {

        var me = this;

        me.is_animating = true;

        if (me.current_slide == me.final_slide) {
            me.checkButtons();
            me.is_animating = false;
            if (me.interval) me.timeout = u.setTimeout(function() {me.slideToLeft();}, me.interval);
            return;
        }

        if (me.current_slide < me.final_slide) {
            if (me.skip_ending) {
                me.next_slide = me.current_slide-1;
                if (me.next_slide < 0) me.next_slide = me.length-1;
            } else me.next_slide = me.current_slide+1;
        } else {
            if (me.skip_ending) {
                me.next_slide = me.current_slide+1;
                if (me.next_slide == me.length) me.next_slide = 0;
            } else me.next_slide = me.current_slide-1;
        }

        me.u_main.removeClass('is-animating');

        var u_current = u(me.u_slides.nodes[me.current_slide]);
        var u_next = u(me.u_slides.nodes[me.next_slide]);
        u_current.addClass('current').removeClass('next');
        u_next.addClass('next').removeClass('current');


        if (me.fullscreen) me.calcFullscreen();
    }

    Slider.prototype.startAnimation = function(callback) {

        var me = this;

        var u_current = u(me.u_slides.nodes[me.current_slide]);
        var u_next = u(me.u_slides.nodes[me.next_slide]);
        var fallback = null;

        var start = function() {

            u_next.transition(end);
            me.u_main.addClass('is-animating');

            window.setTimeout(function() {

                for (var i=0; i<me.animation_objects.length; i++) {
                    var u_object = me.animation_objects[i].object;
                    var animations = me.animation_objects[i].animations;

                    for (var animation in animations) {
                        u_object.css(animation, animations[animation]);
                    }
                }

                if (!u.transition_event) end();
                else {
                    var duration = u_next.css('transition-duration');
                    if (duration.substr(-1) == "s") duration = Math.round(parseFloat(duration)*1000);
                    else duration = parseInt(duration);

                    fallback = window.setTimeout(end, duration+100);
                }

            }, 100);
        }

        var end = function() {

            if (u.transition_event) u_next.off(u.transition_event);
            if (fallback) window.clearTimeout(fallback);

            me.u_main.removeClass('is-animating');
            u_current.removeClass('current');
            u_next.removeClass('next').addClass('current');

            if (callback) callback();

            me.current_slide = me.next_slide;
            me.animate();
        }

        window.setTimeout(start, 1);
    }

    Slider.prototype.calcFullscreen = function() {

        var me = this;

        var u_current = u(me.u_slides.nodes[me.current_slide]);
        var u_next = u(me.u_slides.nodes[me.next_slide]);

        var going_right = ((me.current_slide > me.next_slide && !me.skip_ending) || (me.current_slide < me.next_slide && me.skip_ending));

        me.animation_objects = [];
        if (going_right) {

            u_current.css('left', '0vw');
            u_next.css('left', '-100vw');
            u_next.first().focus();

            me.animation_objects.push({
                'object': u_current,
                'animations': {
                    'left': '100vw'
                }
            });

            me.animation_objects.push({
                'object': u_next,
                'animations': {
                    'left': '0vw'
                }
            });

        } else {

            u_current.css('left', '0vw');
            u_next.css('left', '100vw');
            u_next.first().focus();

            me.animation_objects.push({
                'object': u_current,
                'animations': {
                    'left': '-100vw'
                }
            });

            me.animation_objects.push({
                'object': u_next,
                'animations': {
                    'left': '0vw'
                }
            });

        }

        me.startAnimation();
    }

    Slider.prototype.resize = function() {

        var me = this;

        var image_width = 0;
        var image_height = 0;
        me.u_slides.each$(function() {
            var u_slide = u(this);
            if (u_slide.css('display') == 'block') {

                u('img', this).each$(function() {
                    var u_image = u(this);
                    image_width = u_image.width();
                    image_height = u_image.height();

                    if (image_width && image_height) return false;

                    image_width = 0;
                    image_height = 0;
                });

                if (image_width && image_height) return false;
            }
        });

        if (!image_width || !image_height) {
            window.setTimeout(function() {me.resize();}, 50);
            return;
        }

        var window_width = u.window.width();
        var window_height = u.window.height();

        var width = image_width/window_width;
        var height = image_height/window_height;

        if (width > height) me.u_main.addClass('vertical');
        else me.u_main.removeClass('vertical');
    }

    u('.slider').each(function(node) {
        new Slider(u(node));
    });



    /**
     * Establishes a functionality with which you can turn any object into a link by adding the attribute "data-href" to the object.
     * Optional you also can add the attribute "data-target".
     */
    function Link(u_main) {

        var me = this;
        me.u_main = u_main;

        me.u_main.click(function(event) {return me.click(event);});
    }

    Link.prototype.click = function(event) {

        event.preventDefault();

        var me = this;
        var href = me.u_main.attr('data-href');
        var target = me.u_main.attr('data-target');

        if (!target) target = '_self';
        if (target == '_self') location.href = href;
        else window.open(href, target);

        return false;
    }

    u('*[data-href]').each(function(node) {
        new Link(u(node));
    });



    function EndlessLoader(u_main) {

        var me = this;
        me.u_main = u_main;
        me.u_pagination = u('.pagination', me.u_main.first());
        me.loading = false;

        if (me.u_pagination.length) {

            me.u_pagination.remove();
            me.u_next_page = u('.next_page', me.u_pagination.first());

            if (me.u_next_page.length) {

                me.href = me.u_next_page.first().href;
                me.scroll_function = function() {me.scroll();};
                u.window.on2('scroll', me.scroll_function);

            }
        }
    }

    EndlessLoader.prototype.scroll = function() {

        var me = this;

        if (me.loading) return;

        if (!me.href) {
            u.window.off('scroll', me.scroll_function);
            return;
        }

        if (me.u_main.size().bottom <= u.window.height()) {
            me.loading = true;
            window.setTimeout(function() {me.load();}, 10);
        }
    }

    EndlessLoader.prototype.load = function() {

        var me = this;

        if (!u.ajax(me.href, function(context, success) {me.add(context, success);})) {
            me.href = null;
            me.loading = false;
        }
    }

    EndlessLoader.prototype.add = function(context, success) {

        var me = this;

        if (!success) {
            me.href = null;
            me.loading = false;
            return;
        }

        var lower = context.toLowerCase();
        context = context.substring(lower.indexOf('<body'), lower.indexOf('</body>')+7);

        var u_new = [];
        u(context).each(function(node) {
            if (!u_new.length) u_new = u('.endless-loader', node);
        });

        if (!u_new.length) {
            me.href = null;
            me.loading = false;
            return;
        }

        var u_pagination = u('.pagination', u_new.first());
        if (u_pagination.length) {
            u_pagination.remove();
            var u_next_page = u('.next_page', u_pagination.first());
            if (u_next_page.length) {
                me.href = u_next_page.first().href;
            } else me.href = null;
        } else me.href = null;

        var u_children = u_new.children();
        u_children.each(function(node) {
            me.u_main.append(node);
        });

        me.u_main.trigger('endlessLoader', u_children);
        u.window.trigger('resize');

        me.loading = false;
    }

    u('.endless-loader').each(function(node) {
        new EndlessLoader(u(node));
    });



    function Gallery(u_main) {

        var me = this;
        me.u_main = u_main;
        me.width = me.u_main.width();

        me.u_columns = u('.gallery-col', me.u_main.first());
        me.u_items = u('.gallery-item', me.u_main.first());
        me.u_images = u('img', me.u_main.first());

        me.order();
        me.u_images.on("load imageSet", function() { me.order(); });
        u.window.resize(function() { me.resize(); });
    }

    Gallery.prototype.order = function() {

        var me = this;

        me.u_items.remove();

        me.u_items.each(function(node) {

            var height = 999999999;
            var column = -1;
            me.u_columns.each(function(node, index) {
                var u_column = u(node);
                var column_height = u_column.height();
                if (column_height < height) {
                    height = column_height;
                    column = index;
                }
            });

            if (column >= 0) {
                u(me.u_columns.nodes[column]).append(node);
            }
        });
    }

    Gallery.prototype.resize = function() {

        var me = this;

        if ( me.u_main.width() != me.width) {
            me.order();
            me.width =  me.u_main.width();
        }
    }

    u('.gallery').each(function(node) {
        new Gallery(u(node));
    });




    function Accordion(u_main) {

        var me = this;
        me.u_main = u_main;
        me.u_items = u('.accordion-item', me.u_main.first());

        u('.accordion-head', me.u_main.first()).click(function() {me.click(u(this));});
        u('.accordion-body', me.u_main.first()).transition(function() {me.transition(u(this));});
    }

    Accordion.prototype.click = function(u_button) {

        var me = this;

        var u_item = u_button.parent();
        var is_open = u_item.hasClass('open');

        me.u_items.removeClass('open opened');
        if (!is_open) {
            u_item.addClass('open');
            if (!u.transition_event) u_item.addClass('opened');
        }
    }

    Accordion.prototype.transition = function(u_body) {

        var me = this;

        var u_item = u_body.parent();
        var is_open = u_item.hasClass('open');

        me.u_items.removeClass('opened');
        if (is_open) u_item.addClass('opened');
    }

    u('.accordion').each(function(node) {
        new Accordion(u(node));
    });

});
