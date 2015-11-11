$j = jQuery;

self.CollapsableSearchForm = {
    leafClass: "no-children",
    openedClass: "children-opened",
    closedClass: "children-closed",
    init: function() {
        var oF = self.CollapsableSearchForm;
        var oLi = $j("form.search_form div.categories li");
        var aChecks = oLi.children("input[type=checkbox]").each(function(){
            var oCheck = $j(this);
            var oUl = oCheck.nextAll("ul");
            var oA = oUl.prevAll("a");
            if (oUl.length) {
                oCheck.click(oF.toggle);
                oA.click(oF.toggle);
                oCheck.siblings("label").click(oF.toggle);
                oA.removeClass(
                    oF.leafClass
                ).removeClass(
                    oF.openedClass
                ).addClass(
                    oF.closedClass
                ).children("span").text(">");
            }
            if (oCheck.attr("checked")) {
                oF.expand(oUl);
            }
        });
    },
    destruct: function() {
        self.CollapsableSearchForm = null;
    },
    toggle: function() {
        var oF = self.CollapsableSearchForm;
        var aFields = $j(this).parent().children("input, ul");
        var oCheck = $j(aFields[0]);
        var oUl = $j(aFields[1]);
        var bBubble = true;
        if ($j(this).is("a")) {
            oCheck.attr("checked", !oCheck.attr("checked"));
            bBubble = false;
        }
        if (oCheck.attr("checked")) {
            oF.expand(oUl);
        } else {
            oF.collapse(oUl);
        }
        return bBubble;
    },
    collapse: function(oUl) {
        var oF = self.CollapsableSearchForm;
        oUl.slideUp("normal");
        oUl.find("input[type=checkbox]").attr("checked", false);
        oA = oUl.siblings("a");
        if (!oA.is("." + oF.leafClass)) {
            oA.removeClass(
                oF.openedClass
            ).addClass(
                oF.closedClass
            ).children("span").text(">");
        }
    },
    expand: function(oUl) {
        var oF = self.CollapsableSearchForm;
        oUl.slideDown("normal");
        oA = oUl.siblings("a");
        if (!oA.is("." + oF.leafClass)) {
            oA.removeClass(
                oF.closedClass
            ).addClass(
                oF.openedClass
            ).children("span").text("v");
        }
    }
}

$j(document).ready(self.CollapsableSearchForm.init);
$j(window).unload(self.CollapsableSearchForm.destruct);
