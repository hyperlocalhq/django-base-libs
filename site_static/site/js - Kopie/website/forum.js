$j = jQuery;

self.ForumManager = {
    sSlug: "",
    iActiveIndex: 0,
    init: function() {
        var oSelf = self.ForumManager;
        // parse url
        var aUrlBits = window.website.path.substr(1).split("/");
        // aUrlBits[0] should be "group"
        // aUrlBits[1] is the group slug
        oSelf.sSlug = aUrlBits[1];

        // add onclick functions
        $j(".newForumCategory a").click(oSelf.newForumCategory);
        $j(".editForumCategory a").click(oSelf.editForumCategory);
        $j(".deleteForumCategory a").click(oSelf.deleteForumCategory);
        
        $j(".newThreadCategory a").click(oSelf.newThreadCategory);
        $j(".editThreadCategory a").click(oSelf.editThreadCategory);
        $j(".deleteThreadCategory a").click(oSelf.deleteThreadCategory);
        
        $j(".newThread a").click(oSelf.newThread);
        $j(".editThread a").click(oSelf.editThread);
        $j(".deleteThread a").click(oSelf.deleteThread);
        
        $j(".editPost a").click(oSelf.editPost);
        $j(".deletePost a").click(oSelf.deletePost);
        $j(".refusePost a").click(oSelf.refusePost);
        $j(".mark_as_spamPost a").click(oSelf.markAsSpamPost);
        
    },
    
    rel_root_dir: function() {
      	var root_dir = document.location.pathname.split(/forum(.+)$/);
    	return root_dir[0] + "forum/";
    },
    
    newForumCategory: function() {
        open_popup(
            gettext('New Forum Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/forum-category/new/",
            false
        );
        return false;
    },
    
    editForumCategory: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        var iForumCategorySlug = aM[1];
		
        open_popup(
            gettext('Edit Forum Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/forum-category/" + iForumCategorySlug + "/edit/",
            false
        );
        return false;
    },
    
    deleteForumCategory: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        var iForumCategorySlug = aM[1];
		
        open_popup(
            gettext('Delete Forum Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/forum-category/" + iForumCategorySlug + "/delete/",
            true
        );
        return false;
    },
    
    newThreadCategory: function() {
        open_popup(
            gettext('New Thread Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread-category/new/",
            false
        );
        return false;
    },
    
    editThreadCategory: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
		var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
		
        open_popup(
            gettext('Edit Thread Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread-category/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/edit/",
            false
        );
        return false;
    },

    deleteThreadCategory: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
		
        open_popup(
            gettext('Delete Thread Category'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread-category/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/delete/",
            true
        );
        return false;
    },
 
   newThread: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        open_popup(
            gettext('New Thread'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/new/",
            false
        );
        return false;
    },
    
    editThread: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        open_popup(
            gettext('Edit Thread'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/edit/",
            false
        );
        return false;
    },

    deleteThread: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        open_popup(
            gettext('Delete Thread'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/thread/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/delete/",
            true
        );
        return false;
    },
    
    editPost: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        var iPostId = iBits[3];
        
        open_popup(
            gettext('Edit Comment'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/post/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/post" + iPostId + "/edit/",
            false
        );
        return false;
    },

    deletePost: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        var iPostId = iBits[3];
        open_popup(
            gettext('Delete Post'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/post/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/post" + iPostId + "/delete/",
            true
        );
        return false;
    },
    
    refusePost: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        var iPostId = iBits[3];
        open_popup(
            gettext('Refuse Post'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/post/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/post" + iPostId + "/refuse/",
            true
        );
        return false;
    },
    
    markAsSpamPost: function() {
        var aM = $j(this).parent("span").addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);
        
        var iBits = aM[1].split('__');
        var iForumCategorySlug = iBits[0];
        var iThreadCategorySlug = iBits[1];
        var iThreadSlug = iBits[2];
        var iPostId = iBits[3];
        open_popup(
            gettext('Mark Post as Spam'),
            584, "auto",
            self.ForumManager.rel_root_dir() + "helper/post/" + iForumCategorySlug + "/" + iThreadCategorySlug + "/" + iThreadSlug + "/post" + iPostId + "/mark_as_spam/",
            true
        );
        return false;
    },

    destruct: function() {
        self.ForumManager = null;
    }
};

if (self.open_popup || self._jquery_popup_loading) {
    $j(document).ready(function(){
        self.ForumManager.init();
    });
} else {
    self._jquery_popup_loading = true;
    $j.get(
        settings.STATIC_URL + "site/js/jquery/jquery.popup.js",
        function(sData) {
            eval(sData);
            self._jquery_popup_loading = null;
            $j(document).ready(function(){
                self.ForumManager.init();
            });
        }
    );
}

$j(window).unload(function() {
    self.ForumManager.destruct();
});
