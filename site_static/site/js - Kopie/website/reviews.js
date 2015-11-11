var $j = jQuery;

self.ReviewRatingManager = {
    init: function() {
        $j(".adding_to_review a").click(self.ReviewRatingManager.add);
    },
    add: function() {
        // add a class "in_progress" to the list item which contains the currently clicked link and parse the id of that list item
        var aM = $j(this).parent("li").addClass(
            "in_progress"
        ).attr("id").match(/_(\d+)_(\d+)$/);
        var iRateIndex = aM[1];
        var iReviewId = aM[2];
        // execute the rating
        $j.get(
            "/helper/reviews/" + iRateIndex + "/" + iReviewId + "/",
            new Function("sData", "self.ReviewRatingManager.showResults(sData, '" + iRateIndex + "', '" + iReviewId + "')")
        );
        return false;
    },
    showResults: function(sData, iRateIndex, iReviewId) {
        eval("oData = " + sData);
        if (oData) {
            // remove the class "in_progress" from the active list item
            var oLi = $j("#adding_to_review_" + iRateIndex + "_" + iReviewId).removeClass(
                "in_progress"
            );
            // change the link to a span
            oLi.children("a").replaceWith(
                $j("<span>").html(oLi.children("a").html())
            );
            // update the rating value
            oLi.children("span.review_rating_count").text(
                oData["rating" + iRateIndex]
            );
        }
    }
};

$j(document).ready(self.ReviewRatingManager.init);
