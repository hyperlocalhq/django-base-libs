(function($, undefined) {

    self.CommentManager = {
        sCommentAddUrl : "comments/add_ajax/",
        init: function() {
            var oSelf = self.CommentManager;
            
            
            /* cleanup all input values. this is needed, because we perform a page reload by
               document.location.reload(false) after submitting the comment. So, the forms
               have to be emptied!!
            */
            $("#id_name").val('');
            $("#id_email").val('');
            $("#id_url_link").val('');
            $("#id_comment").val('');
            
            // Comment form submit event for ajax comments
            $("#id_dyn_add_comment form").submit(
                oSelf.postAsAjax
            );
            $("#but_preview").click(oSelf.previewView);
            $("#but_post").click(oSelf.postView);
            $("#but_cancel").click(oSelf.cancelView);
        },
        
        postAsAjax: function() {
            var sUrl = self.CommentManager.sCommentAddUrl;
            var oValues = {};
            $(this).find(":input").each(function() {
                var $oElem = $(this);
                var sName = $oElem.attr("name");
                var sValue = $oElem.val();
                if (sName) {
                    if (!$oElem.is(":checkbox") || $oElem.attr("checked")) {
                        if (oValues[sName]) {
                            if (typeof(oValues[sName]) == "string") {
                                oValues[sName] = [oValues[sName]];
                            }
                            oValues[sName].push(sValue);
                        } else {
                            oValues[sName] = sValue;
                        }
                    }
                }
            });
            $.post(sUrl, oValues, self.CommentManager.updateView);
            return false;
        },
    
        cancelView: function() {
            var sUrl = self.CommentManager.sCommentAddUrl;
            $.get(sUrl, self.CommentManager.updateView);
        },
        
        previewView: function() {
            $(":submit[name=post]").attr("name", "");
            $(":submit[name=preview]").attr("name", "");
            $("#id_dyn_add_comment form").append(
                '<div><input type="hidden" name="preview" value="1" /></div>'
            ).submit();
            return false;
        },
        
        postView: function() {
            $(":submit[name=post]").attr("name", "");
            $(":submit[name=preview]").attr("name", "");
            $("#id_dyn_add_comment form").append(
                '<div><input type="hidden" name="post" value="1" /></div>'
            ).submit();
            return false;
        },
        
        updateView: function(sHtml) {
            //alert(sHtml);
            if(sHtml=="reload") {
                document.location.reload(false)
                //document.location.href = document.location.href;
            }
            else {
                $("#id_dyn_add_comment").html(sHtml);
            }
            
            $("#id_dyn_add_comment form").submit(self.CommentManager.postAsAjax);
            $("#but_preview").click(self.CommentManager.previewView);
            $("#but_post").click(self.CommentManager.postView);
            $("#but_cancel").click(self.CommentManager.cancelView);
        },
    
        setCommentAddUrl: function(sUrl) {
            self.CommentManager.sCommentAddUrl = sUrl
        },
        
        destruct: function() {
            self.CommentManager = null;
        }
    };
    
    $(document).ready(function(){
        self.CommentManager.init();
    });
    
    $(window).unload(function() {
        self.CommentManager.destruct();
    });

}(jQuery));
