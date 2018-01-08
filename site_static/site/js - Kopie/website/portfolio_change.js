(function($, undefined) {

    self.PortfolioChangeManager = {
        init: function() {
            var oSelf = self.PortfolioChangeManager;
            
            $("#link_to_media_file_switcher").click(function() {
                return oSelf.switch_to_section("#link_to_media_file");
            });
            $("#upload_media_file_switcher").click(function() {
                return oSelf.switch_to_section("#upload_media_file");
            });
            
            var sSection = document.location.hash;
            if (sSection != "#link_to_media_file" && !$("#id_external_url").val()) {
                sSection = "#upload_media_file";
            } else {
                sSection = "#link_to_media_file";
            }
            oSelf.switch_to_section(sSection);
        },
        switch_to_section: function(sSection) {
            $("#link_to_media_file,#upload_media_file").hide();
            $(sSection).show();
            return false;
        },
        destruct: function() {
            self.PortfolioChangeManager = null;
        }
    };
    
    $(document).ready(function(){
        self.PortfolioChangeManager.init();
    });
    
    $(window).unload(function() {
        self.PortfolioChangeManager.destruct();
    });
    
}(jQuery));
