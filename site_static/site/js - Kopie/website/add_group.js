$j = jQuery;

self.GroupMainDataManager = {
    
    fillInContactData : true,
    
    init: function() {
        var oSelf = self.GroupMainDataManager;
        
        $j("#id_access_type").change(oSelf.showAccessType).change();
        $j(".access_type_desc dt").addClass("hidden");
    },
    showAccessType: function() {
        $j(".access_type_desc").hide()
        var sId = $j(this).val();
        if (sId) {
            $j("#access_type_desc_" + sId).slideDown();
        }
    },
    
    destruct: function() {
        self.GroupMainDataManager = null;
    }
};

$j(document).ready(function(){
    self.GroupMainDataManager.init();
});

$j(window).unload(function() {
    self.GroupMainDataManager.destruct();
});


