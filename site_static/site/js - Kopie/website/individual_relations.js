$j = jQuery;

if (self.IndividualRelationManager) { // DEBUG
    alert("The individual_relations.js is included into this page twice. Please remove the duplicate from the template (probably {% block extrahead %}{% endblock %}).");
}

self.IndividualRelationManager = {
    sContextItemType: "",
    sUsername: "",
    sInnerTextToAdd: gettext("Add to contacts"),
    sTitleToAdd: gettext("Add to contacts"),
    sInnerTextToCancel: gettext("Cancel relationship"),
    sTitleToCancel: gettext("Cancel relationship"),
    sInnerTextToRemove: gettext("It's your contact"),
    sTitleToRemove: gettext("Remove from contacts"),
    sInnerTextToConfirm: gettext("Requesting confirmation"),
    sTitleToConfirm: gettext("Confirm relationship"),
    init: function() {
        var oSelf = self.IndividualRelationManager;
        var aUrlBits = window.website.path.substr(1).split("/");
        // person|institution|event|document|group
        oSelf.sContextItemType = aUrlBits[0];
        if ("person" == oSelf.sContextItemType) {
            oSelf.sUsername = aUrlBits[1];
            var sLang = window.settings.lang;
            $j(
                "#activity_" + sLang + " .navi_add-to-contacts_" + sLang
            ).click(function(){
                return oSelf.invite(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_accept-relationship_" + sLang
            ).click(function(){
                return oSelf.accept(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_deny-relationship_" + sLang
            ).click(function(){
                return oSelf.deny(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_cancel-invitation_" + sLang
            ).click(function(){
                return oSelf.cancel(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_edit-relationship_" + sLang
            ).click(function(){
                return oSelf.edit(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_remove-from-contacts_" + sLang
            ).click(function(){
                return oSelf.remove(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_block-contact_" + sLang
            ).click(function(){
                return oSelf.block(oSelf.sUsername);
            });
            $j(
                "#activity_" + sLang + " .navi_unblock-contact_" + sLang
            ).click(function(){
                return oSelf.unblock(oSelf.sUsername);
            });
        }
    },
    invite: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Invite Contact'),
            584, "auto",
            "/helper/individual-relation/invite/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    accept: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Accept Invitation'),
            584, "auto",
            "/helper/individual-relation/accept/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    deny: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Deny Contact'),
            584, "auto",
            "/helper/individual-relation/deny/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    cancel: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Cancel Invitation'),
            584, "auto",
            "/helper/individual-relation/cancel/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    edit: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Edit Relationship'),
            584, "auto",
            "/helper/individual-relation/edit/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    remove: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Remove Relationship'),
            584, "auto",
            "/helper/individual-relation/remove/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    block: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Block Contact'),
            584, "auto",
            "/helper/individual-relation/block/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    unblock: function(sUsername) {
        var oSelf = self.IndividualRelationManager;
        open_popup(
            gettext('Invite'),
            584, "auto",
            "/helper/individual-relation/unblock/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    updatePage: function() {
        var oSelf = self.IndividualRelationManager;
        var sLang = window.settings.lang;
        $j("#activity_" + sLang).load(
            document.location.pathname + " #activity_" + sLang,
            oSelf.init
        );
    },
    destruct: function() {
        self.IndividualRelationManager = null;
    }
};

if (self.open_popup || self._jquery_popup_loading) {
    $j(document).ready(function(){
        self.IndividualRelationManager.init();
    });
} else {
    self._jquery_popup_loading = true;
    $j.get(
        settings.STATIC_URL + "site/js/jquery/jquery.popup.js",
        function(sData) {
            eval(sData);
            self._jquery_popup_loading = null;
            $j(document).ready(function(){
                self.IndividualRelationManager.init();
            });
        }
    );
}

$j(window).unload(function() {
    self.IndividualRelationManager.destruct();
});
