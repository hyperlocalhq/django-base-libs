(function($,e,b){var c="hashchange",h=document,f,g=$.event.special,i=h.documentMode,d="on"+c in e&&(i===b||i>7);
function a(j){j=j||location.href;
return"#"+j.replace(/^[^#]*#?(.*)$/,"$1")
}$.fn[c]=function(j){return j?this.bind(c,j):this.trigger(c)
};
$.fn[c].delay=50;
g[c]=$.extend(g[c],{setup:function(){if(d){return false
}$(f.start)
},teardown:function(){if(d){return false
}$(f.stop)
}});
f=(function(){var j={},p,m=a(),k=function(q){return q
},l=k,o=k;
j.start=function(){p||n()
};
j.stop=function(){p&&clearTimeout(p);
p=b
};
function n(){var r=a(),q=o(m);
if(r!==m){l(m=r,q);
$(e).trigger(c)
}else{if(q!==m){location.href=location.href.replace(/#.*/,"")+q
}}p=setTimeout(n,$.fn[c].delay)
}$.browser.msie&&!d&&(function(){var q,r;
j.start=function(){if(!q){r=$.fn[c].src;
r=r&&r+a();
q=$('<iframe tabindex="-1" title="empty"/>').hide().one("load",function(){r||l(a());
n()
}).attr("src",r||"javascript:0").insertAfter("body")[0].contentWindow;
h.onpropertychange=function(){try{if(event.propertyName==="title"){q.document.title=h.title
}}catch(s){}}
}};
j.stop=k;
o=function(){return a(q.location.href)
};
l=function(v,s){var u=q.document,t=$.fn[c].domain;
if(v!==s){u.title=h.title;
u.open();
t&&u.write('<script>document.domain="'+t+'"<\/script>');
u.close();
q.location.hash=v
}}
})();
return j
})()
})(jQuery,this);
jQuery.cookie=function(name,value,options){if(typeof value!="undefined"){options=options||{};
if(value===null){value="";
options.expires=-1
}var expires="";
if(options.expires&&(typeof options.expires=="number"||options.expires.toUTCString)){var date;
if(typeof options.expires=="number"){date=new Date();
date.setTime(date.getTime()+(options.expires*24*60*60*1000))
}else{date=options.expires
}expires="; expires="+date.toUTCString()
}var path=options.path?"; path="+options.path:"";
var domain=options.domain?"; domain="+options.domain:"";
var secure=options.secure?"; secure":"";
document.cookie=[name,"=",encodeURIComponent(value),expires,path,domain,secure].join("")
}else{var cookieValue=null;
if(document.cookie&&document.cookie!=""){var cookies=document.cookie.split(";");
for(var i=0;
i<cookies.length;
i++){var cookie=jQuery.trim(cookies[i]);
if(cookie.substring(0,name.length+1)==(name+"=")){cookieValue=decodeURIComponent(cookie.substring(name.length+1));
break
}}}return cookieValue
}};
(function($,undefined){self.close_popup=function(){if(window._popup_win){window._popup_win.dialog("destroy");
window._popup_win=null
}return false
};
self.open_popup=function(sTitle,iW,iH,sUrl,bWarning,oData,oEvents){var sInProgress='<div class="popup_in_progress"><img alt="" src="'+settings.STATIC_URL+'site/js/jquery/indicator.gif" /><span>'+gettext("Loading. Please wait.")+"</span></div>";
var sReloading='<div class="popup_in_progress"><img alt="" src="'+settings.STATIC_URL+'site/js/jquery/indicator.gif" /><span>'+gettext("Reloading the page...")+"</span></div>";
var sRedirecting='<div class="popup_in_progress"><img alt="" width="16" height="16" src="'+settings.STATIC_URL+'site/js/jquery/indicator.gif" /><span>'+gettext("Redirecting...")+"</span></div>";
close_popup();
oEvents=oEvents||{};
var onLoad=oEvents.onload;
function attach_form_events(responseText,textStatus,XMLHttpRequest){if(onLoad){onLoad()
}window._popup_win.find("input[name=cancel]").click(close_popup);
window._popup_win.find("form").submit(function(){var sValues="";
var oValues={};
$(this).find(":input").each(function(){var $oElem=$(this);
var sName=$oElem.attr("name");
var sValue=$oElem.val();
if(sName){if(!$oElem.is(":checkbox")||$oElem.attr("checked")){if(oValues[sName]){if(typeof(oValues[sName])=="string"){oValues[sName]=[oValues[sName]]
}oValues[sName].push(sValue)
}else{oValues[sName]=sValue
}}}});
var oOnBeforeSubmit=oEvents.onbeforesubmit;
var oOnSubmit=oEvents.onsubmit;
var oOnAfterSubmit=oEvents.onaftersubmit;
if(oOnBeforeSubmit){oOnBeforeSubmit()
}if(oOnSubmit){oOnSubmit();
if(oOnAfterSubmit){oOnAfterSubmit()
}}else{window._popup_win.html(sInProgress);
$.post(sUrl,oValues,function(sData,sStatus){if(!sData){if(oOnAfterSubmit){oOnAfterSubmit()
}close_popup()
}else{if(sData=="reload"){window._popup_win.html(sReloading);
document.location.href=document.location.pathname
}else{if(sData.indexOf("redirect")==0){window._popup_win.html(sRedirecting);
document.location.href=sData.replace(/^redirect=/,"")
}else{window._popup_win.html(sData);
attach_form_events()
}}}})
}return false
})
}sTitle=sTitle||"";
iW=parseInt(iW)||400;
var bAutoHeight=(iH=="auto");
if(iH=="auto"||!iH){iH=300
}var iX=(document.documentElement.clientWidth-iW)/2;
var iY=(document.documentElement.clientHeight-iH)/2;
var oPopup=window._popup_win=$("<div>"+sInProgress+"</div>").dialog({title:sTitle,width:iW,minWidth:iW,maxWidth:iW,height:iH,minHeight:iH,maxHeight:iH,position:[iX,iY]});
var oContainer=oPopup.parent().parent();
if(bWarning){oContainer.addClass("ui-warning-dialog")
}if(bAutoHeight){oContainer.css("height","auto")
}oContainer.css("overflow","visible");
sUrl=sUrl||"";
if(oData){oPopup.load(sUrl,oData,attach_form_events)
}else{oPopup.load(sUrl,attach_form_events)
}}
}(jQuery));
jQuery.fn.uniform=function(settings){settings=jQuery.extend({valid_class:"valid",invalid_class:"invalid",error_class:"error",focused_class:"focused",holder_class:"ctrlHolder",field_selector:"input, textarea, select",default_value_color:"#AFAFAF"},settings);
return this.each(function(){var form=jQuery(this),validate=function($input,valid,text){var $p=$input.closest("div."+settings.holder_class).andSelf().toggleClass(settings.invalid_class,!valid).toggleClass(settings.error_class,!valid).toggleClass(settings.valid_class,valid).find("p.formHint");
if(!valid&&!$p.data("info-text")){$p.data("info-text",$p.html())
}else{if(valid){text=$p.data("info-text")
}}if(text){$p.html(text)
}};
form.submit(function(){form.find(settings.field_selector).each(function(){if($(this).val()==$(this).data("default-value")){$(this).val("")
}})
});
form.find(settings.field_selector).each(function(){var $input=$(this),value=$input.val();
$input.data("default-color",$input.css("color"));
if(value==$input.data("default-value")||!value){$input.not("select").css("color",settings.default_value_color);
$input.val($input.data("default-value"))
}});
form.delegate(settings.field_selector,"focus",function(){form.find("."+settings.focused_class).removeClass(settings.focused_class);
var $input=$(this);
$input.parents().filter("."+settings.holder_class+":first").addClass(settings.focused_class);
if($input.val()==$input.data("default-value")){$input.val("")
}$input.not("select").css("color",$input.data("default-color"))
});
form.delegate(settings.field_selector,"blur",function(){var $input=$(this);
form.find("."+settings.focused_class).removeClass(settings.focused_class);
if($input.val()==""||$input.val()==$input.data("default-value")){$input.not("select").css("color",settings.default_value_color);
$input.val($input.data("default-value"))
}else{$input.css("color",$input.data("default-color"))
}});
form.delegate(settings.field_selector,"error",function(e,text){validate($(this),false,text)
});
form.delegate(settings.field_selector,"success",function(e,text){validate($(this),true)
})
})
};