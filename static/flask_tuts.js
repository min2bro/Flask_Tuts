var markerarr = new Array();

let loadoriginUri="data:image/png;base64,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";

let markerShadow = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAYCAYAAABKtPtEAAAACXBIWXMAAAsTAAALEwEAmpwYAAABOWlDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjarZGxSsNQFIa/G0XFoVYI4uBwJ1FQbNXBjElbiiBYq0OSrUlDldIk3NyqfQhHtw4u7j6Bk6PgoPgEvoHi1MEhSHASwW/6zs/hcOAHo2LXnYZRhkGsVbvpSNfz5ewTM0wBQCfMUrvVOgCIkzjiJwI+XxEAz5t23WnwN+bDVGlgAmx3oywEUQH6FzrVIMaAGfRTDeIOMNVJuwbiASj1cn8BSkHub0BJuZ4P4gMwe67ngzEHmEHuK4Cpo0sNUEvSkTrrnWpZtSxL2t0kiOTxKNPRIJP7cZioNFEdHXWB/D8AFvPFdtORa1XL2lvnn3E9X+b2foQAxNJjkRWEQ3X+3YWx8/tc3Bgvw+EtTE+KbPcKbjZg4brIVqtQ3oL78RfCs0/+HAmzJwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6AAAUggAARVYAAA6lwAAF2/XWh+QAAABnElEQVR42uRY0Y6EIAxsOe7/f3i197Ikk9lSqIsXjSakirvITIdSqmYmT74qPqjqqnH1hLku8RQ7vJ4AUE9ylg5IsK8VkACtyfe6wOMG49gqtdQDoLP2CAnWeY5sTyF2lAAP0KiJc/8tAQiS73tNJogJCWAwxbGFwBeHKEmQYQOPI7id+nboQzskoU6CLyLyQ7YQESWpiJH3I4/vBLy1DazMkBApQAFwa5WePSKipTEiIfK853EE3trr/Q2PhHQMQO9XEfl9W48IDUhYSQB6n4G/aCwvLoQEeAEPCeiREKmAl8FsDIjkz55/0RaJv1OQ/8cyqBOJjHbUgHaGgCgQWkIFO4HD/200h2EiVeThV+1IUR05ouz4/RWWwEbboc0kRLUDnj+4EYjWf8UgiGSYQ+b0LmCwzjbobx++8jbIakinwubsoej1OyRC0XKYigEeCQUi7R1S4VD+IwUgCS0G7Dc5DPVOjZKNAdo5XV3xONwDfPg4LMH52ksq/qMgMprX8oJIpspik6Wrs+qCp5fEMhO5bFH0I+9/eln8bwDFO0IimD64UgAAAABJRU5ErkJggg=="

// Round marker template - SVG -initial
let roundSVG ="<svg version='1.1' id='Layer_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' width='40px' height='50px' viewBox='0 0 64 80' enable-background='new 0 0 64 80' xml:space='preserve'> <g> <path fill='%23563D7D' d='M64,32C64,14.327,49.673,0,32,0C14.327,0,0,14.327,0,32c0,14.243,9.309,26.308,22.172,30.456L31.942,80 l9.539-17.429C54.524,58.531,64,46.372,64,32z'/> </g> <g> <defs> <circle id='Clip' cx='32' cy='32' r='28'/> </defs> <clipPath id='ClipPath'> <use xlink:href='%23Clip' overflow='visible'/> </clipPath> <image overflow='visible' clip-path='url(%23ClipPath)' width='64' height='64' id='Icon' xlink:href='AVATAR_URI_HERE' > </image> </g> </svg>"

function makeMarkerUri(imageUri){
  let svg = roundSVG;
  return "data:image/svg+xml;utf-8," + svg.replace("AVATAR_URI_HERE", imageUri);
}

var markerIcon = L.Icon.extend({
    options: {
        shadowUrl: markerShadow,
        iconSize: [32, 40],
        iconAnchor: [16, 40],
        shadowSize: [32, 12],
        shadowAnchor: [16, 6],
        popupAnchor: [0, -35],
    }
});

var loadoriginIcon = new markerIcon({iconUrl: makeMarkerUri( loadoriginUri )})    

function getrestaurants() {
  var restname = document.getElementById("restaurant").value;
  var zipcode = document.getElementById("zipcode").value; 
  var radius = document.getElementById("radius").value;        
  
    
  $.ajax({
    url: '/api/v1.0/tasks/autoc2/restaurantfinder?restaurant='+restname+'&zipcode='+zipcode+'&radius='+radius,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      UpdateMap(data)    
    }

  });
}

// hacked together autocomplete implementation

(function($){
  $(function(){
    let zipcode = '10451',
            radius='10';
    $("#restaurant").autocomplete({
      source: async function(request, response){
        let data = await fetch(`http://localhost:5000/api/v1.0/tasks/autoc2/restaurantfinder/autocomplete?restaurant=${request.term}&zipcode=${zipcode}&radius=${radius}`)
        .then(results => results.json())
        .then(results => results.map(result => {
          return { label: result.restaurant_name, value: result.restaurant_name, lat: result.lat, lon: result.lon}
        }));
        console.log(data);
        // remove the undefined element of the response array so that it doesn't show in up in autocomplete
        response(data);
      },
      minlength: 2,
      select: (event, ui) => {

          console.log(ui.item);
          getrestaurants(ui.item.value);
      }
    });
  })
})(jQuery)


function UpdateMap(data){
  map.setView([data[0]['orig_lat'],data[0]['orig_lon']], 10);
  jQuery("#restaurant-list").empty();

  for (m=1;m<data.length;m++){
  marker = new L.marker([data[m]['lat'],data[m]['lon']], {
          icon: loadoriginIcon,
          riseOnHover: true,
          draggable: false,
          autoPan: true,
         })
          .addTo(map)
          .bindPopup(data[m]['restaurant_name'])
          markerarr.push(marker);
          var node = document.createElement("li");
              node.classList.add("list-group-item");
          node.textContent = data[m]['restaurant_name'];
          document.getElementById("restaurant-list").appendChild(node);
        }
  console.log(data);
}

function UpdateMapAutocomplete(data){
  var lon = "-73.90",
    lat = "40.76";
  map.setView([lat,lon], 10);
  jQuery("#restaurant-list").empty();
  for (m=1;m<data.length;m++){
  marker = new L.marker([lat,lon], {
          icon: loadoriginIcon,
          riseOnHover: true,
          draggable: false,
          autoPan: true,
         })
          .addTo(map)
          .bindPopup(data[m]['restaurant_name'])
          markerarr.push(marker);

          var node = document.createElement("li");
              node.classList.add("list-group-item");
          node.textContent = data[m]['restaurant_name'];
          document.getElementById("restaurant-list").appendChild(node);
        }
  console.log(data);
}




/*Clear all Markers and Polylines on the map*/
function clearMap() {
    // TODO: remove previous search results
/*Remove markers*/
for(i=0;i<markerarr.length;i++) {
    map.removeLayer(markerarr[i]);
    }

/*Remove Polylines*/
for(i in map._layers) {
        if(map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }


}

window.onbeforeunload = function() {
  sessionStorage.removeItem('access_token');
  return '';
};
