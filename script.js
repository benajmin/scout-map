var map;
var heatmap;

function displayInfoWindow(infowindow, map, marker) {
  return function () {
    infowindow.open(map, marker);
  }
}

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
  var infowindows = []
  var contentstrings = []
  $.each( data, function( key, group ) {
    items.push(new google.maps.LatLng(parseFloat(group['Latitude']), parseFloat(group['Longitude'])));
    contentstrings.push('<div id="content">' +
      '<h4>' + group['Name'] + '</h4>' +
      'Meets ' + group['Meeting Day'] + 's at ' + group['Meeting Time'] + ' at ' + group['Meeting Location'] + '<br/>' +
      'Registration Fee: ' + group['Registration Fee'] + '<br/>' +
      (group['Summer Program']? 'Runs Summer Program <br/>' : '') +
      '</div>'
    );

    infowindows.push(new google.maps.InfoWindow({
      content: contentstrings[contentstrings.length-1]
    }));
    var marker = new google.maps.Marker({
      position: items[items.length - 1],
      map: map,
      title: group['Name'],
      icon: 'marker.png'
    });
    marker.addListener('click', displayInfoWindow(infowindows[infowindows.length-1], map, marker));
    markers.push(marker)
  });

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: items,
    map: hmap
  })
});

