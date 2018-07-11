$(function() {
    $.get('/' + settings.lang + '/helper/user-curated-lists/', function(data) {
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
                    $option.attr('checked', 'checked');
                }
                $optgroup.append($option);
            }
            $option = $('<option value="new-for-' + owner.type + '.' + owner.id + '">New Curated List...</option>');
            $optgroup.append($option);
            $newWidget.append($optgroup);
        }
        $newWidget = $newWidget.parent(); // move up the DOM to the wrapping div

        $newWidget.replaceAll('.add_to_own_curated_lists').each(function() {
            new window.form_elements.SelectBox($(this).find('select'));
        });

        $newWidget.on('change', function() {
            console.log($(this).find('select').val());
        });

        $newWidget.on('closed', function() {
            console.log($(this).find('select').val());
        });


    }, 'json');
});
