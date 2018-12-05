u.ready(function() {

    function FavoriteManager(u_element) {

        var me = this;

        me.u_element = u_element;
        me.u_span = u(me.u_element.children('span.sr-only').first());
        me.content_type_id = me.u_element.attr('data-content-type-id');
        me.object_id = me.u_element.attr('data-object-id');

        me.sInnerTextToAdd = favorite_tooltip_text.Add_to_My_Favorites;
        me.sTitleToAdd = favorite_tooltip_text.Add_to_My_Favorites;
        me.sInnerTextToRemove = favorite_tooltip_text.Remove_from_My_Favorites;
        me.sTitleToRemove = favorite_tooltip_text.Remove_from_My_Favorites;

        if (me.content_type_id && me.object_id) u_element.click(function(e) {return me.toggle(e);});
    }

    FavoriteManager.prototype.toggle = function(e) {

        e.preventDefault();

        var me = this;

        me.u_element.addClass('progress').css('cursor', 'wait');
        u.ajax('/' + window.settings.LANGUAGE_CODE + '/helper/favorite/' + me.content_type_id + '/' + me.object_id + '/',
            function(oData, success) {if (success) me.showResults(oData);}
        );

        return false;
    }

    FavoriteManager.prototype.showResults = function(oData) {

        var me = this;

        if (oData) {

            oData = JSON.parse(oData);

            if (oData.action === 'added') {
                me.u_element.attr('title', me.sTitleToRemove).addClass('active');
                me.u_span.html(me.sInnerTextToRemove);
            } else {
                me.u_element.attr('title', me.sTitleToAdd).removeClass('active');
                me.u_span.html(me.sInnerTextToAdd);
            }

            if (oData.count !== undefined) me.u_element.children('.favorites_count').text(oData.count);
        }

        me.u_element.removeClass('progress').css('cursor', '');
    }

    u('button.favorite, a.favorite, .toggle.favorite').each(function(node) {
        new FavoriteManager(u(node));
    });
});
