$j = jQuery;

var InstitutionLookupManager = {
    init: function() {
        InstitutionLookupManager.addEvents("publisher");
    },
    addEvents: function(sName) {
        var oOld = $j("#id_" + sName);
        var sHiddenId = oOld.attr("id") + "_hidden";
        var sVal = oOld.val();
        $j('<input type="text" />').attr({
            id: oOld.attr("id"),
            maxlength: 255,
            size: 30
        }).replaceAll(oOld).after(
            $j('<input type="hidden" />').attr({
                id: sHiddenId,
                name: oOld.attr("name")
            }).val(sVal).change(oOld[0].onchange)
        ).autocomplete("/" + window.settings.lang + "/helper/institution_lookup/", {
            onItemSelect: new Function(
                "oEl",
                "InstitutionLookupManager.onItemSelect('"+sHiddenId+"', oEl)"
            )
        }).addClass("vTextField").val(
            sVal?
                oOld[0].options[oOld[0].selectedIndex].innerHTML:
                ""
        ).change(function() {
            if (!$j(this).val()) {
                $j("#" + sHiddenId).val("").change();
            }
        });
    },
    onItemSelect: function(sHiddenId, oEl) {
        if(oEl == null) {
            return;
        }
        if(!!oEl.extra) {
            $j("#" + sHiddenId).val(oEl.extra[0]).change();
        }
    }
};

$j(document).ready(function() {
    InstitutionLookupManager.init();
});
