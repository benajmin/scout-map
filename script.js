var map;
var heatmap;

$.getJSON("canada.json", function(data) {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 60, lng: -106},
    zoom: 4
  });

  var items = [];
  $.each( data, function( key, group ) {
    items.push(new google.maps.LatLng(parseFloat(group['Latitude']), parseFloat(group['Longitude'])));
  });

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: items,
    map: map
  })
 });

