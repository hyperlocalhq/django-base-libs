/* global self:false, favorite_tooltip_text:false */
(function($, undefined) {
    
    self.FavoriteManager = {
        sContextItemType: '',
        sSlug: '',
        sInnerTextToAdd: favorite_tooltip_text.Add_to_My_Favorites,
        sTitleToAdd: favorite_tooltip_text.Add_to_My_Favorites,
        sInnerTextToRemove: favorite_tooltip_text.Remove_from_My_Favorites,
        sTitleToRemove: favorite_tooltip_text.Remove_from_My_Favorites,
        init: function() {
        },
        destruct: function() {
            self.FavoriteManager = null;
        },
        toggle: function(oElement, iCTId, oObjId) {
            $(oElement).addClass('progress').css({
                cursor: 'wait'
            });
            $.get(
                '/' + window.settings.lang + '/helper/favorite/' + iCTId + '/' + oObjId + '/',
                function(oData) {
                    self.FavoriteManager.showResults(oData, oElement);
                },
                'JSON'
            );
            return false;
        },
        showResults: function(oData, oElement) {
            var oSelf = self.FavoriteManager;
            var $oEl = $(oElement);
            if (oData) {
                var $oSpan = $oEl.children('span:first');
                if (oData.action === 'added') {
                    $oEl.attr({
                        title: oSelf.sTitleToRemove
                    }).addClass('active');
                    $oSpan.html(oSelf.sInnerTextToRemove);
                    $oEl.attr('data-original-title',oSelf.sInnerTextToRemove);
                } else {
                    $oEl.attr({
                        title: oSelf.sTitleToAdd
                    }).removeClass('active');
                    $oSpan.html(oSelf.sInnerTextToAdd);
                    $oEl.attr('data-original-title',oSelf.sInnerTextToAdd);
                }
                if (oData.count !== undefined) {
                    $oEl.children('.favorites_count').text(oData.count);
                }
            }
            $oEl.removeClass('progress').css({cursor: 'pointer'});
        }
    };
    $(document).ready(function(){
        self.FavoriteManager.init();
    });
    
    $(window).unload(function() {
        self.FavoriteManager.destruct();
    });
    
}(jQuery));
