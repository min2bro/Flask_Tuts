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

db = pymongo.MongoClient("mongodb+srv://marcustest:<password>@cluster0.xh91t.mongodb.net/?retryWrites=true&w=majority").sample_restaurants
print(db)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1.0/tasks/autoc2/restaurantfinder', methods=['GET'])
def getrestaurants(): 
    restname = request.args.get('restaurant')

    zipcode = request.args.get('zipcode')
    rad = request.args.get('radius')
    print(f'rad: {rad}')
    print(f'type(rad): {type(rad)}')
    print(f'restaurant: {str(restname)}')
    print(f'type(cord): {type(restname)}')


    print(f'zip_or_addr: {zipcode}')

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(int(zipcode), timeout=None)
    lat=float(location.raw['lat'])
    lon=float(location.raw['lon']) 
    nearby_restaurants = [{'orig_lat':lat, 'orig_lon':lon}]

    print(lat,lon)   

    METERS_PER_MILE = 1609.34

    # filters = { 'location': { '$nearSphere': { '$geometry': { 'type': "Point", 
    #                                  'coordinates': [ lon, lat ] }, 
    #                                 '$maxDistance': int(rad) * METERS_PER_MILE } },
    #                                 'name': {'$regex': restname, "$options" : "i"}}
    pipeline = [ { "$search": { "index": "restaurant_fts","compound":  { "must": { "text": { "query": restname, "path": "name"} } , "should": { "near": { "origin": {"type": "Point","coordinates": [lat, lon] }, "pivot": 500, "path": "location"     } } }} } ]    
    documents = db.restaurant_regex.aggregate(pipeline)
    print(documents)

    for document in documents:
        nearby_restaurants.append({
                       'restaurant_name':document['name'] ,
                       'lat':document['location']['coordinates'][1],
                       'lon':document['location']['coordinates'][0]
                })

        

    return jsonify(nearby_restaurants)



# { 'location': { '$nearSphere': { '$geometry': { 'type': "Point",'coordinates': [40.8283807,-73.9270844] },'$maxDistance': 5 * 1609.34 } } }

# {location: {$nearSphere: { $geometry: { type: "Point",coordinates: [40.8283807,-73.9270844] },$maxDistance:7609.34 } } }