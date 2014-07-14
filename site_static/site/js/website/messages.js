$j = jQuery;

self.MessageActionManager = {
    init: function() {
    	$j(".adding_to_review a").click(self.MessageActionManager.add);
    	
    	// cancel the action
    	$j("#id_ask_sure_no").click(function() {
    		self.MessageActionManager.showHideSureButtons(false)
   		});
   		
   		// perform the action
    	$j("#id_ask_sure_yes").click(function() {
    		self.MessageActionManager.performAction()
   		});
   		   		
    	// the action for the "action" selectbox
    	$j("#id_action").change(function() {
    		if ($j(this).val() != "none")
    			self.MessageActionManager.showHideSureButtons(true);
    		else
    			self.MessageActionManager.showHideSureButtons(false);
   		});
   		
   		// toggle "choose all"
    	$j("#id_choose_all").change(function() {
    		self.MessageActionManager.showHideSureButtons(false);
    	    if ($j(this).attr("checked")) {
    	    	$j("#checkboxes_div_id input").attr("checked", "checked");
  			} else {
  				$j("#checkboxes_div_id input").removeAttr( "checked" );
  			}
   		});
	},
	
	showHideSureButtons: function(show) {
		if (show) 
    		$j("#id_ask_sure").show()
    	else 
    		$j("#id_ask_sure").hide()
    },
	
	performAction: function() {
		var action = $j("#id_action").val();
	
		var sIdList = ""
		$j("#checkboxes_div_id input[checked]").each(
			function( intIndex ){
				// get the ids from action_id. They are formed by "action_" + << id >>
				var nId = $j(this).attr("id").substring(7, $j(this).attr("id").length);
			 	sIdList += nId + " "
			} 
		)
		$j.get(
  		   "/my-messages/json/",
    	   {
        	  action: action,
        	  idlist: sIdList
    	   },
    	   new Function("sData", "self.MessageActionManager.showResults(sData)")
		);
		return false;
	},
    
    showResults: function(sData) {
    	// TODO currently not used, because we make a full page reload here!
        eval("oData = " + sData);
        
        // TODO maybe we want some ajax stuff here    
        window.location.reload();
        self.MessageActionManager.showHideSureButtons(false);
        // uncheck all checkboxes
        $j("#id_choose_all").removeAttr( "checked" );
        $j("#checkboxes_div_id input").removeAttr( "checked" );
    }
};

$j(document).ready(self.MessageActionManager.init);
