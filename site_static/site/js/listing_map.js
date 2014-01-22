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
                styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#a2daf2"}]},{"featureType":"landscape.man_made","elementType":"geometry","stylers":[{"color":"#f7f1df"}]},{"featureType":"landscape.natural","elementType":"geometry","stylers":[{"color":"#d0e3b4"}]},{"featureType":"landscape.natural.terrain","elementType":"geometry","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#bde6ab"}]},{"featureType":"poi","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"poi.medical","elementType":"geometry","stylers":[{"color":"#fbd3da"}]},{"featureType":"poi.business","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffe15f"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#efd151"}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.local","elementType":"geometry.fill","stylers":[{"color":"black"}]},{"featureType":"transit.station.airport","elementType":"geometry.fill","stylers":[{"color":"#cfb2db"}]}],
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
                },
                zoomControlOptions: {
                    style: google.maps.ZoomControlStyle.SMALL
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
            $oList.trigger('after_list_load');
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
        /* the center of the map should be (x, y), where
        x = avg(min(xx), max(xx))
        y = avg(min(yy), max(yy))
        xx is the array of latitudes
        yy is the array of longitudes
        */
        var lat_min = long_min = 500;
        var lat_max = long_max = -500;
        var aPoints = [];
        var sMarkerImgDefault = self.settings.STATIC_URL + 'site/img/marker_default.png';
        var sMarkerImgSelected = self.settings.STATIC_URL + 'site/img/marker_selected.png';

        var oMarkerImgDefault = new google.maps.MarkerImage(sMarkerImgDefault, null, null, null, new google.maps.Size(20,30));
        var oMarkerImgSelected = new google.maps.MarkerImage(sMarkerImgSelected, null, null, null, new google.maps.Size(20,30));

        var oActiveMarker = null;

        var active_object_id = '';
        if (window.location.hash) {
            // get options object from hash
            var options = window.location.hash ? $.deparam.fragment(window.location.hash, true) : {};
            // apply options from hash
            active_object_id = options.object_id;
        }

        $(self.aGeopositions).each(function(i, el) {
            // DEFINE IMAGE
            var iLat = el.latitude;
            var iLong = el.longitude;
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
            // var oImage = new google.maps.MarkerImage(sMarkerImgDefault, null, null, null, new google.maps.Size(20,30));

            var oMarker = new google.maps.Marker({

                position: oPoint,
                map: oMap,
                icon: oMarkerImgDefault
            });


            oMarker.list_index = i;

            var $item = $(this);
            google.maps.event.addListener(oMarker, 'click', function() {
                if (oActiveMarker && oActiveMarker != oMarker) {
                    oActiveMarker.setIcon(oMarkerImgDefault);
                }
                oMarker.setIcon(oMarkerImgSelected);
                oActiveMarker = oMarker;
                $.bbq.pushState({object_id: oMarker.object_id});
                $('#map-description').load(el.html_src,function(){
                    $(".row-map").removeClass( "map-only" );
                    $(".row-map").removeClass( "map-filter" );
                    google.maps.event.trigger(oMap, "resize");
                    lazyload_images();
                });
            });
            oMarker.categories = el.categories;
            oMarker.object_id = el.object_id;
            aMarkers.push(oMarker);
            aPoints.push(oPoint);

            if (el.object_id == active_object_id) {
                oActiveMarker = oMarker;
            }
        });

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition  (
                function(position)  {
                    // var oImage = self.settings.STATIC_URL + 'site/img/marker_current.png';
                    var oImage = new google.maps.MarkerImage(self.settings.STATIC_URL + "site/img/marker_current.png", null, null, null, new google.maps.Size(20,30));

                    var oMarker = new google.maps.Marker({
                        position: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
                        map: oMap,
                        icon: oImage
                    });
                    oMarker.setZIndex(999);
                    google.maps.event.addListener(oMarker, 'click', function() {
                        $('#map-description').html("You are here!");
                    });
                },
                function(){
                    // alert('Unable to get location');
                },
                { enableHighAccuracy: true }
            );
        }
        // FIT MAP
        if (document.location.search) {
            fit_map(oMap, aPoints);
        }
        if (oActiveMarker) {
            oMap.setCenter(oActiveMarker.getPosition());
            google.maps.event.trigger(oActiveMarker, 'click');
        }
    }

    function map_filter(event, param) {
        var categories = param.filter;
        $(aMarkers).each(function() {
            var oMarker = this;
            var bVisible = true;
            var iLen = categories.length;
            var i, oRe, sCat;
            for(i=0; i<iLen; i++) {
                sCat = categories[i];
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

$(document).ready(function() {

    $( "#toggle-map-sidebar" ).click(function() {
        $(".row-map").toggleClass( "map-only" );
        google.maps.event.trigger(oMap, "resize");
        return false;
    });

    $( "#toggle-map-filter" ).click(function() {
        $(".row-map").toggleClass( "map-filter" );
        google.maps.event.trigger(oMap, "resize");
        return false;
    });
});


