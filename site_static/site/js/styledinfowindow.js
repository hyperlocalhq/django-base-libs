/* An StyledInfoWindow is like an info window, but it displays
 * under the marker, opens quicker, and has flexible styling.
 * @param {Object} opts Passes configuration options.
 */
function StyledInfoWindow(opts) {
    google.maps.OverlayView.call(this);
    this.latlng_ = opts.position;
    this.content_ = opts.content;
    this.map_ = opts.map;
    this.height_ = 102;
    this.width_ = 285;
    this.size_ = new google.maps.Size(this.height_, this.width_);
    this.offsetVertical_ = -this.height_;
    this.offsetHorizontal_ = 0;
    this.panned_ = false;
    this.setMap(this.map_);

    // We need to listen to bounds_changed event so that we can redraw
    // absolute position every time the map moves.
    // This is only needed because we append to body instead of map panes.
    var me = this;
    google.maps.event.addListener(this.map_, 'bounds_changed', function() {
        me.draw();
    });
}
StyledInfoWindow.instance = null;

/**
 * StyledInfoWindow extends GOverlay class from the Google Maps API
 */
StyledInfoWindow.prototype = new google.maps.OverlayView();

/**
 * Creates the DIV representing this StyledInfoWindow
 */
StyledInfoWindow.prototype.onRemove = function() {
    if (this.div_) {
        this.div_.parentNode.removeChild(this.div_);
        this.div_ = null;
    }
};

/**
 * Called when the overlay is first added to the map.
 */
StyledInfoWindow.prototype.onAdd = function() {
    // Creates the element if it doesn't exist already.
    this.createElement();
};

/**
 * Redraw based on the current projection and zoom level.
 */
StyledInfoWindow.prototype.draw = function() {
    // Since we use bounds changed listener, projection is sometimes null
    if (!this.getProjection()) {
        return;
    }

    // This gives us the position in the tiles div.
    var pixPosition = this.getProjection().fromLatLngToDivPixel(this.latlng_);
    var centerPosition = this.getProjection().fromLatLngToDivPixel(this.map_.getCenter());
    var centerPositionReal = new google.maps.Point(this.map_.getDiv().offsetWidth/2, this.map_.getDiv().offsetHeight/2);
    // Figure out difference between map div and tiles div, so that we can
    // calculate position in map div
    var centerOffsetX = -centerPosition.x + centerPositionReal.x;
    var centerOffsetY = -centerPosition.y + centerPositionReal.y;

    if (!pixPosition) return;
    var alignment = StyledInfoWindow.Align.ABOVE //this.getBestAlignment();
    var paddingTop = 0;
    var paddingLeft = 0;
    var widthLess = 0;
    
    this.width_ = 600;
    this.height_ = 0;
    image = '';
    this.offsetX_ = -(this.width_ / 2 + 5);
    this.offsetY_ = -(this.height_ + 40);
            
    // Now position our DIV based on the DIV coordinates of our bounds
    this.div_.style.width = this.width_ + 'px';
    this.div_.style.left = (pixPosition.x + this.offsetX_) + centerOffsetX + 'px';
    this.div_.style.height = this.height_ + 'px';
    this.div_.style.top = (pixPosition.y + this.offsetY_) + centerOffsetY + 'px';
    //this.div_.style.paddingTop = paddingTop + 'px';
    //this.div_.style.paddingLeft = paddingLeft + 'px';
    this.div_.style.background = 'url("' + window.settings.STATIC_URL + 'site/img/gmap/' + image + '")';
    this.div_.style.display = 'block';
    
    this.wrapperDiv_.style.width = (this.width_- widthLess) + 'px';
    this.wrapperDiv_.style.height = this.height_ + 'px';
    this.wrapperDiv_.style.marginTop = paddingTop + 'px';
    this.wrapperDiv_.style.marginLeft = paddingLeft + 'px';
    this.wrapperDiv_.style.overflow = 'visible';
    if (!this.panned_) {
        this.panned_ = true;
        this.maybePanMap();
    }
};

/**
 * Creates the DIV representing this StyledInfoWindow in the floatPane.  If the panes
 * object, retrieved by calling getPanes, is null, remove the element from the
 * DOM.  If the div exists, but its parent is not the floatPane, move the div
 * to the new pane.
 * Called from within draw.  Alternatively, this can be called specifically on
 * a panes_changed event.
 */
StyledInfoWindow.prototype.createElement = function() {
    if (StyledInfoWindow.instance) {
        var previous = StyledInfoWindow.instance;
        previous.close();
        previous.onRemove();
        previous.setMap(null);
        StyledInfoWindow.instance = null;
    }    
    var panes = this.getPanes();
    var div = this.div_;
    if (!div) {
        // This does not handle changing panes.  You can set the map to be null and
        // then reset the map to move the div.
        div = this.div_ = document.createElement('div');
        div.style.border = '0px none';
        div.style.position = 'absolute';
        div.style.overflow = 'visible';
        var wrapperDiv = this.wrapperDiv_ = document.createElement('div');
        wrapperDiv.className="info_window";
        var contentDiv = document.createElement('div');
        if (typeof this.content_ == 'string') {
            contentDiv.innerHTML = this.content_;
        } else {
            contentDiv.appendChild(this.content_);
        }
        contentDiv.className="wrapper";
        var closeImg = document.createElement('img');
        closeImg.src = window.settings.STATIC_URL + 'site/img/gmap/closebigger.gif';
        closeImg.className="close";
        contentDiv.appendChild(closeImg);

        function removeStyledInfoWindow(ib) {
            return function() {
                ib.setMap(null);
            };
        }

        google.maps.event.addDomListener(closeImg, 'click', removeStyledInfoWindow(this));
        
        wrapperDiv.appendChild(contentDiv);
        wrapperDiv.className="location";
        div.appendChild(wrapperDiv);
        // Append to body, to avoid bug with Webkit browsers
        // attempting CSS transforms on IFRAME or SWF objects
        // and rendering badly.
        this.map_.getDiv().appendChild(div);
        //document.body.appendChild(div);
    } else if (div.parentNode != panes.floatPane) {
        // The panes have changed.  Move the div.
        div.parentNode.removeChild(div);
        panes.floatPane.appendChild(div);
    } else {
        // The panes have not changed, so no need to create or move the div.
    }
    StyledInfoWindow.instance = this;
};

StyledInfoWindow.mouseFilter = function(e) {
    e.returnValue = 'true';
    e['handled'] = true;
}

/**
 * Closes infowindow
 */
StyledInfoWindow.prototype.close = function() {
    this.setMap(null);
};

/**
 * Pan the map to fit the StyledInfoWindow,
 * if its top or bottom corners aren't visible.
 */
StyledInfoWindow.prototype.maybePanMap = function() {
    // if we go beyond map, pan map
    var map = this.map_;
    var projection = this.getProjection();
    var bounds = map.getBounds();
    if (!bounds) return;
    
    // The dimension of the infowindow
    var iwWidth = this.width_;
    var iwHeight = this.height_;
    
    // The offset position of the infowindow
    var iwOffsetX = this.offsetX_;
    var iwOffsetY = this.offsetY_;
    
    var anchorPixel = projection.fromLatLngToDivPixel(this.latlng_);
    var bl = new google.maps.Point(
        anchorPixel.x + iwOffsetX + 20,
        anchorPixel.y + iwOffsetY + iwHeight
    );
    var tr = new google.maps.Point(
        anchorPixel.x + iwOffsetX + iwWidth,
        anchorPixel.y + iwOffsetY
    );
    var sw = projection.fromDivPixelToLatLng(bl);
    var ne = projection.fromDivPixelToLatLng(tr);
    
    // The bounds of the infowindow
    if (!map.getBounds().contains(ne) || !map.getBounds().contains(sw)) {
        map.panToBounds(new google.maps.LatLngBounds(sw, ne));
    }
};

/**
 * @enum {number}
 */
StyledInfoWindow.Align = {
    ABOVE: 0,
    LEFT: 1,
    RIGHT: 2,
    BELOW: 3
};

/**
 * Finds best alignment for infowindow.
 * @return {number} Alignment.
 */
StyledInfoWindow.prototype.getBestAlignment = function() {
    var bestAlignment = StyledInfoWindow.Align.LEFT;
    var minPan = 0;

    for (var alignment in StyledInfoWindow.Align) {
        var alignment = StyledInfoWindow.Align[alignment];
        var panValue = this.getPanValue(alignment);
        if (panValue > minPan) {
            minPan = panValue;
            bestAlignment = alignment;
        }
    }

    return bestAlignment;
};

/**
 * Calculates distance of corner for each alignment.
 * @param {number} alignment An alignment constant.
 * @return {number} Distance for that alignment.
 */
StyledInfoWindow.prototype.getPanValue = function(alignment) {
    var mapSize = new google.maps.Size(this.map_.getDiv().offsetWidth,
        this.map_.getDiv().offsetHeight);
    var bounds = this.map_.getBounds();
    var sideLatLng;
    switch (alignment) {
        case StyledInfoWindow.Align.ABOVE:
            sideLatLng = new google.maps.LatLng(
                bounds.getNorthEast().lat(),
                this.latlng_.lng()
            );
            break;
        case StyledInfoWindow.Align.BELOW:
            sideLatLng = new google.maps.LatLng(
                bounds.getSouthWest().lat(),
                this.latlng_.lng()
            );
            break;
        case StyledInfoWindow.Align.RIGHT:
            sideLatLng = new google.maps.LatLng(
                this.latlng_.lat(),
                bounds.getNorthEast().lng()
            );
            break;
        case StyledInfoWindow.Align.LEFT:
            sideLatLng = new google.maps.LatLng(
                this.latlng_.lat(),
                bounds.getSouthWest().lng()
            );
            break;
    }
    var dist = StyledInfoWindow.distHaversine(
        this.latlng_.lat(),
        this.latlng_.lng(),
        sideLatLng.lat(),
        sideLatLng.lng()
    );
    return dist;
};


/**
 * Converts degrees to radians.
 * @param {number} num Angle in degrees.
 * @return {number} Angle in radians.
 */
StyledInfoWindow.toRad = function(num) {
    return num * Math.PI / 180;
}

/**
 * Calculates distance between two coordinates.
 * @param {number} lat1 Latitude of first coord.
 * @param {number} lon1 Longitude of second coord.
 * @param {number} lat2 Latitude of second coord.
 * @param {number} lon2 Longitude of second coord.
 * @return {number} The distance.
 */
StyledInfoWindow.distHaversine = function(lat1, lon1, lat2, lon2) {
    var R = 6371; // earth's mean radius in km
    var dLat = StyledInfoWindow.toRad(lat2 - lat1);
    var dLon = StyledInfoWindow.toRad(lon2 - lon1);
    lat1 = StyledInfoWindow.toRad(lat1), lat2 = StyledInfoWindow.toRad(lat2);

    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1) * Math.cos(lat2) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;
    return d;
}
