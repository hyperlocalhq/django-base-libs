(function($){  
    $.fn.autoscroll = function() {
        $('html,body').animate(
            {
                scrollLeft: this.offset().left,
                scrollTop: this.offset().top
            },
            500
        );
        return this;
    };  
})(jQuery);

var oMap;

(function($, undefined) {
    var oInfobox;
    var aMarkers = [];
    var oCurrentMarker = null;
    
    $(document).ready(function() {
        var $oList = $('body');
        if ($oList.length) {
            var oOptions = {
                zoom: 13,
				mapTypeControl: false,
				zoomControl: true,
				streetViewControl: true,                
                center: new google.maps.LatLng(52.515306, 13.363863),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                navigationControlOptions: {
                    style: google.maps.NavigationControlStyle.SMALL
                }
            };
            var oNode = document.getElementById("gmap");
            if (oNode) {
                oMap = new google.maps.Map(oNode, oOptions);
            }
            $oList.bind(
                'before_list_load',
                before_list_load
            ).bind(
                'after_list_load',
                after_list_load
            ).bind(
                'map_filter',
                map_filter
            );
            if (!location.hash) {
                $oList.trigger('after_list_load');
            } else {
                $oList.trigger('before_list_load');
            }
        }
    });
    
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
        var sMarkerImg;
        for (i=0, iLen=aPos.length; i<iLen; i++) {
            // DEFINE IMAGE
            if (i < 10) {
                sMarkerImg = window.settings.STATIC_URL + "site/img/gmap/markers_1-10.png"
                iMarkerImgY = (-34 * i);
            } else if (i < 26) {
                sMarkerImg = window.settings.STATIC_URL + "site/img/gmap/markers_11-26.png"
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

            oMarker.categories = aPos[i]['categories'];
            aMarkers.push(oMarker);
            aPoints.push(oPoint);
            
            // DRAW MARKER LINK
            $('.location:eq(' + i + ')').data('marker_obj', oMarker).click(function() {
                oMap.setCenter($(this).data('marker_obj').getPosition());
                google.maps.event.trigger($(this).data('marker_obj'), "click");
                //oMap.setCenter($(this).data('marker_obj').getPosition());
                //oMap.setZoom(16);
                //$("#museum_list_map").autoscroll();
                console.log ("test")
                // $('html, body').animate({scrollTop:0}, 'slow');
                $('body').addClass('map_visible');
                setTimeout(function() {
                    google.maps.event.trigger(oMap, 'resize');
                }, 600);
                return false;
            });
        }
        // FIT MAP
        if (document.location.search) {
            fit_map(oMap, aPoints);
        }

    }
    
    function map_filter(event, param) {
        var categories = param.filter;
        $(aMarkers).each(function() {
            var oMarker = this;
            var bVisible = true;
            var iLen = categories.length;
            var oRe, sCat;
            for(i=0; i<iLen; i++) {
                sCat = categories[i].replace(/\./, "");
                oRe = new RegExp("\\b" + sCat + "\\b");
                if (!oMarker.categories.match(oRe)) {
                    bVisible = false;
                    break;
                }
            }
            oMarker.setVisible(bVisible);
        });
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

