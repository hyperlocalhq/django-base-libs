(function($, undefined) {
    
    self.FavoriteManager = {
        sContextItemType: "",
        sSlug: "",
        sInnerTextToAdd: trans["Favorite"],
        sTitleToAdd: trans["Add to favorites"],
        sInnerTextToRemove: trans["Favorite"],
        sTitleToRemove: trans["Remove from favorites"],
        
        
        init: function() {
            var oSelf = self.FavoriteManager; 
            var aUrlBits = window.website.path.substr(1).split("/");
            // person|institution|event|document|group
            oSelf.sContextItemType = aUrlBits[0];
            var sLang = window.settings.lang;
            if (settings.URL_ID_INSTITUTION == oSelf.sContextItemType) {
                oSelf.sSlug = aUrlBits[1];
                $(
                    "#activity_" + sLang + " .navi_add-institution-to-favorites_" + sLang + ",#activity_" + sLang + " .navi_remove-institution-from-favorites_" + sLang
                ).click(function() {
                    $("#adding_to_favorites_0").click();
                    return false;
                });
            } else if (settings.URL_ID_DOCUMENT == oSelf.sContextItemType) {
                oSelf.sSlug = aUrlBits[1];
                var sLang = window.settings.lang;
                $(
                    "#activity_" + sLang + " .navi_add-document-to-favorites_" + sLang + ",#activity_" + sLang + " .navi_remove-document-from-favorites_" + sLang
                ).click(function() {
                    $("#adding_to_favorites_0").click();
                    return false;
                });
            }
        },
        destruct: function() {
            self.FavoriteManager = null;
        },
        toggle: function(iCounter, iCTId, oObjId) {
            $("#adding_to_favorites_" + iCounter).addClass("progress").css({
                cursor: "wait"
            });
            $.get(
                "/helper/favorite/" + iCTId + "/" + oObjId + "/",
                function(oData) {
                    self.FavoriteManager.showResults(oData, iCounter);
                },
                "JSON"
            );
            return false;
        },
        showResults: function(oData, iCounter) {
            var oSelf = self.FavoriteManager;
            var $oEl_class = $(".adding_to_favorites_" + iCounter);
            
            $oEl_class.each(function() {
               var $oEl = $(this);
               
                if (oData) {
                    $oSpan = $oEl.children("span").not(".dont-toggle-text").first();
                    var $counter = $oEl.children("span.counter");
                    
                    if (oData["action"] == "added") {
                        $oEl.attr({
                            title: oSelf.sTitleToRemove
                        }).addClass("active").addClass("on");
                        
                        if ($oSpan.hasClass('sr-only')) $oSpan.html(oSelf.sTitleToRemove);
                        else $oSpan.html(oSelf.sInnerTextToRemove);
                        
                        if ($counter.length) {
                            var count = parseInt($counter.text());
                            count++;
                            $counter.text(count);
                        }
                    } else {
                        $oEl.attr({
                            title: oSelf.sTitleToAdd
                        }).removeClass("active").removeClass("on");
                        
                        if ($oSpan.hasClass('sr-only')) $oSpan.html(oSelf.sTitleToAdd);
                        else $oSpan.html(oSelf.sInnerTextToAdd); 
                        
                        if ($counter.length) {
                            var count = parseInt($counter.text());
                            count--;
                            if (count < 0) count = 0;
                            $counter.text(count);
                        }
                    }
                    if (oData["count"] != undefined) {
                        $oEl.children(".favorites_count").text(oData["count"]);
                    }
                }
                $oEl.removeClass("progress").css({cursor: "pointer"});
               
            });
            
            var sLang = window.settings.lang;
            $("#activity_" + sLang).load(
                location.pathname + " #activity_" + sLang,
                oSelf.init
            );
        }
    };
    
    self.FavoriteContactManager = {
        sInnerTextToAdd: trans["Add contact"],
        sTitleToAdd: trans["Add contact"],
        sInnerTextToRemove: trans["It's your contact"],
        sTitleToRemove: trans["Remove contact"],
        init: function() {
        },
        destruct: function() {
            self.FavoriteContactManager = null;
        },
        toggle: function(iCounter, iCTId, oObjId) {
            $("#adding_to_favorites_" + iCounter).addClass("progress").css({
                cursor: "wait"
            });
            $.get(
                "/helper/favorite/" + iCTId + "/" + oObjId + "/",
                function(oData) {
                    self.FavoriteContactManager.showResults(oData, iCounter);
                },
                "JSON"
            );
            return false;
        },
        showResults: function(oData, iCounter) {
            var oSelf = self.FavoriteContactManager;
            var $oEl = $("#adding_to_favorites_" + iCounter);
            if (oData) {
                $oSpan = $oEl.children("span:first");
                if (oData["action"] == "added") {
                    $oEl.attr({
                        title: oSelf.sTitleToRemove
                    }).addClass("active");
                    $oSpan.html(oSelf.sInnerTextToRemove);
                } else {
                    $oEl.attr({
                        title: oSelf.sTitleToAdd
                    }).removeClass("active");
                    $oSpan.html(oSelf.sInnerTextToAdd);
                }
            }
            $oEl.removeClass("progress").css({cursor: "pointer"});
        }
    };
    
    self.MemoManager = {
        sInnerTextToAdd: trans["Add to Memo"],
        sTitleToAdd: trans["Add to Memo"],
        sInnerTextToRemove: trans["Remove Memo"],
        sTitleToRemove: trans["Remove Memo"],
        init: function() {
        },
        destruct: function() {
            self.MemoManager = null;
        },
        toggle: function(iCounter, iCTId, oObjId) {
            $("#adding_to_memos_" + iCounter).addClass("progress").css({
                cursor:"wait"
            });
            $.get(
                "/helper/memo/" + iCTId + "/" + oObjId + "/",
                function(oData) {
                    self.MemoManager.showResults(oData, iCounter);
                },
                "JSON"
            );
            return false;
        },
        showResults: function(oData, iCounter) {
            var oSelf = self.MemoManager;
            $oEl = $("#adding_to_memos_" + iCounter);
            if (oData) {
                $("ul.toolbar .memos .item_count").text(oData.memo_count);
                if (oData.memo_count == 0) {
                    $("ul.toolbar .memos").addClass("hidden");
                } else {
                    $("ul.toolbar .memos").removeClass("hidden");
                }
                $oSpan = $oEl.children("span:first");
                if (oData["action"] == "added") {
                    $oEl.attr({
                        title: oSelf.sTitleToRemove
                    }).addClass("active");
                    $oSpan.html(oSelf.sInnerTextToRemove);
                } else {
                    $oEl.attr({
                        title: oSelf.sTitleToAdd
                    }).removeClass("active");
                    $oSpan.html(oSelf.sInnerTextToAdd);
                    if (-1 != location.pathname.indexOf("/memos/")) {
                        $oSpan.parents(".info:first").fadeOut("normal").slideUp("normal", function() {
                            $(this).remove();
                            $(".info:odd").removeClass("odd even").addClass("odd");
                            $(".info:even").removeClass("odd even").addClass("even");
                        });
                    }
                }
            }
            $oEl.removeClass("progress").css({cursor: "pointer"});
        }
    };
    
    $(document).ready(function(){
        self.FavoriteManager.init();
        self.FavoriteContactManager.init();
        self.MemoManager.init();
    });
    
    $(window).unload(function() {
        self.FavoriteManager.destruct();
        self.FavoriteContactManager.destruct();
        self.MemoManager.destruct();
    });
    
}(jQuery));
