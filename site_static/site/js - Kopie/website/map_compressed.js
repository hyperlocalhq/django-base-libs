(function($,undefined){self.GMapViewManager={oMap:null,aMarkers:[],sContextItemType:"",sSlug:"",sGMapImagePath:window.settings.STATIC_URL+"site/img/gmap/",oSelected:null,init:function(){var oSelf=self.GMapViewManager;
oSelf.initGMaps(document.getElementById("gmap_view"));
var aUrlBits=window.website.path.substr(1).split("/");
oSelf.sContextItemType=aUrlBits[0];
oSelf.sSlug=aUrlBits[aUrlBits.length-3];
$("#dyn_map").removeClass("hidden");
oSelf.markAllGeopositions()
},initGMaps:function(oElem){var oSelf=self.GMapViewManager;
var oOptions={zoom:15,center:new google.maps.LatLng(52.523781,13.411895),mapTypeId:google.maps.MapTypeId.ROADMAP,mapTypeControlOptions:{style:google.maps.MapTypeControlStyle.DROPDOWN_MENU},navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}};
oSelf.oMap=new google.maps.Map(oElem,oOptions)
},clearMarkers:function(){var oSelf=self.GMapViewManager;
while(oSelf.aMarkers.length>0){var oMarker=oSelf.aMarkers.pop();
oMarker.setMap(null);
oMarker=null
}},drawMarker:function(oPoint){var oSelf=self.GMapViewManager;
var oImage=new google.maps.MarkerImage(window.settings.STATIC_URL+"site/img/gmap/markers_1-10.png",new google.maps.Size(20,34),new google.maps.Point(0,340),new google.maps.Point(10,34));
var oShadow=new google.maps.MarkerImage(window.settings.STATIC_URL+"site/img/gmap/marker_shadow.png",new google.maps.Size(37,34),new google.maps.Point(0,0),new google.maps.Point(8,25));
var oMarker=new google.maps.Marker({position:oPoint,map:oSelf.oMap,shadow:oShadow,icon:oImage});
oSelf.aMarkers.push(oMarker)
},markGeoposition:function(sIndex){var oSelf=self.GMapViewManager;
var aPos=self.aGeopositions||[];
if(typeof(sIndex)!="string"&&typeof(sIndex)!="number"){sIndex=$(this).attr("href").split("#")[1].substr(8)
}var aGeo=aPos[parseInt(sIndex,10)];
iLat=aGeo[0];
iLong=aGeo[1];
if(oSelf.oSelected){oSelf.oSelected.removeClass("active")
}oSelf.clearMarkers();
var oPoint=new google.maps.LatLng(iLat,iLong);
oSelf.oMap.setCenter(oPoint,15);
oSelf.drawMarker(oPoint)
},markAllGeopositions:function(){var oSelf=self.GMapViewManager;
if(oSelf.oSelected){oSelf.oSelected.removeClass("active")
}oSelf.clearMarkers();
var aPos=self.aGeopositions||[];
var lat_min=long_min=500;
var lat_max=long_max=-500;
var aPoints=[];
for(iI=0,iLen=aPos.length;
iI<iLen;
iI++){iLat=aPos[iI][0];
iLong=aPos[iI][1];
if(lat_max<iLat){lat_max=iLat
}if(iLat<lat_min){lat_min=iLat
}if(long_max<iLong){long_max=iLong
}if(iLong<long_min){long_min=iLong
}var oPoint=new google.maps.LatLng(iLat,iLong);
oSelf.drawMarker(oPoint);
aPoints.push(oPoint)
}oSelf.fitMap(aPoints)
},fitMap:function(aPoints){var oSelf=self.GMapViewManager;
var oMap=oSelf.oMap;
var oBounds=new google.maps.LatLngBounds();
for(var i=0,iLen=aPoints.length;
i<iLen;
i++){oBounds.extend(aPoints[i])
}var oNEPoint=oBounds.getNorthEast();
oBounds.extend(new google.maps.LatLng(oNEPoint.lat()-0.005,oNEPoint.lng()-0.005));
var oSWPoint=oBounds.getNorthEast();
oBounds.extend(new google.maps.LatLng(oSWPoint.lat()+0.005,oSWPoint.lng()+0.005));
oMap.fitBounds(oBounds)
},destruct:function(){self.GMapViewManager=null
}};
$(document).ready(function(){self.GMapViewManager.init()
});
$(window).unload(function(){self.GMapViewManager.destruct()
})
}(jQuery));