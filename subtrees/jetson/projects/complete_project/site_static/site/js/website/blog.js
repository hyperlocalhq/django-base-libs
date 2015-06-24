(function($, undefined) {

    self.BlogManager = {
        sSlug: "",
        iActiveIndex: 0,
        init: function() {
            var oSelf = self.BlogManager;
            // parse url
            var aUrlBits = window.website.path.substr(1).split("/");
            // aUrlBits[0] should be "blog"
            // aUrlBits[1] is the person or institution slug or whatever slug
            oSelf.sSlug = aUrlBits[1];
    
            // disabled due to mockups 
            //$(".editPost a").click(oSelf.editPost);
            $(".deletePost a").click(oSelf.deletePost);
            $(".refuseComment a").click(oSelf.refuseComment);
            $(".acceptComment a").click(oSelf.acceptComment);
            $(".markAsSpamComment a").click(oSelf.markAsSpamComment);
            
            // init the commentManagers Url for Ajax Blog Comments
            if (self.CommentManager) {
                self.CommentManager.setCommentAddUrl(oSelf.obj_dir() + "comments/add_ajax/");
            }
        },
        
        obj_dir: function() {
            var obj_dir = document.location.pathname.split(/$&\/(.+)$/im);
            return obj_dir[0];
        },
        
        rel_root_dir: function() {
            var root_dir = document.location.pathname.split(/blog(.+)$/);
            return root_dir[0] + "blog/";
        },
        
        editPost: function() {
            var aM = $(this).parent("li").addClass(
                "in_progress"
            ).attr("id").match(/_(.+)$/);
    
            var iPostSlug = aM[1];
            
            open_popup(
                gettext('Edit Post'),
                532, "auto",
                self.BlogManager.rel_root_dir() + "helper/post/" +  iPostSlug + "/edit/",
                false
            );
            return false;
        },
    
        deletePost: function() {
            /*
            var aM = $(this).parent("li").addClass(
                "in_progress"
            ).attr("id").match(/_(.+)$/);
    
            var iPostSlug = aM[1];
            
            open_popup(
                gettext('Delete Post'),
                532, "auto",
                self.BlogManager.rel_root_dir() + "helper/post/" +  iPostSlug + "/delete/",
                true
            );
            return false;
            */
        },
        
        refuseComment: function() {
            var aM = $(this).parent().attr("id").match(/_(.+)$/);
            var iCommentId = aM[1];
            
            open_popup(
                gettext('Refuse Comment'),
                532, "auto",
                self.BlogManager.rel_root_dir() + "helper/comment/" +  iCommentId + "/refuse/",
                true
            );
            return false;
        },
        
        acceptComment: function() {
            var aM = $(this).parent().attr("id").match(/_(.+)$/);
            var iCommentId = aM[1];        
            
            open_popup(
                gettext('Accept Comment'),
                532, "auto",
                self.BlogManager.rel_root_dir() + "helper/comment/" +  iCommentId + "/accept/",
                true
            );
            return false;
        },
        
        markAsSpamComment: function() {
            var aM = $(this).parent().attr("id").match(/_(.+)$/);
            var iCommentId = aM[1];        
            
            open_popup(
                gettext('Mark as Spam'),
                532, "auto",
                self.BlogManager.rel_root_dir() + "helper/comment/" +  iCommentId + "/mark_as_spam/",
                true
            );
            return false;
        },
    
        destruct: function() {
            self.BlogManager = null;
        }
    };
    
    $(document).ready(function(){
        self.BlogManager.init();
    });
    
    $(window).unload(function() {
        self.BlogManager.destruct();
    });

}(jQuery));
