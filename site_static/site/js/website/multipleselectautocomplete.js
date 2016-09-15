self.MutipleSelectAutoCompleteManager = {
    init: function () {
        $('select[multiple]:visible').each(function () {
            var valuesList = [];
            var valuesIDsMap = {};
            $('option', this).each(function () {
                if (!$(this).attr('value')) return;
                valuesList.push($(this).text());
                valuesIDsMap[$(this).text()] = $(this).attr('value');
            });
            var selectField = this;
            var selectFieldID = $(this).attr('id');
            var selectFieldName = $(this).attr('name');
            var inputFieldID = selectFieldID + '_autocomplete';
            var selectedListID = selectFieldID + '_selected';
            $(this).wrap('<div class="autocomplete_container"></div>');
            $(this).after('<ul id="' + selectedListID + '" class="autocomplete_selected"/><input type="text" id="' + inputFieldID + '" />');
            var $input = $('#' + inputFieldID);
            $input.autocomplete(valuesList, {
                selectFirst: false,
                highlight: false,
                max: 20,
                minChars: 1,
                mustMatch: 1,
                matchContains: true
            });
            $input.result(function (event, data, formatted) {
                var id = valuesIDsMap[data];
                if (id) {
                    $('#' + selectedListID).append('<li>' + data + '<a href="#" class="closebutton" /></li>');
                    $('option[value=' + id + ']', selectField).attr('selected', true);
                    $(this).val('');
                    $('#' + selectedListID + ' li:last').data('id', id);
                    $('#' + inputFieldID).focus();
                    event.preventDefault();
                }
            });
            $('option[selected]', this).each(function () {
                $('#' + selectedListID).append('<li>' + $(this).text() + '<a href="#" class="closebutton" /></li>');
                $('#' + selectedListID + ' li:last').data('id', $(this).attr('value'));
            });
            $(this).hide();
            $('#' + selectedListID + ' a.closebutton').live('click', function (event) {
                var li = $(this).parents('li:first');
                var id = li.data('id');
                li.remove();
                $('option[value=' + id + ']', selectField).attr('selected', false);
                event.preventDefault();
            });
        });
    },

    destruct: function () {
        self.MutipleSelectAutoCompleteManager = null;
    }

}

$(document).ready(function () {
    self.MutipleSelectAutoCompleteManager.init();
});


$(window).unload(function () {
    self.MutipleSelectAutoCompleteManager.destruct();
});

