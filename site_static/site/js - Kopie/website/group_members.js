$j = jQuery;

self.GroupMembersManager = {
    sSlug: "",
    iActiveIndex: 0,
    init: function() {
        var oSelf = self.GroupMembersManager;
        // parse url
        var aUrlBits = window.website.path.substr(1).split("/");
        // aUrlBits[0] should be "group"
        // aUrlBits[1] is the group slug
        oSelf.sSlug = aUrlBits[1];
        
        //alert("slug = " + oSelf.sSlug);
        
        // add onclick functions
        $j(".editMember a").click(oSelf.editMember);
    },
    
    editMember: function() {
        var aM = $j(this).parent("div").addClass(
            "in_progress"
        ).attr("id").match(/_(\d+)$/);
        var iUserId = aM[1];
		//alert("UserId =" + iUserId)
		
		var oSelf = self.GroupMembersManager;
        open_popup(
            gettext("Edit Group Member"),
            584, "auto",
            "/helper/edit-"+ settings.URL_ID_PERSONGROUP +"-member/" + oSelf.sSlug + "/" + iUserId + "/",
            false
        );
        return false;
    },
    
    destruct: function() {
        self.GroupMembersManager = null;
    },
};

if (self.open_popup || self._jquery_popup_loading) {
    $j(document).ready(function(){
        self.GroupMembersManager.init();
    });
} else {
    self._jquery_popup_loading = true;
    $j.get(
        settings.STATIC_URL + "site/js/jquery/jquery.popup.js",
        function(sData) {
            eval(sData);
            self._jquery_popup_loading = null;
            $j(document).ready(function(){
                self.GroupMembersManager.init();
            });
        }
    );
}
    
$j(window).unload(function() {
    self.GroupMembersManager.destruct();
});
