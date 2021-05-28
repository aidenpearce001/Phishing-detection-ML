/*
Template Name: Niche
Author: UXLiner
*/
$(function() {
    "use strict";

//Simple Basic Map
	var map;
    $(document).ready(function(){
      map = new GMaps({
        el: '#simplemap',
        lat: -12.043333,
        lng: -77.028333,
        zoomControl : true,
        zoomControlOpt: {
            style : 'SMALL',
            position: 'TOP_LEFT'
        },
        panControl : false,
        streetViewControl : false,
        mapTypeControl: false,
        overviewMapControl: false
      });
    });
	
//Marker
var map;
    $(document).ready(function(){
      map = new GMaps({
        el: '#mapmarker',
        lat: -12.043333,
        lng: -77.028333
      });
      map.addMarker({
        lat: -12.043333,
        lng: -77.03,
        title: 'Lima',
        details: {
          database_id: 42,
          author: 'HPNeo'
        },
        click: function(e){
          if(console.log)
            console.log(e);
          alert('You clicked in this marker');
        },
        mouseover: function(e){
          if(console.log)
            console.log(e);
        }
      });
      map.addMarker({
        lat: -12.042,
        lng: -77.028333,
        title: 'Marker with InfoWindow',
        infoWindow: {
          content: '<p>HTML Content</p>'
        }
      });
    });
	
//OverlayLayer
var map;
    $(document).ready(function(){
      map = new GMaps({
        el: '#overlaylayer',
        lat: -12.043333,
        lng: -77.028333
      });
      map.drawOverlay({
        lat: map.getCenter().lat(),
        lng: map.getCenter().lng(),
        layer: 'overlayLayer',
        content: '<div class="overlay">Lima<div class="overlay_arrow above"></div></div>',
        verticalAlign: 'top',
        horizontalAlign: 'center'
      });
    });	
//OverlayLayer
$(document).ready(function(){
      var path = [
        [-12.040397656836609,-77.03373871559225],
        [-12.040248585302038,-77.03993927003302],
        [-12.050047116528843,-77.02448169303511],
        [-12.044804866577001,-77.02154422636042],
        [-12.040397656836609,-77.03373871559225]
      ];
      var url = GMaps.staticMapURL({
        lat: -12.043333,
        lng: -77.028333,
        polyline: {
          path: path,
          strokeColor: '#131540',
          strokeOpacity: 0.6,
          strokeWeight: 6
        }
      });
      $('<img/>').attr('src', url).appendTo('#polyline');
    });
	
//Styled	
$(function () {
          var map = new GMaps({
          el: "#styled",
          lat: 41.895465,
          lng: 12.482324,
          zoom: 5, 
          zoomControl : true,
          zoomControlOpt: {
            style : "SMALL",
            position: "TOP_LEFT"
          },
          panControl : true,
          streetViewControl : false,
          mapTypeControl: false,
          overviewMapControl: false
        });
        
        var styles = [
            {
              stylers: [
                { hue: "#00ffe6" },
                { saturation: -20 }
              ]
            }, {
                featureType: "road",
                elementType: "geometry",
                stylers: [
                    { lightness: 100 },
                    { visibility: "simplified" }
              ]
            }, {
                featureType: "road",
                elementType: "labels",
                stylers: [
                    { visibility: "off" }
              ]
            }
        ];
        
        map.addStyle({
            styledMapName:"Styled Map",
            styles: styles,
            mapTypeId: "map_style"  
        });
        
        map.setStyle("map_style");
      });
})(jQuery);