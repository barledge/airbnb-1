mapboxgl.accessToken = 'pk.eyJ1IjoibGFtdWNoYWNobyIsImEiOiJjajhvN3ZhbjQwMGNrMzNvMzc0ZDZmbmw5In0.oRLqqZFfNMz1k9WaL_P7FQ'

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v9',
  center: [parseFloat(currentRoom.latlng[1]), parseFloat(currentRoom.latlng[0])],
  zoom: 9
})
