$j = jQuery;

if (self.GroupMembershipManager) { // DEBUG
    alert("The groups_networks.js is included into this page twice. Please remove the duplicate from the template (probably {% block extrahead %}{% endblock %}).");
}

self.GroupMembershipManager = {
    sContextItemType: "",
    sSlug: "",
    sInnerTextToAdd: gettext("Join Group"),
    sTitleToAdd: gettext("Join Group"),
    sInnerTextToCancel: gettext("Cancel Joining"),
    sTitleToCancel: gettext("Cancel Joining"),
    sInnerTextToRemove: gettext("Leave Group"),
    sTitleToRemove: gettext("Leave Group"),
    init: function() {
        var oSelf = self.GroupMembershipManager;
        var aUrlBits = window.website.path.substr(1).split("/");
        // person|institution|event|document|group
        oSelf.sContextItemType = aUrlBits[0];
        if ("group" == oSelf.sContextItemType) {
            oSelf.sSlug = aUrlBits[1];
            var sLang = window.settings.LANGUAGE_CODE;
            $j(
                "#featured_join_group,#activity_" + sLang + " .navi_join-this-group_" + sLang
            ).click(function(){
                return oSelf.request(oSelf.sSlug);
            });
            $j(
                "#activity_" + sLang + " .navi_leave-this-group_" + sLang
            ).click(function(){
                return oSelf.remove(oSelf.sSlug);
            });
        }
    },
    request: function(sSlug) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Join Group'),
            584, "auto",
            "/helper/group-membership/request/" + sSlug + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    invite: function(sSlug, sUsername) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Invite User'),
            584, "auto",
            "/helper/group-membership/invite/" + sSlug + "/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    accept_user: function(sSlug, sUsername) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Accept User'),
            400, "auto",
            "/helper/group-membership/accept-user/" + sSlug + "/" + sUsername + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    deny_user: function(sSlug, sUsername) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Deny User'),
            584, "auto",
            "/helper/group-membership/deny-user/" + sSlug + "/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    cancel_user: function(sSlug, sUsername) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Cancel Invitation'),
            584, "auto",
            "/helper/group-membership/cancel-user/" + sSlug + "/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    remove_user: function(sSlug, sUsername) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Remove Member'),
            584, "auto",
            "/helper/group-membership/remove-user/" + sSlug + "/" + sUsername + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    accept_group: function(sSlug) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Accept Invitation to a Group'),
            584, "auto",
            "/helper/group-membership/accept-group/" + sSlug + "/",
            false,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    deny_group: function(sSlug) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Deny Invitation to a Group'),
            584, "auto",
            "/helper/group-membership/deny-group/" + sSlug + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    cancel: function(sSlug) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Cancel Group Joining'),
            584, "auto",
            "/helper/group-membership/cancel/" + sSlug + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    remove: function(sSlug) {
        var oSelf = self.GroupMembershipManager;
        open_popup(
            gettext('Remove Relationship'),
            584, "auto",
            "/helper/group-membership/remove/" + sSlug + "/",
            true,
            false,
            {
                onaftersubmit: oSelf.updatePage
            }
        );
        return false;
    },
    updatePage: function() {
        var oSelf = self.GroupMembershipManager;
        var sLang = window.settings.LANGUAGE_CODE;
        $j("#activity_" + sLang).load(
            document.location.pathname + " #activity_" + sLang,
            oSelf.init
        );
    },
    destruct: function() {
        self.GroupMembershipManager = null;
    }
};

if (self.open_popup) {
    $j(document).ready(function(){
        self.GroupMembershipManager.init();
    });
} else {
    self._jquery_popup_loading = true;
    $j.get(
        settings.STATIC_URL + "site/js/jquery/jquery.popup.js",
        function(sData) {
            eval(sData);
            self._jquery_popup_loading = null;
            $j(document).ready(function(){
                self.GroupMembershipManager.init();
            });
        }
    );
}

$j(window).unload(function() {
    self.GroupMembershipManager.destruct();
});
