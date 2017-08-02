(function($, undefined) {
    var oMap, oInfobox, oOverlay;
    var aMarkers = [];
    var oCurrentPos, oCurrentPosMarker;
    var oReInnerScripts = /<script\b[^>]*>([\s\S]*?)<\/script>/gm;
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(oPos) {
            oCurrentPos = oPos.coords;
            if (oMap) {
                mark_current_position();
            }
        }, function() {
            oCurrentPos = {
                latitude: 52.523781,
                longitude: 13.411895
            };
            if (oMap) {
                mark_current_position();
            }
        });
    } else {
        oCurrentPos = {
            latitude: 52.523781,
            longitude: 13.411895
        };
    }
    
    $(document).ready(function() {
        var $oList = $('#object_list');
        if ($oList.length) {
            var oCenterPos = oCurrentPos?
                new google.maps.LatLng(oCurrentPos.latitude, oCurrentPos.longitude):
                new google.maps.LatLng(52.523781, 13.411895);
            var oOptions = {
                zoom: 15,
                center: oCenterPos,
                disableDoubleClickZoom: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                navigationControlOptions: {
                    style: google.maps.NavigationControlStyle.SMALL
                }
            };
            oMap = new google.maps.Map(document.getElementById("gmap"), oOptions);
            $oList.bind(
                'before_list_load',
                before_list_load
            ).bind(
                'after_list_load',
                after_list_load
            );
            if (oCurrentPos) {
                mark_current_position();
            }
            google.maps.event.addListener(oMap, 'dblclick', function(oEvent) {
                oCurrentPos = {
                    latitude: oEvent.latLng.lat(),
                    longitude: oEvent.latLng.lng()
                };
                if (oCurrentPosMarker) {
                    // move marker
                    oCurrentPosMarker.setPosition(oEvent.latLng);
                    oMap.panTo(oEvent.latLng);
                    find_closest_objects();
                } else {
                    // set marker
                    mark_current_position();
                }
            });
        }
    });

    
    // Returns an array of GLatLng instances representing the desired points of the
    // radius circle
    var get_overlay_points = function(lat, lng, radius, earth){
        var lat = (lat * Math.PI) / 180; //rad
        var lon = (lng * Math.PI) / 180; //rad
        var d = parseFloat(radius) / earth; // d = angular distance covered on earth's surface
        var aPoints = [];
        var nMinLat = 360, nMaxLat = 0;
        var nMinLng = 90, nMaxLng = -90;
        for (x = 0; x <= 360; x++) { 
            brng = x * Math.PI / 180; //rad
            var destLat = Math.asin(Math.sin(lat)*Math.cos(d) + Math.cos(lat)*Math.sin(d)*Math.cos(brng));
            var destLng = ((lon + Math.atan2(Math.sin(brng)*Math.sin(d)*Math.cos(lat), Math.cos(d)-Math.sin(lat)*Math.sin(destLat))) * 180) / Math.PI;
            destLat = (destLat * 180) / Math.PI;
            if (destLat < nMinLat) {
                nMinLat = destLat;
            }
            if (destLat > nMaxLat) {
                nMaxLat = destLat;
            }
            if (destLng < nMinLng) {
                nMinLng = destLng;
            }
            if (destLng > nMaxLng) {
                nMaxLng = destLng;
            }
            aPoints.push(new google.maps.LatLng(destLat, destLng));
        }
        return {
            aPath: aPoints,
            nMinLat: nMinLat,
            nMaxLat: nMaxLat,
            nMinLng: nMinLng,
            nMaxLng: nMaxLng
        };
    }
    
    // Returns the radius of the earth in the passed unit
    var getEarthRadius = function(key){
        return {
            'mi': 3963.1676,
            'km': 6378.1,
            'ft': 20925524.9,
            'mt': 6378100,
            'in': 251106299,
            'yd': 6975174.98,
            'fa': 3487587.49,
            'na': 3443.89849,
            'ch': 317053.408,
            'rd': 1268213.63,
            'fr': 31705.3408
        }[key]
    }
    
    var redraw = function(){
        // If there's no point stored, we can't do anything
        if (!oCurrentPosMarker) return;
        // If there's an existing overlay, destroy it
        if (oOverlay) {
            oOverlay.setMap(null)
            oOverlay = null;
        }
        // Figure out the radius of the earth in the selected unit
        var nEarth = getEarthRadius("km");
        // And the radius in the entered units
        var nRadius = parseFloat(Number($('#distance').val()));
        if (!nRadius) return;
        // Draw the circle
        var oPos = oCurrentPosMarker.getPosition();
        var oPoints = get_overlay_points(oPos.lat(), oPos.lng(), nRadius, nEarth);
        oOverlay = new google.maps.Polygon({
            paths: oPoints.aPath,
            strokeColor: '#004de8',
            strokeOpacity: 1,
            strokeWeight: 0.62,
            fillColor: '#004de8',
            fillOpacity: 0.27
        });
        oOverlay.setMap(oMap);
        return oPoints;
    }
    
    function mark_current_position() {
        var oPoint = new google.maps.LatLng(oCurrentPos.latitude, oCurrentPos.longitude);
        var oImage = new google.maps.MarkerImage(
            window.settings.STATIC_URL + "site/img/gmap/marker.png",
            // marker size
            new google.maps.Size(20, 34),
            // origin
            new google.maps.Point(0, 0),
            // anchor
            new google.maps.Point(9, 34)
        );
        var oShadow = new google.maps.MarkerImage(
            "http://www.google.com/mapfiles/shadow50.png",
            // The shadow image is larger in the horizontal dimension
            // while the position and offset are the same as for the main image.
            new google.maps.Size(37, 34),
            new google.maps.Point(0, 0),
            new google.maps.Point(8, 34)
        );
        
        oCurrentPosMarker = new google.maps.Marker({
            position: oPoint,
            map: oMap,
            shadow: oShadow,
            icon: oImage,
            title: gettext("Drag me to show creativity around me!"),
            draggable: true
        });
        oMap.panTo(oPoint);
        //oMap.setCenter(oPoint, 15);
        google.maps.event.addListener(oCurrentPosMarker, 'dragstart', function() {
            if (oInfobox) {
                oInfobox.close();
            }
        });
        google.maps.event.addListener(oCurrentPosMarker, 'dragend', function() {
            oMap.panTo(oCurrentPosMarker.getPosition());
            find_closest_objects();
        });
        setTimeout(find_closest_objects, 200);
    }
    
    function find_closest_objects() {
        var oPoints = redraw();
        var oPos = oCurrentPosMarker.getPosition();
        sUrl = "./object-list/?" + $.param({
            center_lat: oPos.lat(),
            center_lng: oPos.lng(),
            distance: $('#distance').val()
            
        });
        $('#object_list').trigger("before_list_load").animate({opacity: 0.25}, 500, function() {
            if (!$(this).data('loading')) {
                $(this).css('opacity', 1);
            }
        }).data('loading', true).load(
            sUrl + " #object_list>*",
            list_loaded
        );
    }

    function list_loaded(responseText, textStatus, XMLHttpRequest) {
        if ("success|notmodified".indexOf(textStatus) != -1) {
            var $oList = $('#object_list');
            var sScripts = "";
            responseText.replace(
                oReInnerScripts,
                function($0, $1) {sScripts += $1;return $0;}
            );
            eval(sScripts);
            $oList.css('opacity', 1).data('loading', false).trigger("after_list_load");
        }
    }
    
    function before_list_load() {
        if (oInfobox) {
            oInfobox.close();
        }
        self.aGeopositions = [];
        for (var i=0, iLen=aMarkers.length; i<iLen;i++) {
            aMarkers[i].setMap(null);
        }
        aMarkers = [];
    }
    
    function after_list_load() {
        var aPos = self.aGeopositions || [];
        /* the center of the map should be (x, y), where 
        x = avg(min(xx), max(xx))
        y = avg(min(yy), max(yy))
        xx is the array of latitudes
        yy is the array of longitudes
        */
        var lat_min = long_min = 500;
        var lat_max = long_max = -500;
        var aPoints = [];
        var sBg, sMarkerImg;
        for (i=0, iLen=aPos.length; i<iLen; i++) {
            // DEFINE IMAGE
            if (i < 10) {
                sMarkerImg = window.settings.STATIC_URL + "site/img/gmap/markers_1-10.png"
                iMarkerImgY = (-34 * i);
            } else if (i < 26) {
                sMarkerImg = window.settings.STATIC_URL + "site/gmap/markers_11-26.png"
                iMarkerImgY = (-34 * (i - 10));
            } else {
                sMarkerImg = window.settings.STATIC_URL + "site/img/gmap/markers_1-10.png"
                iMarkerImgY = (-340);
            }
            
            iLat = aPos[i]['latitude'];
            iLong = aPos[i]['longitude'];
            if (lat_max < iLat)
                lat_max = iLat;
            if (iLat < lat_min)
                lat_min = iLat;
            if (long_max < iLong)
                long_max = iLong;
            if (iLong < long_min)
                long_min = iLong;
            var oPoint = new google.maps.LatLng(iLat, iLong);
            
            // DRAW MARKER
            var oImage = new google.maps.MarkerImage(
                sMarkerImg,
                // This marker is 20 pixels wide by 32 pixels tall.
                new google.maps.Size(20, 34),
                // The origin for this image is 0,0.
                new google.maps.Point(0, -iMarkerImgY),
                // The anchor for this image is the base of the flagpole at 0,32.
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
            
            var oMarker = new google.maps.Marker({
                position: oPoint,
                map: oMap,
                shadow: oShadow,
                icon: oImage
            });
            oMarker.list_index = i;
            (function(oMarker, sContent) {
                google.maps.event.addListener(oMarker, 'click', function() {
                    oInfobox = new StyledInfoWindow({
                        position: oMarker.getPosition(),
                        map: oMap,
                        content: sContent
                    });
                });
            }(oMarker, aPos[i]['content']));

            aMarkers.push(oMarker);
            aPoints.push(oPoint);
            
            // DRAW MARKER LINK
            $('.marker-link:eq(' + i + ')').append(
                $('<a href=""></a>').css({
                    border: "none",
                    display: "block",
                    overflow: "hidden",
                    height: "24px",
                    width: "24px",
                    background: sBg
                })
            ).data('marker_obj', oMarker).click(function() {
                google.maps.event.trigger($(this).data('marker_obj'), "click");
                //oMap.setCenter($(this).data('marker_obj').getPosition());
                //oMap.setZoom(16);
                $("#dyn_map").autoscroll();
                return false;
            });
        }
        // FIT MAP
        //fit_map(oMap, aPoints);

    }
    
    function fit_map(oMap, aPoints) {
        var oBounds = new google.maps.LatLngBounds();
        for (var i=0, iLen=aPoints.length; i<iLen; i++) {
            oBounds.extend(aPoints[i]);
        }
        var oNEPoint = oBounds.getNorthEast();
        oBounds.extend(new google.maps.LatLng(
            oNEPoint.lat() - .005,
            oNEPoint.lng() - .005
        ));
        
        var oSWPoint = oBounds.getNorthEast();
        oBounds.extend(new google.maps.LatLng(
            oSWPoint.lat() + .005,
            oSWPoint.lng() + .005
        ));
        oMap.fitBounds(oBounds);
    }
}(jQuery));

