/* global self:false */
var gettext = window.gettext || function(text) {return text;};

(function($, undefined) {
    
    self.FavoriteManager = {
        sContextItemType: "",
        sSlug: "",
        sInnerTextToAdd: gettext("Add to favorites"),
        sTitleToAdd: gettext("Add to favorites"),
        sInnerTextToRemove: gettext("Remove from favorites"),
        sTitleToRemove: gettext("Remove from favorites"),
        init: function() {
            var oSelf = self.FavoriteManager; 
            $(document).on('click', '.favorite', function(e) {
                e.preventDefault();
                e.stopPropagation();
                oSelf.toggle($(this).get(), $(this).data('content_type_id'), $(this).data('object_id'));
            });
        },
        destruct: function() {
            self.FavoriteManager = null;
        },
        toggle: function(oElement, iCTId, oObjId) {
            $(oElement).addClass("progress").css({
                cursor: "wait"
            });
            $.get(
                "/helper/favorite/" + iCTId + "/" + oObjId + "/",
                function(oData) {
                    self.FavoriteManager.showResults(oData, oElement);
                },
                "JSON"
            );
        },
        showResults: function(oData, oElement) {
            var oSelf = self.FavoriteManager;
            var $oEl = $(oElement);
            if (oData) {
                var $oSpan = $oEl.children("span:first");
                if (oData.action === "added") {
                    $oEl.attr({
                        title: oSelf.sTitleToRemove
                    }).addClass("active");
                    $oSpan.html(oSelf.sInnerTextToRemove);
                    $oEl.attr("data-original-title",oSelf.sInnerTextToRemove);
                } else {
                    $oEl.attr({
                        title: oSelf.sTitleToAdd
                    }).removeClass("active");
                    $oSpan.html(oSelf.sInnerTextToAdd);
                    $oEl.attr("data-original-title",oSelf.sInnerTextToAdd);
                }
                if (oData.count !== undefined) {
                    $oEl.children(".favorites_count").text(oData.count);
                }
            }
            $oEl.removeClass("progress").css({cursor: "pointer"});
        }
    };
    $(document).ready(function(){
        self.FavoriteManager.init();
    });
    
    $(window).unload(function() {
        self.FavoriteManager.destruct();
    });
    
}(jQuery));
