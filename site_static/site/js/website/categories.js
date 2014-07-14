(function($, undefined) {

    self.CategoryManager = {
        init: function() {
            var oF = self.CategoryManager;
            var $oLi = $("div.categories li");
            var aChecks = $oLi.find(":checkbox").each(function(){
                var $oCheck = $(this);
                if ($oCheck.attr("id").match(/^id_[A-Z]{2}_\d+$/)) {
                    var $oLabel = $oCheck.parents("label");
                    var $oUl = $oLabel.nextAll("ul");
                    var $oA = $oLabel.prevAll("a");
                    if ($oUl.length) {
                        $oCheck.click(oF.toggle);
                        $oA.click(oF.toggle);
                        $oA.removeClass(
                            "no-children"
                        ).removeClass(
                            "children-opened"
                        ).addClass(
                            "children-closed"
                        ).children("span").html("&rarr;");
                        $oUl.hide();
                    } else {
                        $oA.click(function() {return false});
                        $oCheck.click(function() {
                            $(this).parents("li").children('label').children(":checkbox").not(this).attr("checked", true);
                        });
                    }
                    if ($oCheck.attr("checked")) {
                        oF.expand($oUl);
                    }
                }
            });
        },
        toggle: function() {
            var oF = self.CategoryManager;
            var $aFields = $(this).parents("li").children("label, ul");
            var $oCheck = $($aFields[0]).children(":checkbox");
            var $oUl = $($aFields[1]);
            var bBubble = true;
            if ($(this).is(":checkbox")) {
                $oCheck.parent().parents("li").children(":checkbox").attr("checked", true);
            }
            if ($(this).is("a")) {
                if ($oUl.is(":hidden")) {
                    oF.expand($oUl);
                } else {
                    oF.collapse($oUl);
                }
                bBubble = false;
            } else {
                if ($oCheck.attr("checked")) {
                    oF.expandAndCheck($oUl);
                } else {
                    oF.collapseAndUncheck($oUl);
                }
            }
            return bBubble;
        },
        collapseAndUncheck: function(oUl) {
            var oF = self.CategoryManager;
            oUl.slideUp("normal");
            oUl.find(":checkbox").attr("checked", false);
            oA = oUl.siblings("a");
            if (!oA.is(".no-children")) {
                oA.removeClass(
                    "children-opened"
                ).addClass(
                    "children-closed"
                ).children("span").html("&rarr;");
            }
        },
        expandAndCheck: function(oUl) {
            var oF = self.CategoryManager;
            oUl.slideDown("normal");
            oA = oUl.siblings("a");
            if (!oA.is(".no-children")) {
                oA.removeClass(
                    "children-closed"
                ).addClass(
                    "children-opened"
                ).children("span").html("&darr;");
            }
        },
        collapse: function(oUl) {
            var oF = self.CategoryManager;
            oUl.slideUp("normal");
            oA = oUl.siblings("a");
            if (!oA.is(".no-children")) {
                oA.removeClass(
                    "children-opened"
                ).addClass(
                    "children-closed"
                ).children("span").html("&rarr;");
            }
        },
        expand: function(oUl) {
            var oF = self.CategoryManager;
            oUl.slideDown("normal");
            oA = oUl.siblings("a");
            if (!oA.is(".no-children")) {
                oA.removeClass(
                    "children-closed"
                ).addClass(
                    "children-opened"
                ).children("span").html("&darr;");
            }
        },
        destruct: function() {
            self.CategoryManager = null;
        }
    };
    
    $(document).ready(function() {
        self.CategoryManager.init();
    });
        
    $(window).unload(self.CategoryManager.destruct);
    
}(jQuery));
