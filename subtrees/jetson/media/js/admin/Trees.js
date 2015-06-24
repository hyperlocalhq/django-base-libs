/*
 * Thanks to Ludo van den Boom, 2008 and  Denis Howlett <denish@isocra.com>
 * 
 * Naming conventions: $VARNAME refers to a JQuery object and
 * 					   oVarname to a Dom object!!!!
 */

$j = jQuery;

if (self.TreeMainManager) { // DEBUG
    alert("Tree.js is included into this page twice. Please remove the duplicate from the template (probably {% block extrahead %}{% endblock %}).");
}

self.TreeMainManager = {
    init: function() {

		var $Table = $j("#tree");
		
		self.TreeManager.initTreeTable($Table, {
			expandable: true,
			expand_level: 0,  
			indent: 18
		});
		
		if ($j("#tree_data").hasClass("dragdrop_allowed")) {
			self.TreeDnDManager.makeDraggable($Table, {
				scrollAmount: 6,
				// level-"sensitivity" for dragging left and right in px
				// should be set between 10, and 20
				hDragInterval: 10,
				// should be set between 1 and 8
				vDragInterval: 5,
			});
			
			/* catch save button: write tree data to a hidden field
			 * and the process submit as usual....
			 */
			$j(".save_all").click(function(){
				$j("#tree_data").val(self.TreeDnDManager.serialize($j("#tree")));
                $j(this).closest('form').submit();
                return false;
			});
		}
		
		$j(".expand_all").click(function(){
			self.TreeManager.expandAll();
		});

		$j(".collapse_all").click(function(){
			self.TreeManager.collapseAll();
		});
    },
    
	destruct: function() {
		self.TreeMainManager = null;
	}
};  

self.TreeManager = {
	// Keep hold of the current table being dragged
    oCurrentTable : null,
    
	bMouseDown : false,
	
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
    initTreeTable: function($Table, opts) {
       	var oSelf = self.TreeManager;
       	
       	oSelf.oCurrentTable = $Table[0];
       	
       	// Add class to enable styles specific to tree table.
		$Table.addClass("tree_table");
		
       	// setting the opts (from defaults and overriting with opts) 
       	oSelf.opts = $j.extend({}, oSelf.defaults, opts);

		//initially hide all rows.
		$j("tbody tr", $Table).each(function () {
			$j(this).hide();
		});
				
		// initialize roots (without recursion for fast inits (expandable)
		if(oSelf.opts.expandable) {
			oSelf.getRoots(oSelf.oCurrentTable).each(function () {
				oSelf.initRow(this);
			});
		// ... and initialize roots with recursion (not expandable)
		} else {
			oSelf.getRoots(oSelf.oCurrentTable).each(function () {
				oSelf.initSubtree(this);
			});
		}
		
		// bind expand/collapse mouse actions    
    	$Table.mousedown(function() {oSelf.bMouseDown = true;});
    	$Table.mouseup(function() {oSelf.bMouseDown = false;});
    	
		// hovering a node marks all subnodes  
		$j("tbody tr th", $Table).hover(function() {
			var $Row = $j(this).parent();
			if (!TreeDnDManager.bMouseDown) {
				oSelf.getDescendants($Row[0]).each(function() {
					$j(this).addClass("showHoverHandleChildren");
				});
				$Row.addClass('showHoverHandle');
			}
    	}, function() {
    		var $Row = $j(this).parent();
    		if (!TreeDnDManager.bMouseDown) {
				oSelf.getDescendants($Row[0]).each(function() {
					$j(this).removeClass("showHoverHandleChildren");
				});
	    		$Row.removeClass('showHoverHandle');
    		}
    	});
    	
    	// initial expand to level...
    	oSelf.getRoots(oSelf.oCurrentTable).each(function() {
    		oSelf.expandTo(this, oSelf.opts.expand_level);
    	});
    },
    
    /*
     * row inits
     */
    initRow: function(oRow) {
    	var oSelf = self.TreeManager;
		var $Row = $j(oRow);
		var oParent = oSelf.getParent(oRow);

		// filtered out ones get a special class
		if ($j("th span", oRow).hasClass("filtered_out")) {
			$Row.addClass("filtered_out");
		}
		
		// remove "expander icons". There may be some left from DnD
		$j("span.expander", oRow).remove();

		// set correct indentation
		var $Cell = $j("th", oRow);
		var $ParentCell = $j("th", oParent);
		var iPadding = 0;
		$Cell.css("cssText", "padding-left: 24px !important;");
		if (oParent) {
			iPadding += parseInt($ParentCell.css("padding-left")) + oSelf.opts.indent;
			$Cell.css("cssText", "padding-left: " + iPadding + "px !important");
		}

		// for rows with children, add an expander icon!
		if(oSelf.hasChildren(oRow) && oSelf.opts.expandable) {
			// add expander icon and register click event!
			$j($Cell[0].lastChild).before('<span style="margin-left: -' + oSelf.opts.indent + 'px; padding-left: ' + oSelf.opts.indent + 'px" class="expander"></span>');
			
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
    	var oSelf = self.TreeManager;
		var $Row = $j(oRow);
		oSelf.initRow(oRow);
		oSelf.childrenOf(oRow).each(function() {
			oSelf.initSubtree(this);
		});
    },
    
    /*
     * collapse all rows under a parent
     */
 	collapseAll: function() {
    	var oSelf = self.TreeManager;
    	oSelf.getRoots(oSelf.oCurrentTable).each(function() {
    		oSelf.collapse(this);
    	});
    },      
    
   	/* 
	 * Hide all descendants of a node. 
	 */
	collapse: function(oRow) {
		var oSelf = self.TreeManager;
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
		var oSelf = self.TreeManager;
		oSelf.expandTo(oRow, oSelf.getLevel(oRow)+1);
	},
	
	/* 
	 * Exapnd and show all children of a node 
	 * to a specified level. 
	 */
	expandTo: function(oRow, iToLevel) {
		var oSelf = self.TreeManager;
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
	expandAll: function() {
    	var oSelf = self.TreeManager;
    	oSelf.getRoots(oSelf.oCurrentTable).each(function() {
    		oSelf.expandTo(this, -1);
    	});
    },
	
	/* 
	 * Toggle a node 
	 */
	toggle: function(oRow) {
		var oSelf = self.TreeManager;
		
		if($j(oRow).is(".expanded"))
			oSelf.collapse(oRow);
		else
			oSelf.expand(oRow);
	},
	
	/*
	 * get the roots of the tree
	 */
	getRoots: function(oTable) {
		// roots are defined by having no class "cild-of-node-<<something>>"
		var $Roots = $j("tbody tr",  oTable).not("[class*=child-of-node]");
		return $Roots
	},
    
    /* 
     * if a node0 is a descendant of node1, return true, false otherwise 
     */ 
    isDescendantOf: function(oRow0, oRow1) {
    	var oSelf = self.TreeManager;

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
		var oSelf = self.TreeManager;
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
		var oSelf = self.TreeManager;
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
			var aMatch = $j(oRow).attr("class").match(/child-of-node-(\d+)/);
			if (aMatch != null) {
				return $j("#node-" + aMatch[1])[0];
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
		return $j("tr.child-of-" + $j(oRow)[0].id);
	},
	
	destruct: function() {
		self.TreeManager = null;
	}
};  

self.TreeDnDManager = {

 	// Keep hold of the current table being dragged
    oCurrentTable : null,
    
    // Keep hold of the current drag object if any
    oDragRow: null,
    
    // Keep hold of the current target row
    oTargetRow: null,

    // Keep hold of the "previous" target row 
    oLastTargetRow: null,
    
    // insert position Y (1 or -1)
    iInsertYPosition : null,
    
    // mouse is down? 
    bMouseDown : false,
    
    // The current mouse offset
    pMouseOffset: null,
    
    // Remember the old value of Y so that we don't do too much processing
    yOld: null,
    
    // Remember the old value of X so that we don't do too much processing
    xOld: null,
        
    opts : {},
	defaults : {
		// amount in px for the window vertical scroll speed
		scrollAmount: 20,
		// "sensivity" of horizontal dragging intervals
		hDragInterval: 20,
		// "sensivity" of vertical dragging intervals
		hDragInterval: 10,
		
	},
	
    init: function() {},
    
    /* 
     * display treeview in table with expand and collapse icons 
     */
    makeDraggable: function($Table, opts) {
    	var oSelf = self.TreeDnDManager;
    	
    	// setting the opts (from defaults and overriting with opts) 
       	oSelf.opts = $j.extend({}, oSelf.defaults, opts);
    
       	/* 
       	 * capture the mouse up and mouse move event.
       	 * We can use bind so that we don't interfere
       	 * with other event handlers 
       	 */
    	//$j("tbody th", $Table).bind('mousemove', oSelf.mousemove);
    	document.onmousemove = oSelf.mousemove; // this one ensures firing always!!!!
    	//$j("html").bind('mouseup', oSelf.mouseup);
    	document.onmouseup = oSelf.mouseup; // this one ensures firing always!!!!

		// make rows draggable
		$j("tbody tr", $Table).each(function() {
			var oRow = this;
            
			if (!$j("th span", this).hasClass("filtered_out")) {
				//var $Cell = $j("th", oRow);
				//$Cell.prepend('<span style="margin-left: -' + oSelf.opts.indent + 'px; padding-left: ' + oSelf.opts.indent + 'px">xxxxx</span>');
				//$Cell.prepend('<span class="draggable" style="margin-left: -32px; padding-left: 32px;"/>');
				$j($j("th", this)[0].firstChild).before('<span class="draggable" style="margin-left: -16px; padding-left: 32px;"/>');
				var $DragCell = $j(".draggable", this);
                $DragCell.mousedown(function(ev) {
                	oSelf.bMouseDown = true;
                    oSelf.oDragRow = oRow;
                    oSelf.oCurrentTable = $Table[0];
                    oSelf.pMouseOffset = oSelf.getMouseOffset(oRow, ev);
                    return false;
                })
                $DragCell.css("cursor", "move");
			}
		});            
    },
    
    /* 
     * Get the mouse coordinates from the event 
     * (allowing for browser differences) 
     */
    mouseCoords: function(ev){
        if(ev.pageX || ev.pageY){
            return {x:ev.pageX, y:ev.pageY};
        }
        return {
            x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
            y:ev.clientY + document.body.scrollTop  - document.body.clientTop
        };
    },
    
    /* 
     * Given a target element and a mouse event, get the mouse offset 
	 * from that element. To do this we need the element's position 
	 * and the mouse position 
	 */
    getMouseOffset: function(target, ev) {
        ev = ev || window.event;

        var docPos    = this.getPosition(target);
        var mousePos  = this.mouseCoords(ev);
        return {x:mousePos.x - docPos.x, y:mousePos.y - docPos.y};
    },
	
	/* 
	 * Get the position of an element by going up the DOM tree 
	 * and adding up all the offsets 
	 */
	getPosition: function(e){
        var left = 0;
        var top  = 0;
        /** Safari fix -- thanks to Luis Chato for this! */
        if (e.offsetHeight == 0) {
            /* 
             * Safari 2 doesn't correctly grab the offsetTop of 
             * a table row this is detailed here:
             * http://jacob.peargrove.com/blog/2006/technical/
             * table-row-offsettop-bug-in-safari/
             * the solution is likewise noted there, grab the
             * offset of a table cell in the row - the firstChild.
             * note that firefox will return a text node as a first
             * child, so designing a more thorough solution may need
             * to take that into account, for now this seems to work
             * in firefox, safari, ie 
             */
            e = e.firstChild; 
        }
        while (e.offsetParent){
            left += e.offsetLeft;
            top  += e.offsetTop;
            e     = e.offsetParent;
        }
        left += e.offsetLeft;
        top  += e.offsetTop;
        return {x:left, y:top};
    },
    
    /*
     * mousemove event handling
     */
	mousemove: function(ev) {
		var oSelf = self.TreeDnDManager;
		
		if (!oSelf.bMouseDown)
			return;
			
		//if (oSelf.oDragRow == null) 
		//	return;
		
        var pMousePos = oSelf.mouseCoords(ev);
        var x = pMousePos.x - oSelf.pMouseOffset.x;
        var y = pMousePos.y - oSelf.pMouseOffset.y;

      	// auto scroll the window 
	    var yOffset = window.pageYOffset;
	 	if (document.all) {
	        if (typeof document.compatMode != 'undefined' &&
	             document.compatMode != 'BackCompat') {
	           yOffset = document.documentElement.scrollTop;
	        }
	        else if (typeof document.body != 'undefined') {
	           yOffset=document.body.scrollTop;
	        }
	    }
   		if (pMousePos.y-yOffset < oSelf.opts.scrollAmount) {
	    	window.scrollBy(0, -oSelf.opts.scrollAmount);
	    } else {
            var windowHeight = window.innerHeight ? window.innerHeight
                    : document.documentElement.clientHeight 
                    ? document.documentElement.clientHeight 
                    : document.body.clientHeight;
            if (windowHeight-(pMousePos.y-yOffset) < oSelf.opts.scrollAmount) {
                window.scrollBy(0, oSelf.opts.scrollAmount);
            }
        }

		// Y-coordinate handling: calculate drop target row and insert position!
        if (oSelf.yOld == null)
        	oSelf.yOld = y;
      	var movingUp = false;
		var movingDown = false;
			
		// interval moving y-detection!!!
        if (y > oSelf.yOld + oSelf.opts.vDragInterval) {
        	movingDown = true;
        	oSelf.yOld = y;	
        }
        if (y < oSelf.yOld - oSelf.opts.vDragInterval) {
        	movingUp = true;
        	oSelf.yOld = y;      
        }

		if (movingUp || movingDown) {        
            oSelf.oTargetRow = oSelf.findDropTargetRow(oSelf.oDragRow, y);
	        if (oSelf.oTargetRow) {
            	// after
                if (movingDown) {
                	oSelf.iInserYPosition = 1;
    				$j(oSelf.oTargetRow).addClass('showDragHandleAfter');
    			// before
                } else {
                	oSelf.iInsertYPosition = -1;
                	$j(oSelf.oTargetRow).addClass('showDragHandleBefore');
                }
            }
            if (oSelf.oLastTargetRow != oSelf.oTargetRow) {
            	if (oSelf.oLastTargetRow != null) { 
					$j(oSelf.oLastTargetRow).removeClass('showDragHandleAfter');
					$j(oSelf.oLastTargetRow).removeClass('showDragHandleBefore');
            	}
    			oSelf.oLastTargetRow = oSelf.oTargetRow;
            }
        }
        
        // x-coordinate handling only, if there is no target row!!!
        if (!oSelf.TargetRow) {
	        // x-coordiante handling is independant!!
	        if (oSelf.xOld == null)
	        	oSelf.xOld = x;
	      	var movingRight = false;
			var movingLeft = false;
				
			// interval moving x-detection!!!
	        if (x > oSelf.xOld + oSelf.opts.hDragInterval) {
	        	movingRight = true;
	        	oSelf.xOld = x;	
	        }
	        if (x < oSelf.xOld - oSelf.opts.hDragInterval) {
	        	movingLeft = true;
	        	oSelf.xOld = x;      
	        }
	
			if (movingLeft || movingRight) {        	
		        /*
		         * We need information about the row, which is the next
		         * successor of the dragged row beeing visible and under the
		         * same parent (roots have no relevance!!) as the dragged
		         * row! If such a row exists, we must not drag the row 
		         * (horizontally), because it is "in the middle" of a tree. 
		         * This would destruct the tree structure. So, if
		         * $NextVisibleRow is null, we are allowed to drag horizontally.
		         */
		        var oParent = self.TreeManager.getParent(oSelf.oDragRow);
		        var bNextVisibleRow = false;
		        if (oParent) {
			        // all visible ones!	         
			        var bNextVisibleRow = $j(oSelf.oDragRow).nextAll(":visible").hasClass("child-of-" + oParent.id);
		        }
		        
		        /* 
		         * H-dragging is allowed, if there is no! "next visible row"
		         * (see expnation above) and a previous visible row and no! 
		         * target row (latter case would be "V-Dragging", which
		         * is handled above. 
		         */
		        if (!bNextVisibleRow && !oSelf.oTargetRow) {
		        	if (movingRight) 
		        		oSelf.setHSubtreePos(oSelf.oDragRow, 1)
		            else 
		        		oSelf.setHSubtreePos(oSelf.oDragRow, -1)            	
		        }
			}
        }    
        return false;
    },	
    
    /* 
     * Find the drop target row. We're only worried about
     * the y position really, because we can only move rows
     * up and down. moving inside and outside of a cell is 
     * handled differently. So, this function applies only to 
     * V-dragging. 
     */
    findDropTargetRow: function(oDraggedRow, y) {
		var oSelf = self.TreeDnDManager;
		var oRows = $j("tbody tr", $j(oSelf.oCurrentTable));
		
		for (var i=0; i<oRows.length; i++) {
			var oRow = oRows[i];
            var rowY = oSelf.getPosition(oRow).y;
            var rowHeight = parseInt(oRow.offsetHeight)/2;
            
            if (oRow.offsetHeight == 0) {
                rowY = oSelf.getPosition(oRow.firstChild).y;
                rowHeight = parseInt(oRow.firstChild.offsetHeight)/2;
            }
            /* 
             * Because we always have to insert before, 
             * we need to offset the height a bit
             */
            if ((y > rowY - rowHeight) && (y < (rowY + rowHeight))) {
                /* 
                 * that's the row we're over
				 * If it's the same as the current row, ignore it
				 * drop is also not allowed on child nodes!
				 */
				if (self.TreeManager.isDescendantOf(oRow, oDraggedRow)) 
					return null;
                return oRow;
            }
        }
        return null;
    },
    
    /*
     * mouseup handling (only relevant for V-dragging)
     */
	mouseup: function(ev) {
		var oSelf = self.TreeDnDManager;
		oSelf.bMouseDown = false;
		// set new vertical position
		if (oSelf.oCurrentTable && oSelf.oDragRow) {
			if (oSelf.oTargetRow) {
            	oSelf.setVSubtreePos(oSelf.oDragRow, oSelf.oTargetRow, oSelf.iInsertYPosition);
				$j(oSelf.oTargetRow).removeClass('showDragHandleAfter');
				$j(oSelf.oTargetRow).removeClass('showDragHandleBefore');
			}
			/* 
			 * If we have a dragObject, then we need to release it,
			 * The row will already have been moved to the right
			 * place so we just reset stuff
			 */ 
			oSelf.oDragRow = null;
			oSelf.oCurrentTable = null;
			oSelf.oTargetRow = null;
			oSelf.iInsertYPosition = null;
		}
    },

    /* 
     * sets the new horizontal position of the subtree
     * iPosition: -1 for "left"
     * 			   1 for "right" 
     */
    setHSubtreePos: function(oDragRow, iPosition) {
    	var oSelf = self.TreeDnDManager;
		var oNewParent = null;
		// we need also a boolean to decide, if a new paretn is set or not
		var bNewParentSet = false;
		
		var oOldDndRowParent = self.TreeManager.getParent(oDragRow);
		
		// move right
		if (iPosition == 1) {
			// find the "next" parent in the previous items
	        var $PrevVisibleRows = $j(oSelf.oDragRow).prevAll(":visible");
	        var i = 0;
	        /*
	         * if the "first previous visible row is already
	         * the parent, nothing has to be done. Otherwise,
	         * search the previous visible rows from "nearest"
	         * to "farest" to get the new parent.
	         */
	        if ($PrevVisibleRows && ($PrevVisibleRows[0] != oOldDndRowParent)) {   
		        while (!oNewParent && i<$PrevVisibleRows.size()) {
		        	var oPrevVisibleParent = self.TreeManager.getParent($PrevVisibleRows[i]);
		        	if (oOldDndRowParent == oPrevVisibleParent) {
		        		bNewParentSet = true;
		        		oNewParent = $PrevVisibleRows[i];
		        	}
		        	i++; 
		        }
	        }
		// move left
		} else {
			bNewParentSet = true;
			oNewParent = self.TreeManager.getParent(oOldDndRowParent);
		}
		
		/*
		 * update childclasses, mark dirty, reinit 
		 * tree parts, if we have a new parent!!
		 */
		if (bNewParentSet) {
			// set new parent class and mark dirty!
			if (oOldDndRowParent)
				$j(oDragRow).removeClass("child-of-" + oOldDndRowParent.id);
			if (oNewParent)
				$j(oDragRow).addClass("child-of-" + $j(oNewParent).attr("id"));
				
			// mark dirty, if any changes...
			$j(oDragRow).addClass('markDirty');
			// update all descendants of the subtree (just mark dirty)!
			self.TreeManager.getDescendants(oDragRow).each(function() {
				$j(this).addClass('markDirty');
			});
			// reinit 
			if (oOldDndRowParent)
				self.TreeManager.initSubtree(oOldDndRowParent);
			if (oNewParent)				
				self.TreeManager.initSubtree(oNewParent);
			else
				self.TreeManager.initSubtree(oDragRow);
		}
    },
    
    /* 
     * sets the new vertical position of the subtree
     * iPosition: -1 for "before"
     * 			   1 for after 
     */
    setVSubtreePos: function(oDragRow, oTargetRow, iPosition) {
    	var oSelf = self.TreeDnDManager;
		var oNewParent = null;

		var oOldDndRowParent = self.TreeManager.getParent(oDragRow);
		
		// before is trivial. just the parent of the target row!
		if (iPosition == -1) {
			oNewParent = self.TreeManager.getParent(oTargetRow);
		} else {
			/* 
			 * Insert after is a little bit more complicated.
			 * If there are any visible children below the 
			 * target row, the target row is the new parent.
			 * 
			 * If there are no visible children below the 
			 * target row, the parent of the target row is
			 * the new parent!
			 */
			 var $VisibleChildren = self.TreeManager.childrenOf(oTargetRow).filter(":visible");
			 if ($VisibleChildren && $VisibleChildren.size())
			 	oNewParent = oTargetRow;
			 else
			 	oNewParent = self.TreeManager.getParent(oTargetRow);
		} 
		
		/*
		 * update childclasses, mark dirty, reinit 
		 * tree parts, if we have a new parent!!
		 */
		// set new parent class and mark dirty!
		if (oOldDndRowParent)
			$j(oDragRow).removeClass("child-of-" + oOldDndRowParent.id);
		if (oNewParent)
			$j(oDragRow).addClass("child-of-" + $j(oNewParent).attr("id"));
			
		// set the dragged row to new position!
		// before
		if (iPosition == -1) {
			$j(oDragRow).insertBefore($j(oTargetRow));
		}
		// after		
		else {
			/*
			 * this is a little bit tricky. we must not forget 
			 * the descendants!! if the target node has any visible
			 * children, the node must be inserted immediately after
			 * the target node. Otherwise, the node must be inserted
			 * after tha last descendant! of the target row.
			 * TODO The code below works, but can be optimized!
			 */
			var oInsertAfter = oTargetRow;
			var $TargetDescendants = self.TreeManager.getDescendants(oTargetRow);
			if ($TargetDescendants && $TargetDescendants.size()) {
				var $VisibleDescs = $TargetDescendants.filter(":visible"); 
				if (!$VisibleDescs || !$VisibleDescs.size()) {
					var $LastHiddenDesc = $TargetDescendants.filter(":hidden").filter(":last");
					oInsertAfter = $LastHiddenDesc[0];
				}
			}
			$j(oDragRow).insertAfter($j(oInsertAfter));
		}

		// mark dirty, if any changes...
		$j(oDragRow).addClass('markDirty');
		
		// insert childs of dragged row. This must be done in reverse order!!
		var $ChildRows = self.TreeManager.getDescendants(oDragRow);
		for (var i=0; i<$ChildRows.length; i++) {
			var oChild = $ChildRows[$ChildRows.length-i-1];
			$j(oChild).insertAfter($j(oDragRow));
			$j(oChild).addClass('markDirty');
		}

		// reinit 
		if (oOldDndRowParent)
			self.TreeManager.initSubtree(oOldDndRowParent);
		if (oNewParent)				
			self.TreeManager.initSubtree(oNewParent);
		else
			self.TreeManager.initSubtree(oDragRow);
    },
    
    /*
     * Serializes the whole tree for saving.
     */
	serialize: function($Table) {
		var result = [];
        var oTable = $Table[0];
        var i = 0;
        
        $j("tbody tr", $Table).each(function() {
        	var sRowId = $j(this).attr("id").match(/node-(\d+)/)[1];
        	var sParentId = null;
        	var oParent = self.TreeManager.getParent(this);
        	if (oParent) {
        		sParentId = $j(oParent).attr("id").match(/node-(\d+)/)[1];
        	}
        	result[i] = {
        		id: sRowId,
        		parent: sParentId
        	} 
        	i++;
        });
        return JSON.stringify(result);
	},

    destruct: function() {
        self.TreeDnDManager = null;
    }
 
};  
    
$j(document).ready(function(){
	self.TreeMainManager.init();
    self.TreeManager.init();
    self.TreeDnDManager.init();
});

$j(window).unload(function() {
	self.TreeMainManager.destruct();
    self.TreeManager.destruct();
    self.TreeDnDManager.destruct();
});

