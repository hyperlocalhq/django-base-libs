/* global self:false, jQuery:false, google:false */

var gettext = self.gettext || function (val) {return val;};

(function ($, undefined) {
    self.reinit_maps = function () {
        $('.map_canvas').each(function() {
            // don't apply maps if they are already applied
            if ($(this).data('initialized')) {
                return;
            }
            var $context = $(this).closest('fieldset');
            // don't apply maps for hidden forms
            if ($('[id^="id_"][id$="latitude"]', $context).attr('id').indexOf('__prefix__') !== -1) {
                return;
            }
            var gMap;
            var gMarker;

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
            function updateLatitudeAndLongitude(lat, lng) {
                lat = Math.round(lat * 1000000) / 1000000;
                lng = Math.round(lng * 1000000) / 1000000;
                $('[id^="id_"][id$="latitude"]', $context).val(lat);
                $('[id^="id_"][id$="longitude"]', $context).val(lng);
            }
            function autocompleteAddress(results) {
                var $foundLocations = $('.map_locations', $context).html('');
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
                            }).appendTo($('<li>').appendTo($foundLocations));
                        }
                        $('<a href="">' + gettext('None of the listed') + '</a>').click(function (e) {
                            e.preventDefault();
                            $foundLocations.hide();
                        }).appendTo($('<li>').appendTo($foundLocations));
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
            }

            $(this).data('initialized', true);
            $(this).data('gmap', gMap);
        });
    };

    $(document).ready(self.reinit_maps);

}(jQuery));
