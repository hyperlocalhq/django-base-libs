/*
 * Thanks to Ludo van den Boom, 2008 and  Denis Howlett <denish@isocra.com>
 * 
 * Naming conventions: $VARNAME refers to a JQuery object and
 * 					   oVarname to a Dom object!!!!
 */

$j = jQuery;

if (self.TreeFilterMainManager) { // DEBUG
    alert("TreeFilter.js is included into this page twice. Please remove the duplicate from the template (probably {% block extrahead %}{% endblock %}).");
}

self.TreeFilterMainManager = {
    init: function() {
		
		$j("ul.tree_filter").each(function(){
			self.TreeFilterManager.initTree($j(this), {
				expandable: true,
				expand_level: 0,  
				indent: 15
			});
		});
	
		//find all selected item and expand the selected one!
		$j("ul.tree_filter li.selected").each(function(){
			var i = 0;
			var oParentArray = new Array();
			var oParent = self.TreeFilterManager.getParent($j(this)[0]);
			while (oParent) {
				oParentArray[i] = oParent;
				oParent = self.TreeFilterManager.getParent(oParent);
				i++;
			}
			for (i=0;i<oParentArray.length;i++) {
				self.TreeFilterManager.expand(oParentArray[oParentArray.length-i-1]);
			}
		});
	
		$j(".expand_all").click(function(){
			var aMatch = $j(this).attr("id").match(/expand_filter_(\d+_.+)/);
			if (aMatch != null) {
				var oUl = $j("#filter_" + aMatch[1])[0];
				self.TreeFilterManager.expandAll(oUl);
			}
		});

		$j(".collapse_all").click(function(){
			var aMatch = $j(this).attr("id").match(/collapse_filter_(\d+_.+)/);
			if (aMatch != null) {
				var oUl = $j("#filter_" + aMatch[1])[0];
				self.TreeFilterManager.collapseAll(oUl);
			}
		});

    },
    
	destruct: function() {
		self.TreeFilterMainManager = null;
	}
};  

self.TreeFilterManager = {
	opts : {},
	defaults : {
		expandable: true,
		expand_level: -1,  
		indent: 12
	},
	
    init: function() {},
    
    /* 
     * display treeview in table with expand and collapse icons 
     */ 
    initTree: function($ul, opts) {
       	var oSelf = self.TreeFilterManager;
       	
       	// Add class to enable styles specific to tree table.
		$ul.addClass("tree_filter");
       	
       	// setting the opts (from defaults and overriting with opts) 
       	oSelf.opts = $j.extend({}, oSelf.defaults, opts);

		//initially hide all rows.
		$j("li", $ul).each(function () {
			$j(this).hide();
		});
				
		// initialize roots (without recursion for fast inits (expandable)
		if(oSelf.opts.expandable) {
			oSelf.getRoots($ul[0]).each(function () {
				oSelf.initRow(this);
			});
			
		// ... and initialize roots with recursion (not expandable)
		} else {
			oSelf.getRoots($ul[0]).each(function () {
				oSelf.initSubtree(this);
			});
		}
    	
    	// initial expand to level...
    	oSelf.getRoots($ul[0]).each(function() {
    		oSelf.expandTo(this, oSelf.opts.expand_level);
    	});
    },
    
    /*
     * row inits
     */
    initRow: function(oRow) {
    	var oSelf = self.TreeFilterManager;
		var $Row = $j(oRow);
		var oParent = oSelf.getParent(oRow);
		
		// set correct indentation
		var $Cell = $j("div", oRow);
		var $ParentCell = $j("div", oParent);
		var iPadding = 0;
		$Cell.css("padding-left", 15);
		$j("a", oRow).css("display", "inline-block");
		//$j("a", oRow).css("padding-left", "0px!important");
		
		if (oParent) {
			iPadding += parseInt($ParentCell.css("padding-left")) + oSelf.opts.indent;
			$Cell.css("padding-left", iPadding + "px");
		}

		// for rows with children, add an expander icon!
		if(oSelf.hasChildren(oRow) && oSelf.opts.expandable) {
			// add expander icon and register click event!
			$j($Cell[0].lastChild).before('<span style="margin-left: -' + 12 + 'px; padding-left: ' + 12 + 'px" class="expander"></span>');
			
			$Row.addClass("collapsed");
			$j("span.expander", $Cell).click(function(){oSelf.toggle(oRow);});
		}
		// show the row, if it is not collapsed
		if (!(oParent && $j(oParent).is(".collapsed"))) {
			$Row.show();
		}
		
    },
    
    /* 
     * inits each row of a whole branch 
     */
    initSubtree: function(oRow) {
    	var oSelf = self.TreeFilterManager;
		var $Row = $j(oRow);
		oSelf.initRow(oRow);
		oSelf.childrenOf(oRow).each(function() {
			oSelf.initSubtree(this);
		});
    },
    
    /*
     * collapse all rows under a parent
     */
 	collapseAll: function(oUl) {
    	var oSelf = self.TreeFilterManager;
    	oSelf.getRoots(oUl).each(function() {
    		oSelf.collapse(this);
    	});
    },      
    
   	/* 
	 * Hide all descendants of a node. 
	 */
	collapse: function(oRow) {
		var oSelf = self.TreeFilterManager;
		var $Row = $j(oRow);
		$Row.removeClass("expanded");
		$Row.addClass("collapsed");
		
		oSelf.childrenOf(oRow).each(function() {
			var $Child = $j(this);
			// Recursively collapse any descending nodes too 
			$Child.removeClass("expanded");
			$Child.addClass("collapsed");
			oSelf.collapse(this);
			$Child.hide();
		});
	},

	/* 
	 * Show all children of a node. 
	 */
	expand: function(oRow) {
		var oSelf = self.TreeFilterManager;
		oSelf.expandTo(oRow, oSelf.getLevel(oRow)+1);
	},
	
	/* 
	 * Exapnd and show all children of a node 
	 * to a specified level. 
	 */
	expandTo: function(oRow, iToLevel) {
		var oSelf = self.TreeFilterManager;
		var $Row = $j(oRow);
		
		if (iToLevel != -1 && oSelf.getLevel(oRow) >= iToLevel)
			return;
		$Row.removeClass("collapsed");
		$Row.addClass("expanded");
		
		oSelf.childrenOf(oRow).each(function() {
			oSelf.initRow(this);
			$j(this).show();
			oSelf.expandTo(this, iToLevel);
		});
	},
	
	/*
	 * Expand all nodes of the tree
	 */
	expandAll: function(oUl) {
    	var oSelf = self.TreeFilterManager;
    	oSelf.getRoots(oUl).each(function() {
    		oSelf.expandTo(this, -1);
    	});
    },
	
	/* 
	 * Toggle a node 
	 */
	toggle: function(oRow) {
		var oSelf = self.TreeFilterManager;
		
		if($j(oRow).is(".expanded"))
			oSelf.collapse(oRow);
		else
			oSelf.expand(oRow);
	},
	
	/*
	 * get the roots of the tree
	 */
	getRoots: function(oList) {
		// roots are defined by having no class "cild-of-node-<<something>>"
		var $Roots = $j("li",  oList).not("[class*=child-of-filter]");
		return $Roots
	},
    
    /* 
     * if a node0 is a descendant of node1, return true, false otherwise 
     */ 
    isDescendantOf: function(oRow0, oRow1) {
    	var oSelf = self.TreeFilterManager;

		// I am a descendant of myself!
		if (oRow0 == oRow1)  
			return true;

		var	oCurrent = oRow0;
		var oParent = null;
    	while((oParent = oSelf.getParent(oCurrent)) != null) {
    		if (oParent == oRow1) {
    			return true;
    		}
    		oCurrent = oParent; 
    	}
    	return false;
    },
    
    /* 
     * gets all! descendants (recursively) of a row node 
     */
	getDescendants: function(oRow) {
		var oSelf = self.TreeFilterManager;
		var ret = [];
    	oSelf.childrenOf(oRow).each(function() {
        	ret.push(this);
        	oSelf.getDescendants($j(this)).each(function() {
        		ret.push(this);
        	});
	  	});
	  	return $j(ret);
	},

	/* 
	 * gets the level of a node 
	 */	
	getLevel: function(oRow) {
		var oSelf = self.TreeFilterManager;
		var oCurrent = oRow;
		var iLevel = 0;
		while (oCurrent = oSelf.getParent(oCurrent)) {
			iLevel++;
		}
		return iLevel;
	},

	/* 
	 * gets the parent node of a node (or null, if there is no parent) 
	 */
	getParent: function(oRow) {
		if (oRow) {
			var aMatch = $j(oRow).attr("class").match(/child-of-filter_(\d+)-node-(\d+)/);
			if (aMatch != null) {
				return $j("#filter_" + aMatch[1] + "-node-" + aMatch[2])[0];
			}
		} 
		return null;
	} ,
	
	/*
	 * checks, if a node has children.
	 * we could also use childrenOf.size, 
	 * but this one is better performing!
	 */
	hasChildren: function(oRow) {
		return $j(oRow).next().is(".child-of-" + $j(oRow)[0].id);
	},
	
	/* 
	 * Select all children of a node. 
	 */	
	childrenOf: function(oRow) {
		return $j("li.child-of-" + $j(oRow)[0].id);
	},
	
	destruct: function() {
		self.TreeFilterManager = null;
	}
};  
   
$j(document).ready(function(){
	self.TreeFilterMainManager.init();
    self.TreeFilterManager.init();
});

$j(window).unload(function() {
	self.TreeFilterMainManager.destruct();
    self.TreeFilterManager.destruct();
});

