/*
* Slides, A Slideshow Plugin for jQuery
* Intructions: http://slidesjs.com
* By: Nathan Searles, http://nathansearles.com
* Version: 1.2
* Updated: February 5th, 2013
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/(function(e){e.fn.slides=function(t){t=e.extend({},e.fn.slides.option,t);return this.each(function(){function S(o,u,a){if(!v&&d){v=!0;t.animationStart(p+1);switch(o){case"next":c=p;l=p+1;l=i===l?0:l;g=s*2;o=-s*2;p=l;break;case"prev":c=p;l=p-1;l=l===-1?i-1:l;g=0;o=0;p=l;break;case"pagination":l=parseInt(a,10);c=e("."+t.paginationClass+" li."+t.currentClass+" a",n).attr("href").match("[^#/]+$");if(l>c){g=s*2;o=-s*2}else{g=0;o=0}p=l}if(u==="fade")t.crossfade?r.children(":eq("+l+")",n).css({zIndex:10}).fadeIn(t.fadeSpeed,t.fadeEasing,function(){if(t.autoHeight)r.animate({height:r.children(":eq("+l+")",n).outerHeight()},t.autoHeightSpeed,function(){r.children(":eq("+c+")",n).css({display:"none",zIndex:0});r.children(":eq("+l+")",n).css({zIndex:0});t.animationComplete(l+1);v=!1});else{r.children(":eq("+c+")",n).css({display:"none",zIndex:0});r.children(":eq("+l+")",n).css({zIndex:0});t.animationComplete(l+1);v=!1}}):r.children(":eq("+c+")",n).fadeOut(t.fadeSpeed,t.fadeEasing,function(){t.autoHeight?r.animate({height:r.children(":eq("+l+")",n).outerHeight()},t.autoHeightSpeed,function(){r.children(":eq("+l+")",n).fadeIn(t.fadeSpeed,t.fadeEasing)}):r.children(":eq("+l+")",n).fadeIn(t.fadeSpeed,t.fadeEasing,function(){});t.animationComplete(l+1);v=!1});else{r.children(":eq("+l+")").css({left:g,display:"block"});t.autoHeight?r.animate({left:o,height:r.children(":eq("+l+")").outerHeight()},t.slideSpeed,t.slideEasing,function(){r.css({left:-s});r.children(":eq("+l+")").css({left:s,zIndex:5});r.children(":eq("+c+")").css({left:s,display:"none",zIndex:0});t.animationComplete(l+1);v=!1}):r.animate({left:o},t.slideSpeed,t.slideEasing,function(){r.css({left:-s});r.children(":eq("+l+")").css({left:s,zIndex:5});r.children(":eq("+c+")").css({left:s,display:"none",zIndex:0});t.animationComplete(l+1);v=!1})}if(t.pagination){e("."+t.paginationClass+" li."+t.currentClass,n).removeClass(t.currentClass);e("."+t.paginationClass+" li:eq("+l+")",n).addClass(t.currentClass)}}}function x(){clearInterval(n.data("interval"))}function T(){if(t.pause){clearTimeout(n.data("pause"));clearInterval(n.data("interval"));w=setTimeout(function(){clearTimeout(n.data("pause"));E=setInterval(function(){S("next",a)},t.play);n.data("interval",E)},t.pause);n.data("pause",w)}else x()}e("."+t.container,e(this)).children().wrapAll('<div class="slides_control"/>');var n=e(this),r=e(".slides_control",n),i=r.children().size(),s=r.children().outerWidth(),o=r.children().outerHeight(),u=t.start-1,a=t.effect.indexOf(",")<0?t.effect:t.effect.replace(" ","").split(",")[0],f=t.effect.indexOf(",")<0?a:t.effect.replace(" ","").split(",")[1],l=0,c=0,h=0,p=0,d,v,m,g,y,b,w,E;if(i<2){e("."+t.container,e(this)).fadeIn(t.fadeSpeed,t.fadeEasing,function(){d=!0;t.slidesLoaded()});e("."+t.next+", ."+t.prev).fadeOut(0);return!1}if(i<2)return;u<0&&(u=0);u>i&&(u=i-1);t.start&&(p=u);t.randomize&&r.randomize();e("."+t.container,n).css({overflow:"hidden",position:"relative"});r.children().css({position:"absolute",top:0,left:r.children().outerWidth(),zIndex:0,display:"none"});r.css({position:"relative",width:s*3,height:o,left:-s});e("."+t.container,n).css({display:"block"});if(t.autoHeight){r.children().css({height:"auto"});r.animate({height:r.children(":eq("+u+")").outerHeight()},t.autoHeightSpeed)}if(t.preload&&r.find("img:eq("+u+")").length){e("."+t.container,n).css({background:"url("+t.preloadImage+") no-repeat 50% 50%"});var N=r.find("img:eq("+u+")").attr("src")+"?"+(new Date).getTime();e("img",n).parent().attr("class")!="slides_control"?b=r.children(":eq(0)")[0].tagName.toLowerCase():b=r.find("img:eq("+u+")");r.find("img:eq("+u+")").attr("src",N).load(function(){r.find(b+":eq("+u+")").fadeIn(t.fadeSpeed,t.fadeEasing,function(){e(this).css({zIndex:5});e("."+t.container,n).css({background:""});d=!0;t.slidesLoaded()})})}else r.children(":eq("+u+")").fadeIn(t.fadeSpeed,t.fadeEasing,function(){d=!0;t.slidesLoaded()});if(t.bigTarget){r.children().css({cursor:"pointer"});r.children().on("click",function(){S("next",a);return!1})}if(t.hoverPause&&t.play){r.bind("mouseover",function(){x()});r.bind("mouseleave",function(){T()})}if(t.generateNextPrev){e("."+t.container,n).after('<a href="#" class="'+t.prev+'">Prev</a>');e("."+t.prev,n).after('<a href="#" class="'+t.next+'">Next</a>')}e("."+t.next,n).on("click",function(e){e.preventDefault();t.play&&T();S("next",a)});e("."+t.prev,n).on("click",function(e){e.preventDefault();t.play&&T();S("prev",a)});if(t.generatePagination){t.prependPagination?n.prepend("<ul class="+t.paginationClass+"></ul>"):n.append("<ul class="+t.paginationClass+"></ul>");r.children().each(function(){e("."+t.paginationClass,n).append('<li><a href="#'+h+'">'+(h+1)+"</a></li>");h++})}else e("."+t.paginationClass+" li a",n).each(function(){e(this).attr("href","#"+h);h++});e("."+t.paginationClass+" li:eq("+u+")",n).addClass(t.currentClass);e("."+t.paginationClass+" li a",n).on("click",function(){t.play&&T();m=e(this).attr("href").match("[^#/]+$");p!=m&&S("pagination",f,m);return!1});e("a.link",n).on("click",function(){t.play&&T();m=e(this).attr("href").match("[^#/]+$")-1;p!=m&&S("pagination",f,m);return!1});if(t.play){E=setInterval(function(){S("next",a)},t.play);n.data("interval",E)}})};e.fn.slides.option={preload:!1,preloadImage:"/img/loading.gif",container:"slides_container",generateNextPrev:!1,next:"next",prev:"prev",pagination:!1,generatePagination:!1,prependPagination:!1,paginationClass:"pagination",currentClass:"current",fadeSpeed:350,fadeEasing:"",slideSpeed:350,slideEasing:"",start:1,effect:"slide",crossfade:!1,randomize:!1,play:0,pause:0,hoverPause:!1,autoHeight:!1,autoHeightSpeed:350,bigTarget:!1,animationStart:function(){},animationComplete:function(){},slidesLoaded:function(){}};e.fn.randomize=function(t){function n(){return Math.round(Math.random())-.5}return e(this).each(function(){var r=e(this),s=r.children(),o=s.length;if(o>1){s.hide();var u=[];for(i=0;i<o;i++)u[u.length]=i;u=u.sort(n);e.each(u,function(e,n){var i=s.eq(n),o=i.clone(!0);o.show().appendTo(r);t!==undefined&&t(i,o);i.remove()})}})}})(jQuery);