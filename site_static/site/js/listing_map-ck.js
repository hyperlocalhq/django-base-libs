(function(e){e.fn.autoscroll=function(){e("html,body").animate({scrollLeft:this.offset().left,scrollTop:this.offset().top},500);return this}})(jQuery);var oMap;(function(e,t){function o(){n&&n.close();self.aGeopositions=[];for(var e=0,t=r.length;e<t;e++)r[e].setMap(null);r=[]}function u(){var t=self.aGeopositions||[],s=long_min=500,o=long_max=-500,u=[],a;for(i=0,iLen=t.length;i<iLen;i++){if(i<10){a=window.settings.STATIC_URL+"site/img/gmap/markers_1-10.png";iMarkerImgY=-34*i}else if(i<26){a=window.settings.STATIC_URL+"site/img/gmap/markers_11-26.png";iMarkerImgY=-34*(i-10)}else{a=window.settings.STATIC_URL+"site/img/gmap/markers_1-10.png";iMarkerImgY=-340}iLat=t[i].latitude;iLong=t[i].longitude;o<iLat&&(o=iLat);iLat<s&&(s=iLat);long_max<iLong&&(long_max=iLong);iLong<long_min&&(long_min=iLong);var l=new google.maps.LatLng(iLat,iLong),c=new google.maps.MarkerImage(a,new google.maps.Size(20,34),new google.maps.Point(0,-iMarkerImgY),new google.maps.Point(10,34)),h=new google.maps.MarkerImage(window.settings.STATIC_URL+"site/img/gmap/marker_shadow.png",new google.maps.Size(37,34),new google.maps.Point(0,0),new google.maps.Point(8,25)),p=new google.maps.Marker({position:l,map:oMap,shadow:h,icon:c});p.list_index=i;(function(e,t){google.maps.event.addListener(e,"click",function(){n=new StyledInfoWindow({position:e.getPosition(),map:oMap,content:t})})})(p,t[i].content);p.categories=t[i].categories;r.push(p);u.push(l);e(".marker-link:eq("+i+")").data("marker_obj",p).click(function(){oMap.setCenter(e(this).data("marker_obj").getPosition());google.maps.event.trigger(e(this).data("marker_obj"),"click");e("body").addClass("map_visible");setTimeout(function(){google.maps.event.trigger(oMap,"resize")},600);return!1})}document.location.search&&f(oMap,u)}function a(t,n){var s=n.filter;e(r).each(function(){var e=this,t=!0,n=s.length,r,o;for(i=0;i<n;i++){o=s[i].replace(/\./,"");r=new RegExp("\\b"+o+"\\b");if(!e.categories.match(r)){t=!1;break}}e.setVisible(t)})}function f(e,t){var n=new google.maps.LatLngBounds;for(var r=0,i=t.length;r<i;r++)n.extend(t[r]);var s=n.getNorthEast();n.extend(new google.maps.LatLng(s.lat()-.005,s.lng()-.005));var o=n.getNorthEast();n.extend(new google.maps.LatLng(o.lat()+.005,o.lng()+.005));e.fitBounds(n)}var n,r=[],s=null;e(document).ready(function(){var t=e("#container");if(t.length){var n={zoom:13,mapTypeControl:!1,zoomControl:!0,streetViewControl:!0,center:new google.maps.LatLng(52.515306,13.363863),mapTypeId:google.maps.MapTypeId.ROADMAP,mapTypeControlOptions:{style:google.maps.MapTypeControlStyle.DROPDOWN_MENU},navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}},r=document.getElementById("gmap");r&&(oMap=new google.maps.Map(r,n));t.bind("before_list_load",o).bind("after_list_load",u).bind("map_filter",a);location.hash?t.trigger("before_list_load"):t.trigger("after_list_load")}})})(jQuery);