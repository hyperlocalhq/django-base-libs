(function(e,t){function n(){e("#photos").each(function(){var t=e(this).data("load-url");e(this).load(t+" #photos>*",function(){e("#photos").sortable({placeholder:"ui-state-highlight",update:function(n,r){var i=[];e(".item","#photos").each(function(){e(this).data("token")&&(i[i.length]=e(this).data("token"))});e.post(t,{ordering:i.join(",")})}});e("#photos").disableSelection().find(".edit_photo").click(function(){e("#edit_photo").load(e(this).attr("href")+" .content form",r);e("#photos").parents("fieldset:first").hide();e(".form-actions:last").hide();return!1});e("#photos").find(".crop_photo").each(function(){e(this).attr("href",e(this).attr("href").replace(/goto_next=.+$/gim,"goto_next="+location.href))});e("#add_photo").click(function(){e("#edit_photo").load(e(this).attr("href")+" .content form",r);e("#photos").parents("fieldset:first").hide();e(".form-actions:last").hide();return!1});e(window).trigger("scrollstop")})});e("#photos").parents("fieldset:first").show();e(".form-actions:last").show()}function r(){e("#button-id-cancel").click(function(){e("#edit_photo").html("");n()});e("#button-id-crop-photo").click(function(){location.href=e(this).data("href").replace(/goto_next=.+$/,"goto_next="+location.href)});e("#button-id-delete-photo").click(function(){var t=e(this).data("href");e("#deleteConfirmation").modal("show");e("#button-id-confirm-deletion").click(function(){e.post(t,{},function(){e("#deleteConfirmation").modal("hide");e("#edit_photo").html("");n()});return!1})});e("#edit_photo form").attr("target","hidden_iframe");self.hidden_iframe_loaded=function(t){var i=e("<div>"+t+"</div>").find("form");if(i.length){e("#edit_photo").html("").append(i);r()}else{e("#edit_photo").html("");n()}}}e(function(){n()})})(jQuery);