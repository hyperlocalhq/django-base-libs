/*global self:false, jQuery:false, google:false */

(function($, undefined) {
    var gettext = window.gettext || function(val) {return val;};
    var oMap, oMarker;
    var $oGmapLocations;
    var aGmapsSearchResults;

    function setMarkerDraggable(oMarker, fCallback, oParams) {
        oMarker.setDraggable(true);
        google.maps.event.addListener(oMarker, "dragend", function() {
            var oPoint = oMarker.getPosition();
            fCallback(oPoint.lat(), oPoint.lng(), oParams);
        });
    }

    function recognizeLocation(sAddress, fCallback) {
        var oGeocoder = new google.maps.Geocoder();
        oGeocoder.geocode(
            {address: sAddress},
            function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    fCallback(results);
                } else {
                    fCallback(false);
                }
            }
        );
    }

    var GMapManager = self.GMapManager = {
        init: function() {
            var oSelf = self.GMapManager;
            var $oDynMapContainer = $(".gmap-wrapper").removeClass("hidden");
            if ($oDynMapContainer.length) {
                $(".dyn_locate_geo").click(oSelf.recognizeLocation);
                $(".dyn_remove_geo").click(oSelf.removeGeoPos);
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
                oMap = new google.maps.Map($oGmap.get(0), oOptions);
                google.maps.event.addListener(oMap, 'dblclick', function(event) {
                    $('[id^="id_"][id$="latitude"]').val(event.latLng.lat());
                    $('[id^="id_"][id$="longitude"]').val(event.latLng.lng());
                    oSelf.adjustGeoposition();
                });
                $oGmapLocations = $('<ul class="gmap_locations">').appendTo($oDynMapContainer).hide();
                oSelf.adjustGeoposition();
            }
        },
        recognizeLocation: function() {
            var oSelf = self.GMapManager;
            recognizeLocation(
                oSelf.getAddress4search(),
                oSelf.autocompleteAddress
            );
        },
        removeGeoPos: function() {
            $('[id^="id_"][id$="latitude"]').val("");
            $('[id^="id_"][id$="longitude"]').val("");
            if (oMarker) {
                oMarker.setMap(null);
            }
        },
        getAddress4search: function() {
            var aFullAddress = [];
            aFullAddress.push(
                $('[id^="id_"][id$="street_address"]').val() +
                " " + $('[id^="id_"][id$="street_address2"]').val()
            );
            aFullAddress.push($('[id^="id_"][id$="city"]').val());
            aFullAddress.push("Germany");
            aFullAddress.push($('[id^="id_"][id$="postal_code"]').val());
            return aFullAddress.join(", ");
        },
        adjustGeoposition: function() {
            var oSelf = self.GMapManager;
            var $oLat = $('[id^="id_"][id$="latitude"]');
            var $oLng = $('[id^="id_"][id$="longitude"]');
            if ($oLat.val() && $oLng.val()) {
                oSelf.markGeoposition($oLat.val(), $oLng.val());
            }
        },
        drawMarker: function(oPoint) {
            /*
            var oImage = new google.maps.MarkerImage(
                window.settings.STATIC_URL + "site/img/gmap/markers_1-10.png",
                // marker size
                new google.maps.Size(20, 34),
                // origin
                new google.maps.Point(0, 340),
                // anchor
                new google.maps.Point(10, 34)
            );
            var oShadow = new google.maps.MarkerImage(
                window.settings.STATIC_URL + "site/img/gmap/marker_shadow.png",
                // The shadow image is larger in the horizontal dimension
                // while the position and offset are the same as for the main image.
                new google.maps.Size(37, 34),
                new google.maps.Point(0, 0),
                new google.maps.Point(8, 25)
            );
            */
            oMarker = new google.maps.Marker({
                position: oPoint,
                map: oMap/*,
                shadow: oShadow,
                icon: oImage*/
            });
        },
        markGeoposition: function(iLat, iLong) {
            var oSelf = self.GMapManager;
            var oPoint = new google.maps.LatLng(iLat, iLong);
            if (oMarker) {
                oMarker.setMap(null);
                oMarker = null;
            }
            oSelf.drawMarker(oPoint);

            oMap.panTo(oPoint, 15);


            setMarkerDraggable(
                oMarker,
                oSelf.correctGeoposition,
                {bNoSuggest: true}
            );
        },
        correctGeoposition: function(iLat, iLng) {
            iLat = Math.round(iLat * 1000000) / 1000000;
            iLng = Math.round(iLng * 1000000) / 1000000;

            $('[id^="id_"][id$="latitude"]').val(iLat);
            $('[id^="id_"][id$="longitude"]').val(iLng);
        },
        autocompleteAddress: function(oResults) {
            aGmapsSearchResults = oResults;

            $oGmapLocations.html("");
            var i, iLen = oResults.length;
            function choose_location() {
                var oResult = aGmapsSearchResults[$(this).data("gmap_index")];
                var aAddressComponents = oResult.address_components;
                GMapManager.extractFromXAL(aAddressComponents);
                var oPoint = oResult.geometry.location;
                var bSuggesting = GMapManager.correctGeoposition(
                    oPoint.lat(),
                    oPoint.lng(),
                    {}
                );
                if (!bSuggesting) {
                    GMapManager.markGeoposition(
                        oPoint.lat(),
                        oPoint.lng()
                    );
                }
                $oGmapLocations.hide();
                return false;
            }
            if (aGmapsSearchResults) {
                if (iLen > 1) {
                    for (i=0; i<iLen; i++) {
                        $('<a href="">' + oResults[i].formatted_address + '</a>').data("gmap_index", i).click(choose_location).appendTo($('<li>').appendTo($oGmapLocations));
                    }
                    $('<a href="">' + gettext("None of the listed") + '</a>').click(function() {
                        $oGmapLocations.hide();
                        return false;
                    }).appendTo($('<li>').appendTo($oGmapLocations));
                    $oGmapLocations.show();
                } else {
                    $oGmapLocations.hide();
                    var oResult = aGmapsSearchResults[0];
                    var aAddressComponents = oResult.address_components;
                    GMapManager.extractFromXAL(aAddressComponents);
                    var oPoint = oResult.geometry.location;
                    var bSuggesting = GMapManager.correctGeoposition(
                        oPoint.lat(),
                        oPoint.lng(),
                        {}
                    );
                    if (!bSuggesting) {
                        GMapManager.markGeoposition(
                            oPoint.lat(),
                            oPoint.lng()
                        );
                    }
                }
            }
        },
        extractFromXAL: function(aAddressComponents) {
            var i, iLen=aAddressComponents.length;
            var sStreetName, sStreetNumber;
            for (i=0; i<iLen; i++) {
                var oObj = aAddressComponents[i];
                switch (oObj.types[0]) {
                    case "locality":
                        $('[id^="id_"][id$="city"]').val(oObj.long_name);
                        break;
                    case "street_number":
                        sStreetNumber = oObj.long_name;
                        break;
                    case "route":
                        sStreetName = oObj.long_name;
                        break;
                    case "postal_code":
                        $('[id^="id_"][id$="postal_code"]').val(oObj.long_name);
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
                var $oStreetAddress = $('[id^="id_"][id$="street_address"]');
                $oStreetAddress.val(sStreetAddress);
            }
        },
        destruct: function() {
            //self.GMapManager = null;
        }
    };

    $(document).ready(function(){
        self.GMapManager.init();
    });

    $(window).unload(function() {
        self.GMapManager.destruct();
    });

}(jQuery));
