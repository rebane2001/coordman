if (!("userdata" in window))
  alert("Userdata corrupted or not found, please consult console logs and the README!")

let openSidebar = () => document.getElementById("sidebar").style.width = "350px";
let closeSidebar = () => document.getElementById("sidebar").style.width = "0";

let attribution = '<a href="https://github.com/rebane2001/coordman">Coordman</a> by Rebane';
let tileSize = 512;

// Layers for different dimensions
let tileLayers = {
"nether": L.tileLayer(
  'tiles/{DIM}/{z}/{x},{y}.png', {
    attribution,
    tileSize,
    maxZoom: 0,
    minZoom: -16,
    DIM: "DIM-1"
  }),

"netherbg": L.tileLayer(
  'tiles/{DIM}/{z}/{x},{y}.png', {
    attribution,
    tileSize,
    maxZoom: 0,
    minZoom: -16,
    zoomOffset: 3,
    DIM: "DIM-1"
  }),

"overworld": L.tileLayer(
  'tiles/{DIM}/{z}/{x},{y}.png', {
    attribution,
    tileSize,
    maxZoom: 0,
    minZoom: -16,
    DIM: "DIM0"
  }),


"end": L.tileLayer(
  'tiles/{DIM}/{z}/{x},{y}.png', {
    attribution,
    tileSize,
    maxZoom: 0,
    minZoom: -16,
    DIM: "DIM1"
  })
};

let layers = {
    "Overworld+Nether": L.layerGroup([tileLayers['netherbg'],tileLayers['overworld']]),
    "Overworld": tileLayers['overworld'],
    "Nether": tileLayers['nether'],
    "The End": tileLayers['end']
};

// Guide overlays
let worldBorder = L.polyline([
    [-30000000, -30000000],
    [-30000000, 30000000],
    [30000000, 30000000],
    [30000000, -30000000],
    [-30000000, -30000000]
], {color: 'red'});

let mainHighways = L.polyline([
    [0, 0],
    [-30000000, 0],
    [0, 0],
    [30000000, 0],
    [0, 0],
    [0, -30000000],
    [0, 0],
    [0, 30000000],
    [0, 0]
], {color: 'LimeGreen'});

let diagHighways = L.polyline([
    [0, 0],
    [-30000000, -30000000],
    [0, 0],
    [30000000, -30000000],
    [0, 0],
    [-30000000, 30000000],
    [0, 0],
    [30000000, 30000000],
    [0, 0]
], {color: 'MediumSpringGreen'});

let disabledLayer = L.tileLayer("",{minZoom: 99});
let waypoints = {
    "- Guides -": disabledLayer,
    "Worldborder": worldBorder,
    "Main Highways": mainHighways,
    "Diag. Highways": diagHighways,
    "- <a href=\"#\" onClick=\"openSidebar()\">Waypoints</a> -": disabledLayer,
};

let defaultLayers = [tileLayers['overworld'], worldBorder];

let sidebar = document.getElementById("sidebar");

// Load icons/locations from userdata
for (const group of window.userdata.groups){
  let groupItems = [];
  sidebar.innerHTML += `<h3>${group.name}</h3>`
  for (const marker of group.markers){
    let icon = L.icon({
      iconUrl: `icons/${marker.icon}.png`,
      shadowUrl: 'icons/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      tooltipAnchor: [16, -28],
      shadowSize: [41, 41]
    });
    // Leaflet maps use a weird coordinate system, so this is fine
    let newMarker = L.marker([-marker.coords[1], marker.coords[0]], {icon});
    let markerData = (typeof marker.data == "string") ? marker.data : marker.data.join("<br>\n");
    newMarker.bindPopup(`<h3>${marker.name}</h3>${markerData}`);
    groupItems.push(newMarker);
    console.log(newMarker.getLatLng());
    sidebar.innerHTML += `${marker.name} (<a href="#" onClick="map.setView([${-marker.coords[1]},${marker.coords[0]}],0)">${marker.coords}</a>)<br>`;
  }
  waypoints[group.name] = L.layerGroup(groupItems);
  if (group.default)
    defaultLayers.push(waypoints[group.name]);
}

// Create the map
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -16,
    layers: defaultLayers
}).setView([0,0], 0);

L.control.layers(layers, waypoints).addTo(map);

// Set coord overlay on the bottom
map.on('mousemove', function(ev) {
    let coords = [Math.round(ev.latlng.lng),Math.round(-ev.latlng.lat)];
    document.getElementById("coordstext").innerText = "Coords: " + coords;
});