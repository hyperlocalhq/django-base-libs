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
        var sMarkerImgDefault = "http://maps.google.com/mapfiles/marker_black.png";
        var sMarkerImgSelected = "http://maps.google.com/mapfiles/marker_orange.png";
        var oActiveMarker = null;

        $('.item').each(function(i) {
            // DEFINE IMAGE
            var iLat = parseFloat($(this).data('latitude'));
            var iLong = parseFloat($(this).data('longitude'));
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
            var oImage = new google.maps.MarkerImage(sMarkerImgDefault);

            var oMarker = new google.maps.Marker({
                position: oPoint,
                map: oMap,
                icon: oImage
            });

            oMarker.list_index = i;

            var $item = $(this);
            google.maps.event.addListener(oMarker, 'click', function() {
                if (oActiveMarker) {
                    oActiveMarker.setIcon(sMarkerImgDefault);
                }
                $('#item_description').html($item.html()).find('.description').load($item.data('description-src'));
                oMarker.setIcon(sMarkerImgSelected);
                oActiveMarker = oMarker;
            });

            //oMarker.categories = aPos[i]['categories'];
            aMarkers.push(oMarker);
            aPoints.push(oPoint);

            // DRAW MARKER LINK
            $('.location:eq(' + i + ')').data('marker_obj', oMarker).click(function() {
                oMap.setCenter($(this).data('marker_obj').getPosition());
                google.maps.event.trigger($(this).data('marker_obj'), "click");
                //oMap.setCenter($(this).data('marker_obj').getPosition());
                //oMap.setZoom(16);
                //$("#museum_list_map").autoscroll();
                // $('html, body').animate({scrollTop:0}, 'slow');
                $('body').addClass('map_visible');
                setTimeout(function() {
                    google.maps.event.trigger(oMap, 'resize');
                }, 600);
                return false;
            });
        });
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition  (
                function(position)  {
                    var oImage = new google.maps.MarkerImage("http://maps.google.com/mapfiles/arrow.png");
                    var oMarker = new google.maps.Marker({
                        position: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
                        map: oMap,
                        icon: oImage
                    });
                    oMarker.setZIndex(999);
                    google.maps.event.addListener(oMarker, 'click', function() {
                        $('#item_description').html("You are here!");
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

