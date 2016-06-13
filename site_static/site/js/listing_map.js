/* jshint unused:false, eqnull:false */

/* global self: false */
/* global jQuery: false */
/* global google: false */
/* global lazyload_images: false */
/* global MarkerWithLabel: false */

/* global oMap: true */
/* global oCurrentLocationMarker: true */

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
    var oGeo2MarkersMapper = {};
    var oCurrentLocationMarker;
    var active_object_id = '';
    var loading = false;

    $(document).ready(function() {
        var $oList = $('body');
        if ($oList.length) {
            var oOptions = {
                zoom: 14,
                panControl: false,
                zoomControl: true,
                mapTypeControl: false,
                scaleControl: false,
                streetViewControl: false,
                overviewMapControl: false,

                center: new google.maps.LatLng(52.515306, 13.363863),

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
        var lat_min = 500, long_min = 500;
        var lat_max = -500, long_max = -500;
        var aPoints = [];

        var oMarkerImgDefault = new google.maps.MarkerImage(self.MARKER_DEFAULT_IMAGE_PATH || self.settings.STATIC_URL + 'site/img/marker_default.png', null, null, null, new google.maps.Size(25,35));
        var oMarkerImgSelected = new google.maps.MarkerImage(self.MARKER_SELECTED_IMAGE_PATH || self.settings.STATIC_URL + 'site/img/marker_selected.png', null, null, null, new google.maps.Size(25,35));

        var oActiveMarker = null;

        if (window.location.hash) {
            // get options object from hash
            var options = window.location.hash ? $.deparam.fragment(window.location.hash, true) : {};
            // apply options from hash
            active_object_id = '' + options.object_id;  // object_id converted to a string
        }

        function setMarkerLabel(oMarker, sHTML) {
            oMarker.labelContent = sHTML;
            oMarker.label.setContent();
        }
        $(self.aGeopositions).each(function(i, el) {
            // DEFINE IMAGE
            var nLat = el.latitude;
            var nLong = el.longitude;
            if (lat_max < nLat) {
                lat_max = nLat;
            }
            if (nLat < lat_min) {
                lat_min = nLat;
            }
            if (long_max < nLong) {
                long_max = nLong;
            }
            if (nLong < long_min) {
                long_min = nLong;
            }
            var oPoint = new google.maps.LatLng(nLat, nLong);

            var oMarker;
            if (oGeo2MarkersMapper[el.geo]) {
                // if marker for this geoposition already exists...
                oMarker = oGeo2MarkersMapper[el.geo];
                // add categories
                oMarker.categories += ' ' + el.categories;
                // add html_source
                oMarker.html_sources.push(el.html_src);
                // add marker
                oMarker.object_ids.push(el.object_id);
                // modify label
                setMarkerLabel(oMarker, '<span class="marker_label">' + oGeo2MarkersMapper[el.geo].html_sources.length + '</span>');
            } else {
                // if marker is new...
                oMarker = new MarkerWithLabel({
                    position: oPoint,
                    map: oMap,
                    icon: oMarkerImgDefault,
                    labelContent: '',
                    labelAnchor: new google.maps.Point(0, 40),
                    labelClass: "marker_label_wrapper",
                    labelInBackground: false
                });
                // define categories
                oMarker.categories = el.categories;
                // define html source
                oMarker.html_sources = [el.html_src];
                // define object_ids
                oMarker.object_ids = [el.object_id];
                // save to existing markers
                oGeo2MarkersMapper[el.geo] = oMarker;

                // attach click event
                google.maps.event.addListener(oMarker, 'click', function() {
                    if (loading) {
                        return;
                    }
                    loading = true;
                    if (oActiveMarker && oActiveMarker !== oMarker) {
                        oActiveMarker.setZIndex(oActiveMarker.old_z_index);
                        oActiveMarker.setIcon(oMarkerImgDefault);
                    }
                    oMarker.setIcon(oMarkerImgSelected);
                    oActiveMarker = oMarker;
                    oActiveMarker.old_z_index = oActiveMarker.getZIndex() || 5;
                    oActiveMarker.setZIndex(google.maps.Marker.MAX_ZINDEX + 1); // active marker always upper than others, but lower than current location

                    // active_object_id will be set if a list item is clicked
                    if (!active_object_id) {
                        // if the marker is clicked physically, active_object_id will be unset, so define it
                        active_object_id = oMarker.object_ids[0];
                    }
                    $.bbq.pushState({object_id: active_object_id});
                    $('#map-description').html('');
                    var loaded_count = 0;
                    $.each(oMarker.html_sources, function(j, src) {
                        $.get(src, function(data) {
                            loaded_count++;
                            $('#map-description').append(data);
                            if (loaded_count === oMarker.html_sources.length) {
                                // when all sources loaded, show the sidebar
                                $("body").removeClass("map-only");
                                $("#map-sidebar").removeClass("map-list map-filter").addClass("map-description");
                                setTimeout(lazyload_images, 500);
                                google.maps.event.trigger(oMap, "resize");
                                loading = false;
                            }
                        }, 'html');
                    });
                    // cleanup active_object_id
                    active_object_id = '';
                });
            }

            if (!oMarker.getZIndex()) {
                oMarker.setZIndex(5);
            }

            aMarkers.push(oMarker);
            aPoints.push(oPoint);

            if (el.object_id === active_object_id) {
                oActiveMarker = oMarker;
            }
        });

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position)  {
                    // var oImage = self.settings.STATIC_URL + 'site/img/marker_current.png';
                    var oImage = new google.maps.MarkerImage(self.settings.STATIC_URL + "site/img/marker_current.gif", null, null, null, new google.maps.Size(16,16));

                    oCurrentLocationMarker = new google.maps.Marker({
                        position: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
                        map: oMap,
                        icon: oImage,
                        optimized: false
                    });
                    oCurrentLocationMarker.setZIndex(google.maps.Marker.MAX_ZINDEX + 2); // always on top
                    // google.maps.event.addListener(oCurrentLocationMarker, 'click', function() {
                    //     $('#map-description').html("You are here!");
                    // });
                    $("#show-current-location").removeClass("hidden");
                },
                function(){
                    // alert('Unable to get location');
                },
                { enableHighAccuracy: true }
            );
        }
        if (oActiveMarker) {
            // CENTER CURRENT MARKER
            oMap.setCenter(oActiveMarker.getPosition());
            google.maps.event.trigger(oActiveMarker, 'click');
        } else if (document.location.search) {
            // FIT MAP
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
            oNEPoint.lat() - 0.005,
            oNEPoint.lng() - 0.005
        ));

        var oSWPoint = oBounds.getNorthEast();
        oBounds.extend(new google.maps.LatLng(
            oSWPoint.lat() + 0.005,
            oSWPoint.lng() + 0.005
        ));
        if (oMap) {
            oMap.fitBounds(oBounds);
        }
    }

    $(window).load(function() {
        setTimeout(function() {
            $('body').removeClass('no-transition');
        }, 100);
    });

    $(document).ready(function() {
        $('#container').find('.item a').click(function() {
            var $item = $(this).closest('.item');
            var sGeo = $item.data('geo');
            var oMarker = oGeo2MarkersMapper[sGeo];
            if (oMarker) {
                active_object_id = $item.data('object_id');
                google.maps.event.trigger(oMarker, 'click');
                oMap.panTo(oMarker.getPosition());
            }
            return false;
        });
        /*
            $(document).on("click", "#cancel-description", function() {
                $("#map-sidebar").removeClass("map-description").addClass("map-list");
                return false;
            });

            $(document).on("click", "#cancel-filter", function() {
                $("#map-sidebar").removeClass("map-filter").addClass("map-list");
                return false;
            });
        */
        $(document).on("click", "#cancel-description", function() {
            $("body").toggleClass( "map-only" );
            setTimeout(function() {
                google.maps.event.trigger(oMap, "resize");
            }, 500);
            return false;
        });

        $("#toggle-map-filter").click(function() {
            $("#map-sidebar").toggleClass("map-filter").removeClass("map-list");
            google.maps.event.trigger(oMap, "resize");
            return false;
        });

        $("#toggle-sidebar").click(function() {
            $("body").toggleClass("map-only");
            setTimeout(function() {
                google.maps.event.trigger(oMap, "resize");
            }, 500);
        });

        $("#map-sidebar").hammer().on('swiperight', function() {
            $("body").addClass("map-only");
            setTimeout(function() {
                google.maps.event.trigger(oMap, "resize");
            }, 500);
        });

        $("#show-current-location").click(function() {
            oMap.panTo(oCurrentLocationMarker.getPosition());
            return false;
        });

        var previous_page = document.referrer;
        $('#cancel-map').click(function() {
            if (!previous_page) {
                previous_page = "../";
            }
            location.href = previous_page;
            return false;
        });

        $('#map-description').bind('scrollstop', lazyload_images);
    });

}(jQuery));
