var sGMapImagePath = window.settings.STATIC_URL + "site/img/gmap/";
var oMap, oLargeMapControl, oMapTypeControl;
var oGeocorrector;
if (window.opener) {
    opener.oGMapWindow = window;
} else {
    parent.oGMapWindow = window;
}

function initGMaps() {
    var oOptions = {
        zoom: 15,
        center: new google.maps.LatLng(52.523781, 13.411895),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        navigationControlOptions: {
            style: google.maps.NavigationControlStyle.SMALL
        }
    };
    oMap = new google.maps.Map(document.body, oOptions);
}

function destructGMaps() {
}

function setMarkerDraggable(oMarker, fCallback, oParams) {
    oMarker.setDraggable(true);
    google.maps.event.addListener(oMarker, "dragend", function() {
        var oPoint = oMarker.getPosition(); 
        fCallback(oPoint.lat(), oPoint.lng(), oParams);
    });
}

function getGeoposition() {
    var oGeocoder = new google.maps.Geocoder();
    var sAddress = retrieveFullAddress();
    oGeocoder.geocode(
        {address:sAddress},
        function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_latitude").value = results.geometry.location.lat();
                document.getElementById("id_longitude").value = results.geometry.location.lng();
            }
        }
    );
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

function locateGeoposition() {
    var sAddress = retrieveFullAddress();
    oPoint = new google.maps.LatLng(
        document.getElementById("id_latitude").value, 
        document.getElementById("id_longitude").value
    );
    oMap.setCenter(oPoint, 14);
    var oMarker = new google.maps.Marker({
      position: oPoint, 
      map: oMap,
      title: sAddress
    });   
}
window.onload = initGMaps;
window.onunload = destructGMaps;
