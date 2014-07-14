(function($,undefined){self.CommentManager={sCommentAddUrl:"comments/add_ajax/",init:function(){var oSelf=self.CommentManager;
$("#id_name").val("");
$("#id_email").val("");
$("#id_url_link").val("");
$("#id_comment").val("");
$("#id_dyn_add_comment form").submit(oSelf.postAsAjax);
$("#but_preview").click(oSelf.previewView);
$("#but_post").click(oSelf.postView);
$("#but_cancel").click(oSelf.cancelView)
},postAsAjax:function(){var sUrl=self.CommentManager.sCommentAddUrl;
var oValues={};
$(this).find(":input").each(function(){var $oElem=$(this);
var sName=$oElem.attr("name");
var sValue=$oElem.val();
if(sName){if(!$oElem.is(":checkbox")||$oElem.attr("checked")){if(oValues[sName]){if(typeof(oValues[sName])=="string"){oValues[sName]=[oValues[sName]]
}oValues[sName].push(sValue)
}else{oValues[sName]=sValue
}}}});
$.post(sUrl,oValues,self.CommentManager.updateView);
return false
},cancelView:function(){var sUrl=self.CommentManager.sCommentAddUrl;
$.get(sUrl,self.CommentManager.updateView)
},previewView:function(){$(":submit[name=post]").attr("name","");
$(":submit[name=preview]").attr("name","");
$("#id_dyn_add_comment form").append('<div><input type="hidden" name="preview" value="1" /></div>').submit();
return false
},postView:function(){$(":submit[name=post]").attr("name","");
$(":submit[name=preview]").attr("name","");
$("#id_dyn_add_comment form").append('<div><input type="hidden" name="post" value="1" /></div>').submit();
return false
},updateView:function(sHtml){if(sHtml=="reload"){document.location.reload(false)
}else{$("#id_dyn_add_comment").html(sHtml)
}$("#id_dyn_add_comment form").submit(self.CommentManager.postAsAjax);
$("#but_preview").click(self.CommentManager.previewView);
$("#but_post").click(self.CommentManager.postView);
$("#but_cancel").click(self.CommentManager.cancelView)
},setCommentAddUrl:function(sUrl){self.CommentManager.sCommentAddUrl=sUrl
},destruct:function(){self.CommentManager=null
}};
$(document).ready(function(){self.CommentManager.init()
});
$(window).unload(function(){self.CommentManager.destruct()
})
}(jQuery));
(function($,undefined){self.BlogManager={sSlug:"",iActiveIndex:0,init:function(){var oSelf=self.BlogManager;
var aUrlBits=window.website.path.substr(1).split("/");
oSelf.sSlug=aUrlBits[1];
$(".deletePost a").click(oSelf.deletePost);
$(".refuseComment a").click(oSelf.refuseComment);
$(".acceptComment a").click(oSelf.acceptComment);
$(".markAsSpamComment a").click(oSelf.markAsSpamComment);
if(self.CommentManager){self.CommentManager.setCommentAddUrl(oSelf.obj_dir()+"comments/add_ajax/")
}},obj_dir:function(){var obj_dir=document.location.pathname.split(/$&\/(.+)$/im);
return obj_dir[0]
},rel_root_dir:function(){var root_dir=document.location.pathname.split(/blog(.+)$/);
return root_dir[0]+"blog/"
},editPost:function(){var aM=$(this).parent("li").addClass("in_progress").attr("id").match(/_(.+)$/);
var iPostSlug=aM[1];
open_popup(gettext("Edit Post"),532,"auto",self.BlogManager.rel_root_dir()+"helper/post/"+iPostSlug+"/edit/",false);
return false
},deletePost:function(){},refuseComment:function(){var aM=$(this).parent().attr("id").match(/_(.+)$/);
var iCommentId=aM[1];
open_popup(gettext("Refuse Comment"),532,"auto",self.BlogManager.rel_root_dir()+"helper/comment/"+iCommentId+"/refuse/",true);
return false
},acceptComment:function(){var aM=$(this).parent().attr("id").match(/_(.+)$/);
var iCommentId=aM[1];
open_popup(gettext("Accept Comment"),532,"auto",self.BlogManager.rel_root_dir()+"helper/comment/"+iCommentId+"/accept/",true);
return false
},markAsSpamComment:function(){var aM=$(this).parent().attr("id").match(/_(.+)$/);
var iCommentId=aM[1];
open_popup(gettext("Mark as Spam"),532,"auto",self.BlogManager.rel_root_dir()+"helper/comment/"+iCommentId+"/mark_as_spam/",true);
return false
},destruct:function(){self.BlogManager=null
}};
$(document).ready(function(){self.BlogManager.init()
});
$(window).unload(function(){self.BlogManager.destruct()
})
}(jQuery));