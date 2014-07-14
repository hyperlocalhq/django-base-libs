(function($, undefined) {

self.PortfolioManager = {
    aThumbs: [],
    aThumb2Index: {},
    sContextItemType: "",
    sSlug: "",
    bInProgress: false,
    iActiveIndex: 0,
    iSlideshowTimeout: 5000,
    iSlideshowTimeoutHandle: null,
    init: function() {
        var oSelf = self.PortfolioManager;
        // parse url
        var aUrlBits = window.website.path.substr(1).split("/");
        // person|institution|event|document|group
        oSelf.sContextItemType = aUrlBits[0];
        // [.., "<slug>", "portfolio", ""]
        oSelf.sSlug = aUrlBits[1];
        var sFilename = document.location.hash.indexOf("#file_")==0?
            document.location.hash.substr(6): "";
        // parse list of photos
        // add onclick functions to them
        $("#dyn_portfolio").removeClass("hidden");
        var $media_thumb_links = $("#media_thumbs li").each(function() {
            $(this).find("a:first").click(oSelf.activate).map(oSelf.registerImage);
        });
        // check the currently selected
        if (sFilename && oSelf.aThumb2Index[sFilename]==null) {
            document.location.href = document.location.pathname;
        }
        // load if # defined
        $("#media_next").click(oSelf.activateNext);
        $("#media_previous").click(oSelf.activatePrevious);
        $("#media_slideshow_start").click(oSelf.startSlideshow);
        $("#media_slideshow_stop").click(oSelf.stopSlideshow);
        
        $("#media_delete").click(oSelf.deleteMediaFile);
        
        self.PortfolioManager.activate(sFilename);

        if ($media_thumb_links.length>1) {
            self.PortfolioManager.activate(sFilename);
            //oSelf.iSlideshowTimeoutHandle = setTimeout(
            //    oSelf.activateNextLoop,
            //    oSelf.iSlideshowTimeout
            //);
        } else {
            $("#media_previous,#media_next,"
                + "#media_slideshow_start,#media_slideshow_stop"
            ).addClass("hidden");
        }
        $("#media_slideshow_start").click();
    },
    destruct: function() {
        self.PortfolioManager = null;
    },
    registerImage: function() {
        var oSelf = self.PortfolioManager;
        var oLink = $(this);
        var sFilename = oLink.attr("href").split("#")[1].substr(5);
        oSelf.aThumb2Index[sFilename] = oSelf.aThumbs.length;
        oSelf.aThumbs[oSelf.aThumbs.length] = oLink;
        return oLink;
    },
    activatePrevious: function() {
        var oSelf = self.PortfolioManager;
        oSelf.stopSlideshow();
        if (oSelf.iActiveIndex > 0) {
            oSelf.aThumbs[oSelf.iActiveIndex-1].click();
        } else {
            return false;
        }
    },
    activateNext: function() {
        var oSelf = self.PortfolioManager;
        oSelf.stopSlideshow();
        if (oSelf.iActiveIndex < oSelf.aThumbs.length - 1) {
            oSelf.aThumbs[oSelf.iActiveIndex+1].click();
        } else {
            return false;
        }
    },
    startSlideshow: function() {
        var oSelf = self.PortfolioManager;
        $("#media_slideshow_start").addClass("hidden");
        $("#media_slideshow_stop").removeClass("hidden");
        oSelf.activateNextLoop();
        return false;
    },
    stopSlideshow: function() {
        var oSelf = self.PortfolioManager;
        $("#media_slideshow_start").removeClass("hidden");
        $("#media_slideshow_stop").addClass("hidden");
        clearTimeout(oSelf.iSlideshowTimeoutHandle);
        return false;
    },
    activateNextLoop: function() {
        var oSelf = self.PortfolioManager;
        if (oSelf.iActiveIndex < oSelf.aThumbs.length - 1) {
            oSelf.aThumbs[oSelf.iActiveIndex+1].click();
        } else {
            oSelf.aThumbs[0].click();
        }
        oSelf.iSlideshowTimeoutHandle = setTimeout(
            oSelf.activateNextLoop,
            oSelf.iSlideshowTimeout
        );
    },
    activate: function(sFilename) {
        var oSelf = self.PortfolioManager;
        if (oSelf.bInProgress) {
            return false;
        }
        oSelf.bInProgress = true;
        if (!oSelf.aThumbs.length) {
            return
        } 
        if (typeof(sFilename) != "string") {
            if (sFilename.pageX) {
                // if clicked manually
                oSelf.stopSlideshow();
            }
            sFilename = $(this).attr("href").split("#")[1].substr(5);
        }
        if (!sFilename) {
            sFilename = oSelf.aThumbs[0].attr("href").split("#")[1].substr(5);
        }
        // activate another thumbnail
        oSelf.aThumbs[oSelf.iActiveIndex].parent().removeClass("active");
        oSelf.iActiveIndex = oSelf.aThumb2Index[sFilename];
        oSelf.aThumbs[oSelf.iActiveIndex].parent().addClass("active");
        // hide existing image and description
        $('#dyn_media_file_container').css({
            height: $('#dyn_media_file_container').height()
        });
        $("#media_file .hidable").fadeOut("slow", function() {
            oSelf.getNewImage(sFilename);
        });
        return true;
    },
    getNewImage: function(sFilename) {
        var oSelf = self.PortfolioManager;
        var sToken = oSelf.aThumbs[oSelf.iActiveIndex].attr("href").split("#")[1].substr(5);
        $("#in_progress").show();
        $.get(
            location.pathname + sToken + "/json/",
            oSelf.showResults,
            "json"
        );
    },
    adjustHeight: function() {
        var oSelf = self.PortfolioManager;
        var iHeight = $('#dyn_media_file_height_measurer').height();
        if (iHeight) {
            $('#dyn_media_file_container').animate({
                height: iHeight
            }, "slow");
        } else {
            setTimeout(oSelf.adjustHeight, 500);
        } 
    },
    showResults: function(oData) {
        // show new image and description
        var oSelf = self.PortfolioManager;
        $("#in_progress").hide();
        
        $("#dyn_media_file_container").css("overflow", "hidden");
        
        $("#media_file_content").html(oData.html);
        $("#media_desc_content").html(oData.description);
        $("#media_file .hidable").fadeIn(oSelf.adjustHeight);
        
        // previous navigation
        if (oSelf.iActiveIndex > 0) {
            $("#media_previous>span").removeClass("disabled");
            $("#media_previous").attr("href", oSelf.aThumbs[oSelf.iActiveIndex-1].attr("href"));
        } else {
            $("#media_previous>span").addClass("disabled");
            $("#media_previous").attr("href", "");
        }
        // next navigation
        if (oSelf.iActiveIndex < oSelf.aThumbs.length - 1) {
            $("#media_next>span").removeClass("disabled");
            $("#media_next").attr("href", oSelf.aThumbs[oSelf.iActiveIndex+1].attr("href"));
        } else {
            $("#media_next>span").addClass("disabled");
            $("#media_next").attr("href", "");
        }
        // administration links
        $("#media_change").attr("href", document.location.pathname + "file_" + oData.token + "/");
        $("#media_delete").attr("href", document.location.pathname + "file_" + oData.token + "/delete/");
        oSelf.bInProgress = false;
    },
    deleteMediaFile: function() {
        var oSelf = self.PortfolioManager;
        var sToken = oSelf.aThumbs[oSelf.iActiveIndex].attr("href").split("#")[1].substr(5);
        open_popup(
            gettext("Delete Media File"),
            584, "auto",
            location.pathname + "file_" + sToken + "/popup_delete/",
            true
        );
        return false;
    }
};

$(document).ready(function(){
    self.PortfolioManager.init();
});

$(window).unload(function() {
    self.PortfolioManager.destruct();
});

}(jQuery));
