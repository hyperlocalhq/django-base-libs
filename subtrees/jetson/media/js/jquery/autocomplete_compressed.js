(function($){$.fn.bgIframe=$.fn.bgiframe=function(s){if($.browser.msie&&/6.0/.test(navigator.userAgent)){s=$.extend({top:"auto",left:"auto",width:"auto",height:"auto",opacity:true,src:"javascript:false;"},s||{});
var prop=function(n){return n&&n.constructor==Number?n+"px":n
},html='<iframe class="bgiframe"frameborder="0"tabindex="-1"src="'+s.src+'"style="display:block;position:absolute;z-index:-1;'+(s.opacity!==false?"filter:Alpha(Opacity='0');":"")+"top:"+(s.top=="auto"?"expression(((parseInt(this.parentNode.currentStyle.borderTopWidth)||0)*-1)+'px')":prop(s.top))+";left:"+(s.left=="auto"?"expression(((parseInt(this.parentNode.currentStyle.borderLeftWidth)||0)*-1)+'px')":prop(s.left))+";width:"+(s.width=="auto"?"expression(this.parentNode.offsetWidth+'px')":prop(s.width))+";height:"+(s.height=="auto"?"expression(this.parentNode.offsetHeight+'px')":prop(s.height))+';"/>';
return this.each(function(){if($("> iframe.bgiframe",this).length==0){this.insertBefore(document.createElement(html),this.firstChild)
}})
}return this
}
})(jQuery);
(function($){$.fn.extend({autocomplete:function(urlOrData,options){var isUrl=typeof urlOrData=="string";
options=$.extend({},$.Autocompleter.defaults,{url:isUrl?urlOrData:null,data:isUrl?null:urlOrData,delay:isUrl?$.Autocompleter.defaults.delay:10,max:options&&!options.scroll?10:150},options);
options.highlight=options.highlight||function(value){return value
};
return this.each(function(){new $.Autocompleter(this,options)
})
},result:function(handler){return this.bind("result",handler)
},search:function(handler){return this.trigger("search",[handler])
},flushCache:function(){return this.trigger("flushCache")
},setOptions:function(options){return this.trigger("setOptions",[options])
},unautocomplete:function(){return this.trigger("unautocomplete")
}});
$.Autocompleter=function(input,options){var KEY={UP:38,DOWN:40,DEL:46,TAB:9,RETURN:13,ESC:27,COMMA:188,PAGEUP:33,PAGEDOWN:34};
var $input=$(input).attr("autocomplete","off").addClass(options.inputClass);
var timeout;
var previousValue="";
var cache=$.Autocompleter.Cache(options);
var hasFocus=0;
var lastKeyPressCode;
var config={mouseDownOnSelect:false};
var select=$.Autocompleter.Select(options,input,selectCurrent,config);
$input.keydown(function(event){lastKeyPressCode=event.keyCode;
switch(event.keyCode){case KEY.UP:event.preventDefault();
if(select.visible()){select.prev()
}else{onChange(0,true)
}break;
case KEY.DOWN:event.preventDefault();
if(select.visible()){select.next()
}else{onChange(0,true)
}break;
case KEY.PAGEUP:event.preventDefault();
if(select.visible()){select.pageUp()
}else{onChange(0,true)
}break;
case KEY.PAGEDOWN:event.preventDefault();
if(select.visible()){select.pageDown()
}else{onChange(0,true)
}break;
case options.multiple&&$.trim(options.multipleSeparator)==","&&KEY.COMMA:case KEY.TAB:case KEY.RETURN:if(selectCurrent()){if(!options.multiple){$input.blur()
}event.preventDefault()
}break;
case KEY.ESC:select.hide();
break;
default:clearTimeout(timeout);
timeout=setTimeout(onChange,options.delay);
break
}}).keypress(function(){}).focus(function(){hasFocus++
}).blur(function(){hasFocus=0;
if(!config.mouseDownOnSelect){hideResults()
}}).click(function(){if(hasFocus++>1&&!select.visible()){onChange(0,true)
}}).bind("search",function(){var fn=(arguments.length>1)?arguments[1]:null;
function findValueCallback(q,data){var result;
if(data&&data.length){for(var i=0;
i<data.length;
i++){if(data[i].result.toLowerCase()==q.toLowerCase()){result=data[i];
break
}}}if(typeof fn=="function"){fn(result)
}else{$input.trigger("result",result&&[result.data,result.value])
}}$.each(trimWords($input.val()),function(i,value){request(value,findValueCallback,findValueCallback)
})
}).bind("flushCache",function(){cache.flush()
}).bind("setOptions",function(){$.extend(options,arguments[1]);
if("data" in arguments[1]){cache.populate()
}}).bind("unautocomplete",function(){select.unbind();
$input.unbind()
});
function selectCurrent(){var selected=select.selected();
if(!selected){return false
}var v=selected.result;
previousValue=v;
if(options.multiple){var words=trimWords($input.val());
if(words.length>1){v=words.slice(0,words.length-1).join(options.multipleSeparator)+options.multipleSeparator+v
}v+=options.multipleSeparator
}$input.val(v);
hideResultsNow();
$input.trigger("result",[selected.data,selected.value]);
return true
}function onChange(crap,skipPrevCheck){if(lastKeyPressCode==KEY.DEL){select.hide();
return
}var currentValue=$input.val();
if(!skipPrevCheck&&currentValue==previousValue){return
}previousValue=currentValue;
currentValue=lastWord(currentValue);
if(currentValue.length>=options.minChars){$input.addClass(options.loadingClass);
if(!options.matchCase){currentValue=currentValue.toLowerCase()
}request(currentValue,receiveData,hideResultsNow)
}else{stopLoading();
select.hide()
}}function trimWords(value){if(!value){return[""]
}var words=value.split($.trim(options.multipleSeparator));
var result=[];
$.each(words,function(i,value){if($.trim(value)){result[i]=$.trim(value)
}});
return result
}function lastWord(value){if(!options.multiple){return value
}var words=trimWords(value);
return words[words.length-1]
}function autoFill(q,sValue){if(options.autoFill&&(lastWord($input.val()).toLowerCase()==q.toLowerCase())&&lastKeyPressCode!=8){$input.val($input.val()+sValue.substring(lastWord(previousValue).length));
$.Autocompleter.Selection(input,previousValue.length,previousValue.length+sValue.length)
}}function hideResults(){clearTimeout(timeout);
timeout=setTimeout(hideResultsNow,200)
}function hideResultsNow(){select.hide();
clearTimeout(timeout);
stopLoading();
if(options.mustMatch){$input.search(function(result){if(!result){$input.val("")
}})
}}function receiveData(q,data){if(data&&data.length&&hasFocus){stopLoading();
select.display(data,q);
autoFill(q,data[0].value);
select.show()
}else{hideResultsNow()
}}function request(term,success,failure){if(!options.matchCase){term=term.toLowerCase()
}var data=cache.load(term);
if(data&&data.length){success(term,data)
}else{if((typeof options.url=="string")&&(options.url.length>0)){var extraParams={};
$.each(options.extraParams,function(key,param){extraParams[key]=typeof param=="function"?param():param
});
$.ajax({mode:"abort",port:"autocomplete"+input.name,dataType:options.dataType,url:options.url,data:$.extend({q:lastWord(term),limit:options.max},extraParams),success:function(data){var parsed=options.parse&&options.parse(data)||parse(data);
cache.add(term,parsed);
success(term,parsed)
}})
}else{failure(term)
}}}function parse(data){var parsed=[];
var rows=data.split("\n");
for(var i=0;
i<rows.length;
i++){var row=$.trim(rows[i]);
if(row){row=row.split("|");
parsed[parsed.length]={data:row,value:row[0],result:options.formatResult&&options.formatResult(row,row[0])||row[0]}
}}return parsed
}function stopLoading(){$input.removeClass(options.loadingClass)
}};
$.Autocompleter.defaults={inputClass:"ac_input",resultsClass:"ac_results",loadingClass:"ac_loading",minChars:1,delay:400,matchCase:false,matchSubset:true,matchContains:false,cacheLength:10,max:100,mustMatch:false,extraParams:{},selectFirst:true,formatItem:function(row){return row[0]
},autoFill:false,width:0,multiple:false,multipleSeparator:", ",highlight:function(value,term){return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)("+term.replace(/([\^\$\(\)\[\]\{\}\*\.\+\?\|\\])/gi,"\\$1")+")(?![^<>]*>)(?![^&;]+;)","gi"),"<strong>$1</strong>")
},scroll:true,scrollHeight:180,attachTo:"body"};
$.Autocompleter.Cache=function(options){var data={};
var length=0;
function matchSubset(s,sub){if(!options.matchCase){s=s.toLowerCase()
}var i=s.indexOf(sub);
if(i==-1){return false
}return i==0||options.matchContains
}function add(q,value){if(length>options.cacheLength){flush()
}if(!data[q]){length++
}data[q]=value
}function populate(){if(!options.data){return false
}var stMatchSets={},nullData=0;
if(!options.url){options.cacheLength=1
}stMatchSets[""]=[];
for(var i=0,ol=options.data.length;
i<ol;
i++){var rawValue=options.data[i];
rawValue=(typeof rawValue=="string")?[rawValue]:rawValue;
var value=options.formatItem(rawValue,i+1,options.data.length);
if(value===false){continue
}var firstChar=value.charAt(0).toLowerCase();
if(!stMatchSets[firstChar]){stMatchSets[firstChar]=[]
}var row={value:value,data:rawValue,result:options.formatResult&&options.formatResult(rawValue)||value};
stMatchSets[firstChar].push(row);
if(nullData++<options.max){stMatchSets[""].push(row)
}}$.each(stMatchSets,function(i,value){options.cacheLength++;
add(i,value)
})
}setTimeout(populate,25);
function flush(){data={};
length=0
}return{flush:flush,add:add,populate:populate,load:function(q){if(!options.cacheLength||!length){return null
}if(!options.url&&options.matchContains){var csub=[];
for(var k in data){if(k.length>0){var c=data[k];
$.each(c,function(i,x){if(matchSubset(x.value,q)){csub.push(x)
}})
}}return csub
}else{if(data[q]){return data[q]
}else{if(options.matchSubset){for(var i=q.length-1;
i>=options.minChars;
i--){var c=data[q.substr(0,i)];
if(c){var csub=[];
$.each(c,function(i,x){if(matchSubset(x.value,q)){csub[csub.length]=x
}});
return csub
}}}}}return null
}}
};
$.Autocompleter.Select=function(options,input,select,config){var CLASSES={ACTIVE:"ac_over"};
var listItems,active=-1,data,term="",needsInit=true,element,list;
function init(){if(!needsInit){return
}element=$("<div/>").hide().addClass(options.resultsClass).css("position","absolute").appendTo(options.attachTo);
list=$("<ul>").appendTo(element).mouseover(function(event){if(target(event).nodeName&&target(event).nodeName.toUpperCase()=="LI"){active=$("li",list).removeClass(CLASSES.ACTIVE).index(target(event));
$(target(event)).addClass(CLASSES.ACTIVE)
}}).click(function(event){$(target(event)).addClass(CLASSES.ACTIVE);
select();
input.focus();
return false
}).mousedown(function(){config.mouseDownOnSelect=true
}).mouseup(function(){config.mouseDownOnSelect=false
});
if(options.width>0){element.css("width",options.width)
}needsInit=false
}function target(event){var element=event.target;
while(element&&element.tagName!="LI"){element=element.parentNode
}if(!element){return[]
}return element
}function moveSelect(step){listItems.slice(active,active+1).removeClass();
movePosition(step);
var activeItem=listItems.slice(active,active+1).addClass(CLASSES.ACTIVE);
if(options.scroll){var offset=0;
listItems.slice(0,active).each(function(){offset+=this.offsetHeight
});
if((offset+activeItem[0].offsetHeight-list.scrollTop())>list[0].clientHeight){list.scrollTop(offset+activeItem[0].offsetHeight-list.innerHeight())
}else{if(offset<list.scrollTop()){list.scrollTop(offset)
}}}}function movePosition(step){active+=step;
if(active<0){active=listItems.size()-1
}else{if(active>=listItems.size()){active=0
}}}function limitNumberOfItems(available){return options.max&&options.max<available?options.max:available
}function fillList(){list.empty();
var max=limitNumberOfItems(data.length);
for(var i=0;
i<max;
i++){if(!data[i]){continue
}var formatted=options.formatItem(data[i].data,i+1,max,data[i].value,term);
if(formatted===false){continue
}var li=$("<li>").html(options.highlight(formatted,term)).addClass(i%2==0?"ac_event":"ac_odd").appendTo(list)[0];
$.data(li,"ac_data",data[i])
}listItems=list.find("li");
if(options.selectFirst){listItems.slice(0,1).addClass(CLASSES.ACTIVE);
active=0
}list.bgiframe()
}return{display:function(d,q){init();
data=d;
term=q;
fillList()
},next:function(){moveSelect(1)
},prev:function(){moveSelect(-1)
},pageUp:function(){if(active!=0&&active-8<0){moveSelect(-active)
}else{moveSelect(-8)
}},pageDown:function(){if(active!=listItems.size()-1&&active+8>listItems.size()){moveSelect(listItems.size()-1-active)
}else{moveSelect(8)
}},hide:function(){element&&element.hide();
active=-1
},visible:function(){return element&&element.is(":visible")
},current:function(){return this.visible()&&(listItems.filter("."+CLASSES.ACTIVE)[0]||options.selectFirst&&listItems[0])
},show:function(){var offset=$(input).offset();
element.css({width:typeof options.width=="string"||options.width>0?options.width:$(input).width(),top:offset.top+input.offsetHeight,left:offset.left}).show();
if(options.scroll){list.scrollTop(0);
list.css({maxHeight:options.scrollHeight,overflow:"auto"});
if($.browser.msie&&typeof document.body.style.maxHeight==="undefined"){var listHeight=0;
listItems.each(function(){listHeight+=this.offsetHeight
});
var scrollbarsVisible=listHeight>options.scrollHeight;
list.css("height",scrollbarsVisible?options.scrollHeight:listHeight);
if(!scrollbarsVisible){listItems.width(list.width()-parseInt(listItems.css("padding-left"))-parseInt(listItems.css("padding-right")))
}}}},selected:function(){var selected=listItems&&listItems.filter("."+CLASSES.ACTIVE).removeClass(CLASSES.ACTIVE);
return selected&&selected.length&&$.data(selected[0],"ac_data")
},unbind:function(){element&&element.remove()
}}
};
$.Autocompleter.Selection=function(field,start,end){if(field.createTextRange){var selRange=field.createTextRange();
selRange.collapse(true);
selRange.moveStart("character",start);
selRange.moveEnd("character",end);
selRange.select()
}else{if(field.setSelectionRange){field.setSelectionRange(start,end)
}else{if(field.selectionStart){field.selectionStart=start;
field.selectionEnd=end
}}}field.focus()
}
})(jQuery);
(function($,undefined){function AutocompleteManagerClass(){var registered_selectors={};
var dynamic=[];
var that=this;
this.init=function(){var i,iLen=dynamic.length;
for(i=0;
i<iLen;
i++){var oEl=dynamic[i];
this.set_autocomplete($(oEl.selector),oEl.urlOrData,oEl.options)
}};
this.reinit=function($oRow){var i,iLen=dynamic.length;
for(i=0;
i<iLen;
i++){var oEl=dynamic[i];
this.set_autocomplete($oRow.find(oEl.selector),oEl.urlOrData,oEl.options)
}};
this.register=function(selector,urlOrData,options){var dynamic_selector=selector.replace(/^#(id_.+?)-.+?-(.+)$/,":input[id$=$2][id^=$1]");
if(dynamic_selector!=selector){if(!registered_selectors[selector]){dynamic.push({selector:dynamic_selector,urlOrData:urlOrData,options:options});
registered_selectors[dynamic_selector]=true
}}else{this.set_autocomplete($(selector),urlOrData,options);
registered_selectors[selector]=true
}};
this.set_autocomplete=function($oField,urlOrData,options){if($oField.length){$oField.unautocomplete().autocomplete(urlOrData,options).result(that.result);
$oField.click(function(){$(this).select()
}).blur(function(){var $oField=$(this);
var $oHidden=$("#"+$oField.attr("id").replace(/_text$/,""));
if(!$oField.val()){$oHidden.val("")
}})
}};
this.result=function(oEvent,aData,sFormatted){var $oField=$(this);
var $oHidden=$("#"+$oField.attr("id").replace(/_text$/,""));
if(aData){$oHidden.val(aData[1])
}else{$oHidden.val("")
}$oHidden.change();
$oHidden.blur()
};
this.formatItem=function(aRow){var sHtml='<span class="ac_title">'+aRow[0]+"</span>";
if(aRow[2]){sHtml+='<br /><span class="ac_description">'+aRow[2]+"</span>"
}return sHtml
};
this.test=function(){console.log(registered_selectors)
}
}self.AutocompleteManager=new AutocompleteManagerClass();
function AutocompleteMultipleManagerClass(){var that=this;
this.remove_item=function(){var $oLI=$(this).parent("li");
var sFieldID=$oLI.attr("id");
var aParts=sFieldID.split("-");
var $oHidden=$("#"+aParts[0].replace(/_value_pk$/,""));
var aPKs=$oHidden.val().split(",");
var aNewPKs=[];
for(i=0;
i<aPKs.length;
i++){if(aPKs[i]!=aParts[1]){aNewPKs.push(aPKs[i])
}}$oHidden.val(aNewPKs.join(","));
$oLI.slideUp("fast",function(){$(this).remove();
$oHidden.change()
});
return false
};
this.set_autocomplete=function($oField,urlOrData,options){if($oField.length){$oField.unautocomplete().autocomplete(urlOrData,options).result(that.result);
$oField.click(function(){$(this).select()
}).blur(function(){$(this).val("")
});
var $oList=$("#"+$oField.attr("id").replace(/_text$/,"_value_list"));
$oList.find("li").each(function(){var $oClosing=$('<a href="#"><span>×</span></a>').click(that.remove_item);
$(this).append($oClosing)
})
}};
this.result=function(oEvent,aData,sFormatted){var $oField=$(this);
var sFieldID=$oField.attr("id");
var $oHidden=$("#"+sFieldID.replace(/_text$/,""));
var sPKs=","+$oHidden.val()+",";
var aPKs=$oHidden.val()?$oHidden.val().split(","):[];
if(aData&&sPKs.indexOf(","+aData[1]+",")==-1){var $oList=$("#"+sFieldID.replace(/_text$/,"_value_list"));
if(!$oList.length){$oList=$('<ul id="'+sFieldID.replace(/_text$/,"_value_list")+'" class="ac_value_list"></ul>').insertBefore($oField)
}var $oLI=$('<li id="'+sFieldID.replace(/_text$/,"_value_pk-"+aData[1])+'"><span>'+aData[0]+" </span></li>");
var $oClosing=$('<a href="#"><span>×</span></a>').click(that.remove_item);
$oLI.hide();
$oList.append($oLI);
$oLI.append($oClosing);
aPKs.push(aData[1]);
$oHidden.val(aPKs.join(","));
$oField.val("").focus();
$oLI.slideDown("fast",function(){$oHidden.change();
$oField.focus()
})
}}
}AutocompleteMultipleManagerClass.prototype=new AutocompleteManagerClass();
AutocompleteMultipleManagerClass.prototype.constructor=AutocompleteMultipleManagerClass;
self.AutocompleteMultipleManager=new AutocompleteMultipleManagerClass();
$(document).ready(function(){self.AutocompleteManager.init();
self.AutocompleteMultipleManager.init()
});
$(window).unload(function(){self.AutocompleteManager=null;
self.AutocompleteMultipleManager=null
})
}(jQuery));