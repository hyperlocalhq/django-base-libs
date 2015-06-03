$j = jQuery;

if (self.RelatedObjectSelectManager) { // DEBUG
    alert("RelatedObjectSelect.js is included into this page twice. Please remove the duplicate from the template (probably {% block extrahead %}{% endblock %}).");
}

self.RelatedObjectSelectManager = {
    init: function() {
    	var oSelf = self.RelatedObjectSelectManager;
    	// initial call of getting all content objects!!
    	$j(".related_object_ct_select").each(oSelf.initSelectFields);
    	// triggers the change event for the contenttype select box!
    	$j(".related_object_ct_select").change(oSelf.contentTypeGetObjects);
    },
    
    destruct: function() {
        self.RelatedObjectSelectManager = null;
    },
    
    initSelectFields: function() {
    	var oSelf = self.RelatedObjectSelectManager;

        var $oContentTypeSelect = $j(this);
        var aMatch = $oContentTypeSelect.attr("id").match(
            /^id_([^-]+-\d+-)?((.+)_)?content_type$/
        );
        var sFormsetPrefix = aMatch[1] || "";
        var sPrefix = aMatch[2] || "";
        var sObjectIdId = "id_" + sFormsetPrefix + sPrefix + "object_id"

        var $oText = $j("#" + sObjectIdId);
        $oText.addClass('vForeignKeyRawIdAdminField');

        var $oObjectSelectWidget = $('<a href="" class="related-lookup" id="lookup_' + sObjectIdId + '" onclick="return showRelatedObjectLookupPopup(this);"> <img src="' + settings.STATIC_URL + 'grappelli/img/admin/selector-search.gif" width="16" height="16" alt="Lookup"></a>');
        var oCT = MODEL_URL_ARRAY[$oContentTypeSelect.val()];
        if (oCT) {
            $oObjectSelectWidget.attr('href', '../../../' + oCT.app + '/' + oCT.model + '/?t=id');
        }
        $oText.after($oObjectSelectWidget);

        /*
        var sValue = $oText.attr("value");
        var $oSelect = $j('<select><option value="">---------</option></select>').attr({
            id: $oText.attr("id"),
            name: $oText.attr("name"),
        }).addClass("related_object_obj_id_select");
        $oText.replaceWith($oSelect);
        
		// now the ajax stuff!   
		if (sValue) { 	
	    	$oSelect.addClass("in_progress");
            // location.href.match(/\/[^\/]+\/[^\/]+\/\d+\/$/)
	        $j.get(
	            "/helper/objects_to_select" + location.href.match(/\/[^\/]+\/[^\/]+\/[^\/]+\/$/)[0] + $oSelect.attr("name") + "/of/" + $j(this).val() + "/",
	            new Function("sData", "self.RelatedObjectSelectManager.updateObjectIdOptions(sData, '" + $oSelect.attr("id") + "', '" + sValue + "' )")
	        );
	    }
	    */
    },
    
    contentTypeGetObjects: function($oThis) {
    	/* maybe there is more than (ct, obj_id) pair in the form present.
		but those pairs have all the ids id_<<prefix>>_content_type and
		id_<<prefix>>_object_id */
    	
        var $oContentTypeSelect = $j(this);
        var aMatch = $oContentTypeSelect.attr("id").match(
            /^id_([^-]+-\d+-)?((.+)_)?content_type$/
        );
        var sFormsetPrefix = aMatch[1] || "";
        var sPrefix = aMatch[2] || "";
        var sObjectIdId = "id_" + sFormsetPrefix + sPrefix + "object_id"

        var $oText = $j("#" + sObjectIdId);

        var $oObjectSelectWidget = $oText.next('.related-lookup');
        var oCT = MODEL_URL_ARRAY[$oContentTypeSelect.val()];
        if (oCT) {
            $oObjectSelectWidget.attr('href', '../../../' + oCT.app + '/' + oCT.model + '/?t=id');
        }

        /*
		// initial options for object Id field		
		var sOptions = "<option value=''>----------</option>";
	    $j("#" + sObjectIdId).html(sOptions);
		
		// now the ajax stuff!
		if ($j(this).val()) {
            $oSelect = $j("#" + sObjectIdId).addClass("in_progress").css({cursor: "wait"});
            // location.href.match(/\/[^\/]+\/[^\/]+\/\d+\/$/)
	        $j.get(
	            "/helper/objects_to_select" + location.href.match(/\/[^\/]+\/[^\/]+\/[^\/]+\/$/)[0] + $oSelect.attr("name") + "/of/" + $j(this).val() + "/",
	            new Function("sData", "self.RelatedObjectSelectManager.updateObjectIdOptions(sData, '" + sObjectIdId + "', '' )")
	        );
	    }
	    */
        return false;
    },

    updateObjectIdOptions: function(sData, sObjectIdId, sInitialValue) {
    	$j("#" + sObjectIdId).removeClass("in_progress").css({cursor: "pointer"});
    	eval("var aData = " + sData);
    	var sOptions = "<option value=''>----------</option>";
        var iLen = aData.length;
    	for(i=0; i<iLen; i++) {
            sKey = aData[i][0];
            sVal = aData[i][1];
    		sOptions += "<option value='" + sKey + "'";
    		if (sKey == sInitialValue)
				sOptions += " selected='selected'";
    		sOptions += ">" + sVal + "</option>";
		}
	    $j("#" + sObjectIdId).html(sOptions);
	}
};

$j(document).ready(function(){
    self.RelatedObjectSelectManager.init();
});

$j(window).unload(function() {
    self.RelatedObjectSelectManager.destruct();
});
