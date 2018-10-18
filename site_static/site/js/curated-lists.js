$(function() {
    $('.add_to_own_curated_lists').each(function() {
        var $oldWidget = $(this);
        var content_type_id = $oldWidget.data('content_type_id');
        var object_id = $oldWidget.data('object_id');
        var url = '/' + settings.lang + '/helper/user-curated-lists/?content_type_id=' + content_type_id + '&object_id=' + object_id;

        $.get(url, function(data) {
            /*
            From something like:

            [
              {
                "owner": {"type": "people.person", "id": 1, "title": "User"},
                "lists": [
                  {"token": "vbmOeY", "item_included": false, "title": "Berlin's Best"}
                ]
              },
              {
                "owner": {"type": "institutions.institution", "id": 543, "title": "Institution 1"},
                "lists": [
                  {"token": "penRe7", "item_included": false, "title": "Our Picks"},
                  {"token": "dfggs2", "item_included": false, "title": "The Best of 2018"}
                ]
              },
              {
                "owner": {"type": "institutions.institution", "id": 124, "title": "Institution 2"},
                "lists": [
                  {"token": "bdfgdf", "item_included": false, "title": "2018 Selection"}
                ]
              }
            ]

            Create something like:

            <div class="input-field select">
                <select placeholder="{% trans 'Add to curated list' %}" multiple>
                    <optgroup label="User">
                        <option value="vbmOeY">Favorites</option>
                        <option value="new">New Curated List...</option>
                    </optgroup>
                    <optgroup label="Institution 1">
                        <option value="penRe7">Our Picks</option>
                        <option value="dfggs2">The Best of 2018</option>
                        <option value="new">New Curated List...</option>
                    </optgroup>
                    <optgroup label="Institution 2">
                        <option value="bdfgdf">2018 Selection</option>
                        <option value="new">New Curated List...</option>
                    </optgroup>
                </select>
            </div>

            */

            var $newWidget = $('<select placeholder="Add to curated list" multiple></select>').wrap('<div class="add_to_own_curated_lists input-field select"></div>');
            for (i=0, ilen=data.length; i<ilen; i++) {
                var personOrInstitution = data[i];
                var owner = personOrInstitution.owner;
                var $optgroup = $('<optgroup label="' + owner.title + '"></optgroup>');
                for (j=0, jlen=personOrInstitution.lists.length; j<jlen; j++) {
                    var list = personOrInstitution.lists[j];
                    $option = $('<option value="' + list.token + '">' + list.title + '</option>');
                    if (list.item_included) {
                        $option.attr('selected', true);
                    }
                    $optgroup.append($option);
                }
                $option = $('<option value="new-for-' + owner.type + '.' + owner.id + '">New Curated List...</option>');
                $optgroup.append($option);
                $newWidget.append($optgroup);
            }
            $newWidget = $newWidget.parent(); // move up the DOM to the wrapping div

            $newWidget.replaceAll($oldWidget).each(function() {
                var $select = $(this).find('select');
                $select.data('previous-value', $select.val());
                new window.form_elements.SelectBox($select);
            });

            $newWidget.on('changed', function() {
                var curated_list_token;
                var $select = $(this).find('select');
                var newChoice = $select.val().filter(function(value) {
                    return -1 === ($select.data('previous-value') || []).indexOf(value);
                });
                var deletedChoice = ($select.data('previous-value') || []).filter(function(value) {
                    return -1 === ($select.val() || []).indexOf(value);
                });
                console.log({newChoice: newChoice.toString(), deletedChoice: deletedChoice.toString()});
                if (deletedChoice.toString()) {
                    curated_list_token = deletedChoice.toString();
                    $.post(
                        '/' + settings.lang + '/helper/user-curated-lists/remove-item/',
                        {
                            curated_list_token: curated_list_token,
                            item_content_type_id: content_type_id,
                            item_object_id: object_id
                        },
                        function(data) {
                            if (data.success) {
                                console.log('Item deleted from the curated list');
                            }
                        },
                        'json'
                    );
                }
                if (newChoice.toString()) {
                    curated_list_token = newChoice.toString();
                    if (curated_list_token.indexOf('new-for-') === 0) {
                        var owner_app_model_pk = curated_list_token.replace('new-for-', '').split('.');
                        var curated_list_title = prompt('Enter list title', 'My new list');
                        $.post(
                            '/' + settings.lang + '/helper/user-curated-lists/add-item-to-new/',
                            {
                                owner_app_model: owner_app_model_pk[0] + '.' + owner_app_model_pk[1],
                                owner_pk: owner_app_model_pk[2],
                                title: curated_list_title,
                                item_content_type_id: content_type_id,
                                item_object_id: object_id
                            },
                            function(data) {
                                if (data.success) {
                                    location.href = data.redirect_url;
                                }
                            },
                            'json'
                        );
                    } else {
                        $.post(
                            '/' + settings.lang + '/helper/user-curated-lists/add-item-to-existing/',
                            {
                                curated_list_token: curated_list_token,
                                item_content_type_id: content_type_id,
                                item_object_id: object_id
                            },
                            function(data) {
                                if (data.success) {
                                    location.href = data.redirect_url;
                                }
                            },
                            'json'
                        );
                    }
                }
                $select.data('previous-value', $select.val());
            });


        }, 'json');
    });
});
