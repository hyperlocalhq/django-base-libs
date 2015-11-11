/**
 Ajaxified listing of items.
 The workflow is this:
   1. Events on widgets trigger the hash change in the url.
   2. The hash change (or existence) in the url triggers loading the list with
      the params in the hash and changing the state of the widgets.
   3. Before the list loading "before_list_load" event is triggered for 
      <div id="object_list"></div> 
   4. After the list loading "after_list_load" event is triggered for 
      <div id="object_list"></div>
*/

(function($, undefined) {
    var sLoadReason = "";
    var oReInnerScripts = /<script\b[^>]*>([\s\S]*?)<\/script>/gm;
    
    $(document).ready(function() {
            
     	$(".page_count").change(function () {
            $(".page_count").val($(this).val());
        	paginate_by($(this).val());
        });
     	
     	$(".page_skip").live("change", function () {
        	$(".page_skip").not(this).val($(this).val());
        	if (this.selectedIndex == 0) {
        	    $(".pagination .previous").html('<span class="disabled"><span class="hidden"></span></span>');
        	} else {
        	    $(".pagination .previous").html('<a href=""><span class="enabled"><span class="hidden"></span></span></a>');
        	}
        	if (this.selectedIndex == this.length - 1) {
        	    $(".pagination .next").html('<span class="disabled"><span class="hidden"></span></span>');
        	} else {
        	    $(".pagination .next").html('<a href=""><span class="enabled"><span class="hidden"></span></span></a>');
        	}
        	open_page($(this).val());
        	return false;
        });
        $(".pagination .previous a").live("click", function () {
            var oSelect = $(this).parents(".pagination").find(".page_skip").get(0)
            oSelect.selectedIndex--;
            $(oSelect).change();
            return false;
        });
        $(".pagination .next a").live("click", function () {
            var oSelect = $(this).parents(".pagination").find(".page_skip").get(0)
            oSelect.selectedIndex++;
            $(oSelect).change();
            return false;
        });
     	
     	$(".list_sorting").change(function () {
            $(".list_sorting").val($(this).val());
        	order_by($(this).val());
        });
        
        $(".abc_filter a").click(function () {
        	filter_by_abc($(this).attr("id"));
        	return false;
        });

     	$("#id_list_view").change(function () {
        	view_by($(this).val());
        });

     	$("#object_list_filter_form").submit(filter_form);
     	
     	$("#object_list_filter_form :input").change(function() {
            $("#object_list_filter_form").submit();
     	})
        
     	$(".list-types a").click(function() {
            document.location = $(this).attr("href") + document.location.hash;
            return false;
     	});
     	
        if ($("#object_list").length) {
            $(window).hashchange(hash_changed);
            if (location.hash) {
                $(window).hashchange();
            }
        }
     	
    });
    
    function filter_form() {
        sLoadReason = "filter_form";
        location.href = "#" + $(this).serialize();
        return false;
    }
    
    function open_page(sVal) {
        sLoadReason = "open_page";
        sVal = sVal || 1;
        load({page: sVal});
    }
    
    function paginate_by(iItems) {
        sLoadReason = "paginate_by";
    	if (iItems) {
            load({page: null, view_type: null, paginate_by: iItems});
	    }
    }
    
    function order_by(sVal) {
        sLoadReason = "order_by";
    	if (sVal) {
            load({page: null, view_type: null, order_by: sVal});
	    }
    }
    
    function view_by(sVal) {
        sLoadReason = "view_by";
        if (sVal == "gallery") {
            alert(gettext("Gallery view is not yet implemented!"));
        }
    }
    
    function filter_by_abc(iId) {
        sLoadReason = "filter_by_abc";
        var aM = iId.match(/id_abc_filter_(.*)$/);
    	if (aM) {
    	    var sFilter = aM[1];
    	    if (sFilter == "") {
    	        sFilter = null;
    	    }
	        load({page: null, view_type: null, 'by-abc': sFilter});
	    }
    }
    
    function load(aParams) {
        if (location.hash) {
            append_to_hash(aParams);
        } else {
            location.href = "#" + append_to_get(aParams, true);
        }
    }
    
    function hash_changed() {
        sUrl = location.href.replace(/(\?.*)?#/, "?");
        $('#object_list').trigger("before_list_load").animate({opacity: 0.25}, 500, function() {
            if (!$(this).data('loading')) {
                $(this).css('opacity', 1);
            }
        }).data('loading', true).load(
            sUrl + " #object_list>*",
            list_loaded
        );
        // trigger the change of aphabetical filter
        var aMatch = location.hash.match(/by-abc=([^&]+)/);
        $(".abc_filter a.active").removeClass("active");
        if (aMatch) {
            $("#id_abc_filter_" + aMatch[1]).addClass("active").focus();
        } else {
            $("#id_abc_filter_").addClass("active").focus();
        }
        // trigger the change of filter form
        var $oForm = $("#object_list_filter_form");
        if ($oForm.length) {
            $oForm.find(":input").not(":button,:submit,:reset").each(function() {
                var sFieldName = $(this).attr("name");
                aMatch = location.hash.match(new RegExp(sFieldName + "=([^&]+)"));
                if ($(this).is(":checkbox")) {
                    if (aMatch) {
                        $(this).attr("checked", "checked");
                    } else {
                        $(this).attr("checked", null);
                    }
                } else {
                    if (aMatch) {
                        $(this).val(aMatch[1]);
                    } else {
                        $(this).val("");
                    }
                }
            });
        }
    }
    
    function list_loaded(responseText, textStatus, XMLHttpRequest) {
        if ("success|notmodified".indexOf(textStatus) != -1) {
            var $oList = $('#object_list');
            if (sLoadReason != "open_page") {
                var $oPagination = $(responseText).find(".pagination").filter(":first");
                $(".pagination").each(function() {
                    $oThis = $(this).html("");
                    if ($oPagination.length) {
                        $oThis.append($oPagination.clone().children());
                    }
                });
            }
            var sScripts = "";
            responseText.replace(
                oReInnerScripts,
                function($0, $1) {sScripts += $1;return $0;}
            );
            eval(sScripts);
            $oList.css('opacity', 1).data('loading', false).trigger("after_list_load");
            sLoadReason = "";
        }
    }

}(jQuery));
