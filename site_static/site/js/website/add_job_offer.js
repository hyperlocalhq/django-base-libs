(function ($, undefined) {

    self.JobOfferMainDataManager = {
        init: function () {
            var oSelf = self.JobOfferMainDataManager;

            $("#id_offering_institution").blur(oSelf.completeContact);

            /* link to manual input of institution data */
            $("#link_enter_institution").click(function () {
                oSelf.manageBlocks("enter institutions manually");
                return false;
            });

            /* link back to institution selection */
            $("#link_select_institution").click(function () {
                oSelf.manageBlocks("select institution");
                return false;
            });

            /* organizer_ind radio buttons events */
            $("#id_contact_person_ind_0").change(function () {
                if ($(this).attr("checked")) {
                    oSelf.manageBlocks("contact person myself");
                }
                return false;
            });
            $("#id_contact_person_ind_1").change(function () {
                if ($(this).attr("checked")) {
                    oSelf.manageBlocks("enter contact person name");
                }
                return false;
            });

            /* initial situation */
            if ($("#id_offering_institution_title").val() != "") {
                oSelf.manageBlocks("enter institutions manually");
            } else {
                oSelf.manageBlocks("select institution");
            }

            if ($("input[name='contact_person_ind']:checked").val() == 1) {
                oSelf.manageBlocks("enter contact person name");
            } else {
                oSelf.manageBlocks("contact person myself");
            }
        },

        manageBlocks: function (sCase) {
            switch (sCase) {
                case "select institution":
                    $("#block_institution_title_input").addClass("hidden");
                    $("#id_offering_institution_title").val("");
                    $("#block_institution_select").removeClass("hidden to_hide");
                    break;
                case "enter institutions manually":
                    $("#block_institution_select").addClass("hidden");
                    $("#id_offering_institution").val("");
                    $("#id_offering_institution_text").val("");
                    $("#block_institution_title_input").removeClass("hidden to_hide");
                    break;
                case "contact person myself":
                    $("#block_contact_input").addClass("hidden");
                    $("#id_contact_person_name").val("");
                    break;
                case "enter contact person name":
                    $("#block_contact_input").removeClass("hidden to_hide");
                    break;
                default:
                    break;
            }
        },

        completeContact: function () {
            var oSelf = self.JobOfferMainDataManager;
            if ($(this).val()) {
                $.get(
                    "/helper/" + settings.URL_ID_JOB_OFFER + "/" + settings.URL_ID_INSTITUTION + "_attrs/" + $("#id_offering_institution").val() + "/",
                    self.JobOfferMainDataManager.fillInContactData,
                    'json'
                );
                return false;
            }
        },

        fillInContactData: function (oData) {
            var oSelf = self.JobOfferMainDataManager;

            // fill in data
            if (!$('#id_street_address').val()) {
                $('#id_street_address').val(oData.street_address);
            }
            if (!$('#id_street_address2').val()) {
                if (oData.street_address2) {
                    $('#id_street_address2').val(oData.street_address2);
                } else {
                    $('#id_street_address2').val('');
                }
            }
            if (!$('#id_postal_code').val()) {
                $('#id_postal_code').val(oData.postal_code);
            }
            if (!$('#id_city').val()) {
                $('#id_city').val(oData.city);
            }
            if (!$('#id_country').val()) {
                $('#id_country').val(oData.country.iso2_code);
            }

            /*
             updating the address, email and url data not at the initial call!
             we need that for form validation (otherwise, any entered data would be
             overwritten
             */

            $('#id_email0_address').val(oData.email0_address);
            $('#id_url0_link').val(oData.url0_link);

            /*
             fill in phone and fax data. we have to map the 'phone-type'.
             for simplicity, this is hardcoded at the moment. But maybe
             there is a nicer solution for that
             */
            var phone_index = -1;
            var fax_index = -1;
            for (i = 0; i < 3; i++) {
                if (oData['phone' + i + '_type_id'] == 1)
                    phone_index = i;
                if (oData['phone' + i + '_type_id'] == 2)
                    fax_index = i;
            }
            if (phone_index != -1) {
                $('#id_phone_country').val(oData['phone' + phone_index + '_country']);
                $('#id_phone_area').val(oData['phone' + phone_index + '_area']);
                $('#id_phone_number').val(oData['phone' + phone_index + '_number']);
            }
            if (fax_index != -1) {
                $('#id_fax_country').val(oData['phone' + fax_index + '_country']);
                $('#id_fax_area').val(oData['phone' + fax_index + '_area']);
                $('#id_fax_number').val(oData['phone' + fax_index + '_number']);
            }
        },

        destruct: function () {
            self.JobOfferMainDataManager = null;
        }
    };

    $(document).ready(function () {
        self.JobOfferMainDataManager.init();
    });

    $(window).unload(function () {
        self.JobOfferMainDataManager.destruct();
    });

}(jQuery));
