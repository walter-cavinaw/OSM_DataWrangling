/**
 * Created by Walter on 4/20/2015.
 */
var map;
var mapMarkers;
var heatmap;
var markerCluster;
function init_goog_map() {
    mapMarkers = [];
     var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(49.264, -123.1207)
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    heatmap = plot_heatmap(map);
    map.setOptions({minZoom: 10, maxZoom: 17});
}

function plot_heatmap(map){
    var list_data = [];
    d3.json("chart_data/amenities.json", function(error,data) {
        list_data = data.map(function(a){
           if (a.hasOwnProperty('pos')){
           return new google.maps.LatLng(a.pos[0], a.pos[1]);}
        });
        console.log(list_data);
        var heatmap = new google.maps.visualization.HeatmapLayer({
            data: list_data,
            dissipating: false,
            radius: 0.002,
            maxIntensity: 1
         });
        heatmap.setMap(map);
    });
    return heatmap;
}