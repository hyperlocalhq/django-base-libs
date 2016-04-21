/* global self:false, jQuery:false, google:false */

var gettext = function (val) {
    
    var return_val = trans[val];
    if (!return_val || return_val == "") return_val = val;
    
    return return_val;
};

(function ($, undefined) {
    self.reinit_maps = function () {
        $('.map_canvas').each(function() {
            // don't apply maps if they are already applied
            if ($(this).data('initialized')) {
                return;
            }
            
            $(this).html('');
            
            var $context = $(this).closest('fieldset');
            // don't apply maps for hidden forms
            var $test = $('[id^="id_"][id$="latitude"]', $context);
            if ($test.length && $test.attr('id').indexOf('__prefix__') !== -1) {
                return;
            }
            
            var gMap;
            var gMarker;
            var gAllMarker = [];
            var gAllInfowindows = [];
            var showing_marker = 0;

            function getAddress4search() {
                var address = [];
                var sStreetAddress2 = $('[id^="id_"][id$="street_address2"]', $context).val();
                if (sStreetAddress2) {
                    sStreetAddress2 = ' ' + sStreetAddress2;
                }
                address.push($('[id^="id_"][id$="street_address"]', $context).val() + sStreetAddress2);
                address.push($('[id^="id_"][id$="city"]', $context).val());
                //address.push($('[id^="id_"][id$="country"]', $context).val());
                address.push($('[id^="id_"][id$="postal_code"]', $context).val());
                return address.join(', ');
            }
            function updateMarker(lat, lng) {
                var point = new google.maps.LatLng(lat, lng);
                if (gMarker) {
                    gMarker.setPosition(point);
                } else {
                    gMarker = new google.maps.Marker({
                        position: point,
                        map: gMap
                    });
                }
                gMap.panTo(point, 15);
                gMarker.setDraggable(true);
                google.maps.event.addListener(gMarker, 'dragend', function () {
                    var point = gMarker.getPosition();
                    updateLatitudeAndLongitude(point.lat(), point.lng());
                });
            }
            
            function updateAllMarker(lat, lng, title, institution, address) {
                var over = address;
                var click = address;
                if (institution) {
                    over = institution + " \n" + over;
                    click = institution + " <br/>" + click;
                }
                if (title && title.toLowerCase() != institution.toLowerCase()) {
                    over = title + " \n" + over;
                    click = title + " <br/>" + click;
                }
                
                
                var point = new google.maps.LatLng(lat, lng);
                var marker = new google.maps.Marker({
                    position: point,
                    map: gMap,
                    //title: name
                });
                
                var infowindow = new google.maps.InfoWindow({
                    content: click
                });
                marker.addListener('click', function() {
                    infowindow.open(gMap, marker);
                });
                marker.addListener('mouseover', function() {
                    infowindow.open(gMap, marker);
                });
                
                gAllMarker.push(marker);
                gAllInfowindows.push(infowindow);
                
                gAllInfowindows[showing_marker].open(gMap, gAllMarker[showing_marker]);
                gMap.panTo(gAllMarker[showing_marker].position, 15);
            }
            
            function updateLatitudeAndLongitude(lat, lng) {
                lat = Math.round(lat * 1000000) / 1000000;
                lng = Math.round(lng * 1000000) / 1000000;
                $('[id^="id_"][id$="latitude"]', $context).val(lat);
                $('[id^="id_"][id$="longitude"]', $context).val(lng);
            }
            function autocompleteAddress(results) {
                var $foundLocations = $('.map_locations', $context).html('');
                var $foundLocations_ul = $('<ul></ul>');
                $foundLocations.append($foundLocations_ul);
                var i, len = results.length;

                // console.log(JSON.stringify(results, null, 4));

                if (results) {
                    if (len > 1) {
                        for (i=0; i<len; i++) {
                            $('<a href="">' + results[i].formatted_address + '</a>').data('gmap_index', i).click(function (e) {
                                e.preventDefault();
                                var result = results[$(this).data('gmap_index')];
                                updateAddressFields(result.address_components);
                                var point = result.geometry.location;
                                updateLatitudeAndLongitude(point.lat(), point.lng());
                                updateMarker(point.lat(), point.lng());
                                $foundLocations.hide();
                            }).appendTo($('<li>').appendTo($foundLocations_ul));
                        }
                        $('<a href="">' + gettext('None of the listed') + '</a>').click(function (e) {
                            e.preventDefault();
                            $foundLocations.hide();
                        }).appendTo($('<li>').appendTo($foundLocations_ul));
                        $foundLocations.show();
                    } else {
                        $foundLocations.hide();
                        var result = results[0];
                        updateAddressFields(result.address_components);
                        var point = result.geometry.location;
                        updateLatitudeAndLongitude(point.lat(), point.lng());
                        updateMarker(point.lat(), point.lng());
                    }
                }
            }
            function updateAddressFields(addressComponents) {
                var i, len=addressComponents.length;
                var streetName, streetNumber;
                for (i=0; i<len; i++) {
                    var obj = addressComponents[i];
                    var obj_type = obj.types[0];
                    if (obj_type === 'locality') {
                        $('[id^="id_"][id$="city"]', $context).val(obj.long_name);
                    }
                    if (obj_type === 'street_number') {
                        streetNumber = obj.long_name;
                    }
                    if (obj_type === 'route') {
                        streetName = obj.long_name;
                    }
                    if (obj_type === 'postal_code') {
                        $('[id^="id_"][id$="postal_code"]', $context).val(obj.long_name);
                    }
                    //if (obj_type === 'country') {
                    //    $('[id^="id_"][id$="country"]').val(obj.short_name);
                    //}
                }
                if (streetName) {
                    var streetAddress = streetName;
                    if (streetNumber) {
                        streetAddress += ' ' + streetNumber;
                    }
                    $('[id^="id_"][id$="street_address"]', $context).val(streetAddress);
                }
            }

            $('.locate_address').click(function () {
                var oGeocoder = new google.maps.Geocoder();
                oGeocoder.geocode(
                    {address: getAddress4search()},
                    function (results, status) {
                        if (status === google.maps.GeocoderStatus.OK) {
                            autocompleteAddress(results);
                        } else {
                            autocompleteAddress(false);
                        }
                    }
                );
            });

            $('.remove_geo').click(function () {
                $('[id^="id_"][id$="latitude"]', $context).val('');
                $('[id^="id_"][id$="longitude"]', $context).val('');
                gMarker.setMap(null);
                gMarker = null;
            });
            
            $('.next-location', $context).click(function () {
                
                var $this = $(this);
                
                showing_marker++;
                if (showing_marker >= gAllMarker.length) showing_marker = 0;
                
                for (var i=0, length=gAllInfowindows.length; i<length; i++) {
                    gAllInfowindows[i].close();
                }
                
                gAllInfowindows[showing_marker].open(gMap, gAllMarker[showing_marker]);
                gMap.panTo(gAllMarker[showing_marker].position, 15);
                
                $this.blur();
            });

            gMap = new google.maps.Map($('.map_canvas', $context).get(0), {
                scrollwheel: false,
                zoom: 16,
                center: new google.maps.LatLng(52.523781, 13.411895),
                disableDoubleClickZoom: true
            });
            google.maps.event.addListener(gMap, 'dblclick', function (event) {
                updateLatitudeAndLongitude(event.latLng.lat(), event.latLng.lng());
                updateMarker(event.latLng.lat(), event.latLng.lng());
            });
            $('.map_locations', $context).hide();

            var $lat = $('[id^="id_"][id$="latitude"]', $context);
            var $lng = $('[id^="id_"][id$="longitude"]', $context);
            if ($lat.val() && $lng.val()) {
                updateMarker($lat.val(), $lng.val());
            } else {
                var counter = 0;
                var found = false;
                do {
                    found = false;
                    var $lat = $('[id^="id_"][id$="latitude_'+counter+'"]', $context);
                    var $lng = $('[id^="id_"][id$="longitude_'+counter+'"]', $context);
                    var $title = $('[id^="id_"][id$="title_'+counter+'"]', $context);
                    var $institution = $('[id^="id_"][id$="institution_'+counter+'"]', $context);
                    var $address = $('[id^="id_"][id$="address_'+counter+'"]', $context);
                    if ($lat.val() && $lng.val()) {
                        updateAllMarker($lat.val(), $lng.val(), $title.val(), $institution.val(), $address.val());
                        found = true;
                        counter++;
                    }
                } while (found);
            }

            if (gAllMarker.length < 2) {
                $('.next-location', $context).css('display', 'none');
            } else {
                $('.next-location', $context).css('display', '');
            }
            
            if (gAllMarker.length == 0) {
                $(this).closest('.static-map').css('display', 'none');
            } else {
                $(this).closest('.static-map').css('display', '');
            }
            
            $(this).data('initialized', true);
            $(this).data('gmap', gMap);
        });
    };

    $(document).ready(self.reinit_maps);

}(jQuery));
