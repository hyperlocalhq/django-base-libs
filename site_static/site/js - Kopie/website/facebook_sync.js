(function($, undefined) {
    var sIndicator = '<img src="' + settings.STATIC_URL + 'site/js/jquery/indicator.gif" alt="" />';
    $(document).ready(function() {
        function show_sync_controls() {
            var oCCBUpdated, oFBUpdated, sDate;
            var $oLinking = $(this).parents('.gallery-linking');
            var $oContainer = $oLinking.parent();
            var sCCBToken = $oLinking.data("ccb-gallery-token");
            var nCCBCount = $oLinking.data("ccb-gallery-count") || 0;
            sDate = $oLinking.data("ccb-gallery-updated");
            if (sDate) {
                oCCBUpdated = new Date(sDate);
            }
            var sFBId = $oLinking.data("fb-album-id");
            var nFBCount = $oLinking.data("fb-album-count") || 0;
            sDate = $oLinking.data("fb-album-updated");
            if (sDate) {
                oFBUpdated = new Date(sDate);
            }
            $(this).html("");
            var $oControls = $('<ul class="toolbar"></ul>').appendTo($(this));
            if (sCCBToken && !sFBId) {
                $(
                    '<a href="" class="copy-ccb-to-fb"><span><span>' + gettext("Copy &gt;") + '</span></span></a>'
                ).click(function() {
                    $(this).parents(".sync-controls").html('<div>' + sIndicator + ' ' + gettext("Copying...") +  '</div>');
                    $oLinking.parent().load(location.pathname, {
                        ccb_gallery_token: sCCBToken,
                        action: "ccb-to-fb"
                    }, function() {
                        $oContainer.find('.sync-controls').each(show_sync_controls);
                    });
                    return false;
                }).appendTo($('<li></li>').appendTo($oControls));
            } else if (!sCCBToken && sFBId) {
                $(
                    '<a href="" class="copy-fb-to-ccb"><span><span>' + gettext("&lt; Copy") + '</span></span></a>'
                ).click(function() {
                    $(this).parents(".sync-controls").html('<div>' + sIndicator + ' ' + gettext("Copying...") +  '</div>');
                    $oLinking.parent().load(location.pathname, {
                        fb_album_id: sFBId,
                        action: "fb-to-ccb"
                    }, function() {
                        $oContainer.find('.sync-controls').each(show_sync_controls);
                    });
                    return false;
                }).appendTo($('<li></li>').appendTo($oControls));
            } else {
                $(
                    '<a href="" class="copy-fb-to-ccb"><span><span>' + gettext("&lt; Copy") + '</span></span></a>'
                ).click(function() {
                    $(this).parents(".sync-controls").html('<div>' + sIndicator + ' ' + gettext("Copying...") +  '</div>');
                    $oLinking.parent().load(location.pathname, {
                        ccb_gallery_token: sCCBToken,
                        fb_album_id: sFBId,
                        action: "fb-to-ccb"
                    }, function() {
                        $oContainer.find('.sync-controls').each(show_sync_controls);
                    });
                    return false;
                }).appendTo($('<li></li>').appendTo($oControls));
                $(
                    '<a href="" class="sync-fb-and-ccb"><span><span>' + gettext("Sync") + '</span></span></a>'
                ).click(function() {
                    $(this).parents(".sync-controls").html('<div>' + sIndicator + ' ' + gettext("Syncing...") +  '</div>');
                    $oLinking.parent().load(location.pathname, {
                        ccb_gallery_token: sCCBToken,
                        fb_album_id: sFBId,
                        action: "sync"
                    }, function() {
                        $oContainer.find('.sync-controls').each(show_sync_controls);
                    });
                    return false;
                }).appendTo($('<li></li>').appendTo($oControls));
                $(
                    '<a href="" class="copy-ccb-to-fb"><span><span>' + gettext("Copy &gt;") + '</span></span></a>'
                ).click(function() {
                    $(this).parents(".sync-controls").html('<div>' + sIndicator + ' ' + gettext("Copying...") +  '</div>');
                    $oLinking.parent().load(location.pathname, {
                        ccb_gallery_token: sCCBToken,
                        fb_album_id: sFBId,
                        action: "ccb-to-fb"
                    }, function() {
                        $oContainer.find('.sync-controls').each(show_sync_controls);
                    });
                    return false;
                }).appendTo($('<li></li>').appendTo($oControls));
            }
        };
        $('.sync-controls').each(show_sync_controls);
    });
}(jQuery));
