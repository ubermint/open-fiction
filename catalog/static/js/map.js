var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat(coords.split(", ")),
    zoom: 17
  })
});


map.on('postcompose',function(e){
    document.querySelector('canvas').style.filter="sepia(30%) grayscale(50%) ";
  });