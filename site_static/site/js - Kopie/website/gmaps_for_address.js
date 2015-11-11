(function($, undefined) {
    var sGMapImagePath = window.settings.STATIC_URL + "site/img/gmap/";
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
                if (status == google.maps.GeocoderStatus.OK) {
                    fCallback(results);
                } else {
                    fCallback(false);
                }
            }
        );
    }
    
    self.GMapManager = {
        init: function() {
            var oSelf = self.GMapManager;
            var $oDynMapContainer = $("#dyn_set_map").removeClass("hidden");
            if ($oDynMapContainer.length) {
                $("#dyn_locate_geo").click(oSelf.recognizeLocation);
                $("#dyn_remove_geo").click(oSelf.removeGeoPos);
                var $oGmap = $('<div id="gmap">').prependTo($oDynMapContainer);
                var oOptions = {
                    zoom: 15,
                    center: new google.maps.LatLng(52.523781, 13.411895),
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    mapTypeControlOptions: {
                        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                    },
                    disableDoubleClickZoom: true
                };
                oMap = new google.maps.Map($oGmap.get(0), oOptions);
                google.maps.event.addListener(oMap, 'dblclick', function(event) {
                    $("#id_latitude").val(event.latLng.lat());
                    $("#id_longitude").val(event.latLng.lng());
                    oSelf.adjustGeoposition()
                });
                $oGmapLocations = $('<ul id="gmap_locations">').appendTo($oDynMapContainer).hide();
                oSelf.adjustGeoposition();
                $("#id_street_address").blur(oSelf.recognizeLocation);
                $("#id_street_address2").blur(oSelf.recognizeLocation);
                $("#id_postal_code").blur(oSelf.recognizeLocation);
                $("#id_city").blur(oSelf.recognizeLocation);
                $("#id_country").change(oSelf.recognizeLocation);
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
            var oSelf = self.GMapManager;
            $("#id_latitude").val("");
            $("#id_longitude").val("");
            oMarker.setMap(null);
        },
        getAddress4search: function() {
            var aFullAddress = [];
            aFullAddress.push(
                $("#id_street_address").val()
                + " " + $("#id_street_address2").val()
            );
            aFullAddress.push($("#id_city").val());
            aFullAddress.push($("#id_country").val());
            aFullAddress.push($("#id_postal_code").val());
            return aFullAddress.join(", ");
        },
        adjustGeoposition: function() {
            var oSelf = self.GMapManager;
            var $oLat = $("#id_latitude");
            var $oLng = $("#id_longitude");
            if ($oLat.val() && $oLng.val()) {
                oSelf.markGeoposition($oLat.val(), $oLng.val());
            }
        },
        drawMarker: function(oPoint) {
            var oSelf = self.GMapManager;
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
            
            oMarker = new google.maps.Marker({
                position: oPoint,
                map: oMap,
                shadow: oShadow,
                icon: oImage
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
        correctGeoposition: function(iLat, iLng, oParams) {
            iLat = Math.round(iLat * 1000000) / 1000000;
            iLng = Math.round(iLng * 1000000) / 1000000;
    
            $("#id_latitude").val(iLat);
            $("#id_longitude").val(iLng);
        },
        autocompleteAddress: function(oResults) {
            aGmapsSearchResults = oResults;
            
            $oGmapLocations.html("");
            var iLen = oResults.length;
            if (aGmapsSearchResults) {
                if (iLen > 1) {
                    for (i=0; i<iLen; i++) {
                        $('<a href="">' + oResults[i].formatted_address + '</a>').data("gmap_index", i).click(function() {
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
                        }).appendTo($('<li>').appendTo($oGmapLocations));
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
            var oSelf = self.GMapManager;
            var i, iLen=aAddressComponents.length;
            var sStreetName, sStreetNumber;
            for (i=0; i<iLen; i++) {
                oObj = aAddressComponents[i];
                switch (oObj.types[0]) {
                    case "locality":
                        document.getElementById("id_city").value = oObj.long_name;
                        break;
                    case "street_number":
                        sStreetNumber = oObj.long_name;
                        break;
                    case "route":
                        sStreetName = oObj.long_name;
                        break;
                    case "postal_code":
                        document.getElementById("id_postal_code").value = oObj.long_name;
                        break;
                    case "country":
                        document.getElementById("id_country").value = oObj.short_name;
                        break;
                }
            }
            if (sStreetName) {
                var sStreetAddress = sStreetName;
                if (sStreetNumber) {
                    sStreetAddress += " " + sStreetNumber;
                }
                var $oStreetAddress = $("#id_street_address"); 
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
