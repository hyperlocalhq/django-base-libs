/*global self:false, jQuery:false, google:false */

(function($, undefined) {
    var gettext = window.gettext || function(val) {return val;};
    var aMaps = {}, aMarkers = {};
    var $oGmapLocations = {};
    var aGmapsSearchResults = {};

    function setMarkerDraggable(nIndex, oMarker, fCallback, oParams) {
        oMarker.setDraggable(true);
        google.maps.event.addListener(oMarker, "dragend", function() {
            var oPoint = oMarker.getPosition();
            fCallback(nIndex, oPoint.lat(), oPoint.lng(), oParams);
        });
    }

    function recognizeLocation(nIndex, sAddress, fCallback) {
        var oGeocoder = new google.maps.Geocoder();
        oGeocoder.geocode(
            {address: sAddress},
            function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    fCallback(nIndex, results);
                } else {
                    fCallback(nIndex, false);
                }
            }
        );
    }

    var GMapManager = self.GMapManager = {
        init_all: function() {
            var oSelf = self.GMapManager;
            $('.gmap-wrapper').each(function(nIndex, el) {
                if (!$(el).closest('.grp-empty-form').length) {
                    oSelf.init(nIndex);
                }
            });
        },
        init: function(nIndex) {
            var oSelf = self.GMapManager;
            var $oDynMapContainer = $('.gmap-wrapper:eq(' + nIndex + ')');
            if ($oDynMapContainer.length) {
                $('.dyn_locate_geo:eq(' + nIndex + ')').click(function() {oSelf.recognizeLocation(nIndex);});
                $('.dyn_remove_geo:eq(' + nIndex + ')').click(function() {oSelf.removeGeoPos(nIndex);});
                var $oGmap = $('<div class="gmap">').prependTo($oDynMapContainer);
                var oOptions = {
                    mapTypeControl: false,
                    zoomControl: true,
                    streetViewControl: true,
                    scrollwheel: false,
                    zoom: 15,
                    center: new google.maps.LatLng(52.523781, 13.411895),
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    zoomControlOptions: {
                        style: google.maps.ZoomControlStyle.SMALL
                    },
                    disableDoubleClickZoom: true
                };
                aMaps[nIndex] = new google.maps.Map($oGmap.get(0), oOptions);
                google.maps.event.addListener(aMaps[nIndex], 'dblclick', function(event) {
                    $('[id$="latitude"]:eq(' + nIndex + ')').val(event.latLng.lat());
                    $('[id$="longitude"]:eq(' + nIndex + ')').val(event.latLng.lng());
                    oSelf.adjustGeoposition(nIndex);
                });
                $oGmapLocations[nIndex] = $('<ul class="gmap_locations">').appendTo($oDynMapContainer).hide();
                oSelf.adjustGeoposition(nIndex);
                $oDynMapContainer.parents('.grp-collapse').on('click', function(e) {
                    if ($oDynMapContainer.is(':visible')) {
                        e.preventDefault();
                        google.maps.event.trigger(aMaps[nIndex], 'resize');
                    }
                });
            }
        },
        recognizeLocation: function(nIndex) {
            var oSelf = self.GMapManager;
            recognizeLocation(
                nIndex,
                oSelf.getAddress4search(nIndex),
                oSelf.autocompleteAddress
            );
        },
        removeGeoPos: function(nIndex) {
            $('[id$="latitude"]:eq(' + nIndex + ')').val("");
            $('[id$="longitude"]:eq(' + nIndex + ')').val("");
            if (aMarkers[nIndex]) {
                aMarkers[nIndex].setMap(null);
            }
        },
        getAddress4search: function(nIndex) {
            var aFullAddress = [];
            aFullAddress.push(
                $('[id$="street_address"]:eq(' + nIndex + ')').val() +
                ' ' + $('[id$="street_address2"]:eq(' + nIndex + ')').val()
            );
            aFullAddress.push($('[id$="city"]:eq(' + nIndex + ')').val());
            aFullAddress.push("Germany");
            aFullAddress.push($('[id$="postal_code"]:eq(' + nIndex + ')').val());
            return aFullAddress.join(", ");
        },
        adjustGeoposition: function(nIndex) {
            var oSelf = self.GMapManager;
            var $oLat = $('[id$="latitude"]:eq(' + nIndex + ')');
            var $oLng = $('[id$="longitude"]:eq(' + nIndex + ')');
            if ($oLat.val() && $oLng.val()) {
                oSelf.markGeoposition(nIndex, $oLat.val(), $oLng.val());
            }
        },
        drawMarker: function(nIndex, oPoint) {
            aMarkers[nIndex] = new google.maps.Marker({
                position: oPoint,
                map: aMaps[nIndex]
            });
        },
        markGeoposition: function(nIndex, iLat, iLong) {
            var oSelf = self.GMapManager;
            var oPoint = new google.maps.LatLng(iLat, iLong);
            if (aMarkers[nIndex]) {
                aMarkers[nIndex].setMap(null);
                aMarkers[nIndex] = null;
            }
            oSelf.drawMarker(nIndex, oPoint);

            aMaps[nIndex].panTo(oPoint, 15);

            setMarkerDraggable(
                nIndex,
                aMarkers[nIndex],
                oSelf.correctGeoposition,
                {bNoSuggest: true}
            );
        },
        correctGeoposition: function(nIndex, iLat, iLng) {
            iLat = Math.round(iLat * 1000000) / 1000000;
            iLng = Math.round(iLng * 1000000) / 1000000;

            $('[id$="latitude"]:eq(' + nIndex + ')').val(iLat);
            $('[id$="longitude"]:eq(' + nIndex + ')').val(iLng);
        },
        autocompleteAddress: function(nIndex, oResults) {
            aGmapsSearchResults[nIndex] = oResults;

            $oGmapLocations[nIndex].html("");
            var i, iLen = oResults.length;
            function choose_location(nIndex, nChoiceIndex) {

                var oResult = aGmapsSearchResults[nIndex][nChoiceIndex];
                var aAddressComponents = oResult.address_components;
                GMapManager.extractFromXAL(nIndex, aAddressComponents);
                var oPoint = oResult.geometry.location;
                var bSuggesting = GMapManager.correctGeoposition(
                    nIndex,
                    oPoint.lat(),
                    oPoint.lng(),
                    {}
                );
                if (!bSuggesting) {
                    GMapManager.markGeoposition(
                        nIndex,
                        oPoint.lat(),
                        oPoint.lng()
                    );
                }
                $oGmapLocations[nIndex].hide();
            }
            if (aGmapsSearchResults[nIndex]) {
                if (iLen > 1) {
                    for (i=0; i<iLen; i++) {
                        $('<a href="">' + oResults[i].formatted_address + '</a>').data('gmap_index', i).click(function(e) {
                            e.preventDefault();
                            choose_location(nIndex, $(this).data('gmap_index'));
                        }).appendTo($('<li>').appendTo($oGmapLocations[nIndex]));
                    }
                    $('<a href="">' + gettext("None of the listed") + '</a>').click(function() {
                        $oGmapLocations[nIndex].hide();
                        return false;
                    }).appendTo($('<li>').appendTo($oGmapLocations[nIndex]));
                    $oGmapLocations[nIndex].show();
                } else {
                    $oGmapLocations[nIndex].hide();
                    var oResult = aGmapsSearchResults[nIndex][0];
                    var aAddressComponents = oResult.address_components;
                    GMapManager.extractFromXAL(nIndex, aAddressComponents);
                    var oPoint = oResult.geometry.location;
                    var bSuggesting = GMapManager.correctGeoposition(
                        nIndex,
                        oPoint.lat(),
                        oPoint.lng(),
                        {}
                    );
                    if (!bSuggesting) {
                        GMapManager.markGeoposition(
                            nIndex,
                            oPoint.lat(),
                            oPoint.lng()
                        );
                    }
                }
            }
        },
        extractFromXAL: function(nIndex, aAddressComponents) {
            var i, iLen=aAddressComponents.length;
            var sStreetName, sStreetNumber;
            for (i=0; i<iLen; i++) {
                var oObj = aAddressComponents[i];
                switch (oObj.types[0]) {
                    case "locality":
                        $('[id$="city"]:eq(' + nIndex + ')').val(oObj.long_name);
                        break;
                    case "street_number":
                        sStreetNumber = oObj.long_name;
                        break;
                    case "route":
                        sStreetName = oObj.long_name;
                        break;
                    case "postal_code":
                        $('[id$="postal_code"]:eq(' + nIndex + ')').val(oObj.long_name);
                        break;
                    case "country":
                        //document.getElementById("id_country").value = oObj.short_name;
                        break;
                }
            }
            if (sStreetName) {
                var sStreetAddress = sStreetName;
                if (sStreetNumber) {
                    sStreetAddress += " " + sStreetNumber;
                }
                var $oStreetAddress = $('[id$="street_address"]:eq(' + nIndex + ')');
                $oStreetAddress.val(sStreetAddress);
            }
        },
        destruct: function() {
            self.GMapManager = null;
        }
    };

    $(document).ready(function(){
        self.GMapManager.init_all();
    });

    $(window).unload(function() {
        self.GMapManager.destruct();
    });

}(jQuery));
