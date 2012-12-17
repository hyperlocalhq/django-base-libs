/* An StyledInfoWindow is like an info window, but it displays
 * under the marker, opens quicker, and has flexible styling.
 * @param {Object} opts Passes configuration options.
 */function StyledInfoWindow(e){google.maps.OverlayView.call(this);this.latlng_=e.position;this.content_=e.content;this.map_=e.map;this.height_=102;this.width_=285;this.size_=new google.maps.Size(this.height_,this.width_);this.offsetVertical_=-this.height_;this.offsetHorizontal_=0;this.panned_=!1;this.setMap(this.map_);var t=this;google.maps.event.addListener(this.map_,"bounds_changed",function(){t.draw()})}StyledInfoWindow.instance=null;StyledInfoWindow.prototype=new google.maps.OverlayView;StyledInfoWindow.prototype.onRemove=function(){if(this.div_){this.div_.parentNode.removeChild(this.div_);this.div_=null}};StyledInfoWindow.prototype.onAdd=function(){this.createElement()};StyledInfoWindow.prototype.draw=function(){if(!this.getProjection())return;var e=this.getProjection().fromLatLngToDivPixel(this.latlng_),t=this.getProjection().fromLatLngToDivPixel(this.map_.getCenter()),n=new google.maps.Point(this.map_.getDiv().offsetWidth/2,this.map_.getDiv().offsetHeight/2),r=-t.x+n.x,i=-t.y+n.y;if(!e)return;var s=StyledInfoWindow.Align.ABOVE,o=0,u=0,a=0;this.width_=600;this.height_=0;image="";this.offsetX_=-(this.width_/2+5);this.offsetY_=-(this.height_+40);this.div_.style.width=this.width_+"px";this.div_.style.left=e.x+this.offsetX_+r+"px";this.div_.style.height=this.height_+"px";this.div_.style.top=e.y+this.offsetY_+i+"px";this.div_.style.background='url("'+window.settings.STATIC_URL+"site/img/gmap/"+image+'")';this.div_.style.display="block";this.wrapperDiv_.style.width=this.width_-a+"px";this.wrapperDiv_.style.height=this.height_+"px";this.wrapperDiv_.style.marginTop=o+"px";this.wrapperDiv_.style.marginLeft=u+"px";this.wrapperDiv_.style.overflow="visible";if(!this.panned_){this.panned_=!0;this.maybePanMap()}};StyledInfoWindow.prototype.createElement=function(){if(StyledInfoWindow.instance){var e=StyledInfoWindow.instance;e.close();e.onRemove();e.setMap(null);StyledInfoWindow.instance=null}var t=this.getPanes(),n=this.div_;if(!n){n=this.div_=document.createElement("div");n.style.border="0px none";n.style.position="absolute";n.style.overflow="visible";var r=this.wrapperDiv_=document.createElement("div");r.className="info_window";var i=document.createElement("div");typeof this.content_=="string"?i.innerHTML=this.content_:i.appendChild(this.content_);i.className="inner";var s=document.createElement("img");s.src=window.settings.STATIC_URL+"site/img/gmap/closebigger.gif";s.className="close";i.appendChild(s);function o(e){return function(){e.setMap(null)}}google.maps.event.addDomListener(s,"click",o(this));r.appendChild(i);r.className="location";n.appendChild(r);this.map_.getDiv().appendChild(n)}else if(n.parentNode!=t.floatPane){n.parentNode.removeChild(n);t.floatPane.appendChild(n)}StyledInfoWindow.instance=this};StyledInfoWindow.mouseFilter=function(e){e.returnValue="true";e.handled=!0};StyledInfoWindow.prototype.close=function(){this.setMap(null)};StyledInfoWindow.prototype.maybePanMap=function(){var e=this.map_,t=this.getProjection(),n=e.getBounds();if(!n)return;var r=this.width_,i=this.height_,s=this.offsetX_,o=this.offsetY_,u=t.fromLatLngToDivPixel(this.latlng_),a=new google.maps.Point(u.x+s+20,u.y+o+i),f=new google.maps.Point(u.x+s+r,u.y+o),l=t.fromDivPixelToLatLng(a),c=t.fromDivPixelToLatLng(f);(!e.getBounds().contains(c)||!e.getBounds().contains(l))&&e.panToBounds(new google.maps.LatLngBounds(l,c))};StyledInfoWindow.Align={ABOVE:0,LEFT:1,RIGHT:2,BELOW:3};StyledInfoWindow.prototype.getBestAlignment=function(){var e=StyledInfoWindow.Align.LEFT,t=0;for(var n in StyledInfoWindow.Align){var n=StyledInfoWindow.Align[n],r=this.getPanValue(n);if(r>t){t=r;e=n}}return e};StyledInfoWindow.prototype.getPanValue=function(e){var t=new google.maps.Size(this.map_.getDiv().offsetWidth,this.map_.getDiv().offsetHeight),n=this.map_.getBounds(),r;switch(e){case StyledInfoWindow.Align.ABOVE:r=new google.maps.LatLng(n.getNorthEast().lat(),this.latlng_.lng());break;case StyledInfoWindow.Align.BELOW:r=new google.maps.LatLng(n.getSouthWest().lat(),this.latlng_.lng());break;case StyledInfoWindow.Align.RIGHT:r=new google.maps.LatLng(this.latlng_.lat(),n.getNorthEast().lng());break;case StyledInfoWindow.Align.LEFT:r=new google.maps.LatLng(this.latlng_.lat(),n.getSouthWest().lng())}var i=StyledInfoWindow.distHaversine(this.latlng_.lat(),this.latlng_.lng(),r.lat(),r.lng());return i};StyledInfoWindow.toRad=function(e){return e*Math.PI/180};StyledInfoWindow.distHaversine=function(e,t,n,r){var i=6371,s=StyledInfoWindow.toRad(n-e),o=StyledInfoWindow.toRad(r-t);e=StyledInfoWindow.toRad(e),n=StyledInfoWindow.toRad(n);var u=Math.sin(s/2)*Math.sin(s/2)+Math.cos(e)*Math.cos(n)*Math.sin(o/2)*Math.sin(o/2),a=2*Math.atan2(Math.sqrt(u),Math.sqrt(1-u)),f=i*a;return f};