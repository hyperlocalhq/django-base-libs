$j = jQuery;

self.GalleryCommentsManager = {
    sSlug: "",
    iActiveIndex: 0,
    init: function() {
        var oSelf = self.GalleryCommentsManager;
        // parse url
        var aUrlBits = window.website.path.substr(1).split("/");
        // aUrlBits[0] should be "blog"
        // aUrlBits[1] is the person or institution slug or whatever slug
        oSelf.sSlug = aUrlBits[1];

        // disabled due to mockups 
        //$j(".editPost a").click(oSelf.editPost);
        $j(".refuseComment a").click(oSelf.refuseComment);
        $j(".acceptComment a").click(oSelf.acceptComment);
        $j(".markAsSpamComment a").click(oSelf.markAsSpamComment);
        
        // init the commentManagers Url for Ajax Blog Comments
        self.CommentManager.setCommentAddUrl(oSelf.obj_dir() + "comments/add_ajax/");
    },
    
    obj_dir: function() {
      	var obj_dir = document.location.pathname.split(/$&\/(.+)$/im);
    	return obj_dir[0];
    },
    
    rel_root_dir: function() {
      	return document.location.pathname.replace(
            /\/portfolio\/.+/,
            "/portfolio/"
        );
    },
    
    refuseComment: function() {
        var sLink = $(this).attr("href") + "use-popup/";
        open_popup(
            gettext('Refuse Comment'),
            584, "auto",
            sLink,
            true
        );
        return false;
    },
    
    acceptComment: function() {
        var sLink = $(this).attr("href") + "use-popup/";
        
        open_popup(
            gettext('Accept Comment'),
            584, "auto",
            sLink,
            true
        );
        return false;
    },
    
    markAsSpamComment: function() {
        var sLink = $(this).attr("href") + "use-popup/";
        
        open_popup(
            gettext('Mark as Spam'),
            584, "auto",
            sLink,
            true
        );
        return false;
    },

    destruct: function() {
        self.GalleryCommentsManager = null;
    }
};

$j(document).ready(function(){
    self.GalleryCommentsManager.init();
});

$j(window).unload(function() {
    self.GalleryCommentsManager.destruct();
});
