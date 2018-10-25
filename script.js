var map;
var heatmap;

$.getJSON("canada.json", function(data) {
  hmap = new google.maps.Map(document.getElementById('heatmap'), {
    center: {lat: 60, lng: -106},
    zoom: 4
  });
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 60, lng: -106},
    zoom: 4
  });

  var items = [];
  var markers = []
  $.each( data, function( key, group ) {
    items.push(new google.maps.LatLng(parseFloat(group['Latitude']), parseFloat(group['Longitude'])));
    markers.push(new google.maps.Marker({
      position: items[items.length - 1],
      map: map,
      title: group['Name']}));
  });

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: items,
    map: hmap
  })
 });

