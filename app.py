from flask import Flask,render_template,request,make_response,jsonify
import pymongo

from geopy.geocoders import Nominatim
import ssl
import certifi
import geopy.geocoders

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

class mongo_connection:
  conn = None

  def connect(self):
    client = pymongo.MongoClient("mongodb+srv://marcustest:<password>@cluster0.xh91t.mongodb.net/?retryWrites=true&w=majority")
    db = client.sample_restaurants
    self.conn = db["restaurant_regex"]

  def query(self, mql):
      cursor = self.conn.find(mql)  
      return cursor 

db = mongo_connection()
db.connect()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1.0/tasks/autoc2/restaurantfinder', methods=['GET'])
def getrestaurants(): 
    restname = request.args.get('restaurant')
    borough = request.args.get('borough')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    rad = request.args.get('radius')
    coord = request.args.get('coord')
    print(f'rad: {rad}')
    print(f'type(rad): {type(rad)}')
    print(f'restaurant: {str(restname)}')
    print(f'type(cord): {type(restname)}')

    print(restname,borough,state,zipcode)

    print(f'zip_or_addr: {zipcode}')

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(int(zipcode), timeout=None)
    lat=float(location.raw['lat'])
    lon=float(location.raw['lon']) 
    nearby_restaurants = [{'orig_lat':lat, 'orig_lon':lon}]

    print(lat,lon)   

    METERS_PER_MILE = 1609.34

    filters = { 'location': { '$nearSphere': { '$geometry': { 'type': "Point", 
                                     'coordinates': [ lon, lat ] }, 
                                    '$maxDistance': int(rad) * METERS_PER_MILE } },
                                    'name': {'$regex': restname, "$options" : "i"}}
    
    
    documents = db.query(filters)

    for document in documents:
        nearby_restaurants.append({
                       'restaurant_name':document['name'] ,
                       'lat':document['location']['coordinates'][1],
                       'lon':document['location']['coordinates'][0]
                })

        

    return jsonify(nearby_restaurants)



# { 'location': { '$nearSphere': { '$geometry': { 'type': "Point",'coordinates': [40.8283807,-73.9270844] },'$maxDistance': 5 * 1609.34 } } }

# {location: {$nearSphere: { $geometry: { type: "Point",coordinates: [40.8283807,-73.9270844] },$maxDistance:7609.34 } } }