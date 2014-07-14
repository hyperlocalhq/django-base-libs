$j = jQuery;

self.JovotoManager = {
    sExtId: "",
    iActiveIndex: 0,
    init: function() {
        var oSelf = self.JovotoManager;
        // parse url
        var aUrlBits = window.website.path.substr(1).split("/");
        // aUrlBits[0] should be "jovoto"
        // aUrlBits[1] is the external Id of the idea
        oSelf.sExtId = aUrlBits[1];

        $j(".refuseComment a").click(oSelf.refuseComment);
        $j(".acceptComment a").click(oSelf.acceptComment);
        $j(".markAsSpamComment a").click(oSelf.markAsSpamComment);
        
        // init the commentManagers Url for Ajax Jovoto Comments
        self.CommentManager.setCommentAddUrl(oSelf.obj_dir() + "comments/add_ajax/");
        $j("img.contest-small").click(function() {
            var sSrc = $j(this).attr("src").replace(/_thumb\.([^.]+)$/, ".$1");
            $j("img.contest-big").attr("src", sSrc);
        });
    },
    
    obj_dir: function() {
      	var obj_dir = document.location.pathname.split(/$&\/(.+)$/im);
    	return obj_dir[0];
    },

    refuseComment: function() {
        var aM = $j(this).parent().addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);

        var iCommentId = aM[1];
        open_popup(
            gettext('Refuse Comment'),
            584, "auto",
            self.JovotoManager.obj_dir() + "helper/comment/" +  iCommentId + "/refuse/",
            true
        );
        return false;
    },
    
    acceptComment: function() {
        var aM = $j(this).parent().addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);

        var iCommentId = aM[1];
        
        open_popup(
            gettext('Accept Comment'),
            584, "auto",
            self.JovotoManager.obj_dir() + "helper/comment/" +  iCommentId + "/accept/",
            true
        );
        return false;
    },
    
    markAsSpamComment: function() {
        var aM = $j(this).parent().addClass(
            "in_progress"
        ).attr("id").match(/_(.+)$/);

        var iCommentId = aM[1];
        
        open_popup(
            gettext('Mark as Spam'),
            584, "auto",
            self.JovotoManager.obj_dir() + "helper/comment/" +  iCommentId + "/mark_as_spam/",
            true
        );
        return false;
        alert("xxx")
    },

    destruct: function() {
        self.JovotoManager = null;
    }
};

$j.get(
    settings.STATIC_URL + "site/js/website/comment.js",
    function(sData) {
        eval(sData);
        $j(document).ready(function(){
            self.JovotoManager.init();
        });
    }
);

$j(window).unload(function() {
    self.JovotoManager.destruct();
});
