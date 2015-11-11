(function($, undefined) {

    self.FormsetsManager = {
        init: function() {
            var oSelf = self.FormsetsManager;
            $(
                '<div class="buttonHolder">'
                + '<input type="button" class="add-formset primaryAction" value="'
                + gettext('Add another entry')
                + '" />'
                + '</div>'
            ).insertAfter('.formset-form:last');
            $('input:hidden.form_hidden[id$=TOTAL_FORMS]').each(function() {
                var totalField = this;
                var $totalField = $(this);
                var $fieldset = $totalField.nextAll('.formset-form');
                $fieldset.find('input:checkbox[id$=DELETE]').parent().each(function() {
                    var $deleteLink = $(
                        '<a href="#delete_event_time" class="deletebutton"><span>'
                        + gettext('Delete')
                        + '</span></a>'
                    );
                    $(this).hide();
                    $(this).before($deleteLink);
                    $deleteLink.click(function() {
                        if (parseInt($(totalField).val())>1) {
                            $(this).closest('.formset-form').remove();
                            $totalField.val(parseInt($(totalField).val())-1);
                            $fieldset.find('.formset-form').each(function(index, form) {
                                oSelf.set_index_for_fields($(form), index);
                            });
                        }
                        return false;
                    });
                });
                
                $fieldset.parent().find('input:button.add-formset').click(function(e) {
                    var $newForm = $totalField.nextAll('.formset-form').filter(':last').clone(true);
                    
                    oSelf.set_index_for_fields(
                        $newForm,
                        parseInt($totalField.val(), 10)
                    );
                    
                    $newForm.insertAfter('.formset-form:last', this);
                    $totalField.val(parseInt($totalField.val(), 10) + 1);
                });
            });
        },
    
        set_index_for_fields: function($formset_form, index) {
            $formset_form.find(':input').each(function() {
                var $field = $(this);
                if ($field.attr("id")) {
                    $field.attr(
                        "id",
                        $field.attr("id").replace(/-(\d+)-/, "-" + index + "-")
                    );
                }
                if ($field.attr("name")) {
                    $field.attr(
                        "name",
                        $field.attr("name").replace(/-(\d+)-/, "-" + index + "-")
                    );
                }
            });
            $formset_form.find('label').each(function() {
                var $field = $(this);
                if ($field.attr("for")) {
                    $field.attr(
                        "for",
                        $field.attr("for").replace(/-(\d+)-/, "-" + index + "-")
                    );
                }
            });
        },
        
        destruct: function() {
            self.FormsetsManager = null;
        }
    }
    
    $(document).ready(function() {
        self.FormsetsManager.init();
    });
    
    $(window).unload(function() {
        self.FormsetsManager.destruct();
    })
    
}(jQuery));