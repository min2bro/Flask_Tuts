from flask import Flask,render_template,request,make_response,jsonify
import pymongo

from geopy.geocoders import Nominatim
import ssl
import certifi
import geopy.geocoders
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

### Stores secret files for deployment on Heroku as seen here: https://github.com/MirelaI/flask_config_example. Please note that there are better ways to do this, but I wanted to make the tutorial accessible for largest audience.
app.config.from_json('config.json')

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


db = pymongo.MongoClient(app.config["ATLAS_URI"]).sample_restaurants

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/v1.0/tasks/autoc2/restaurantfinder', methods=['GET'])
def getrestaurants(): 
    restname = request.args.get('restaurant')

    zipcode = request.args.get('zipcode')
    rad = request.args.get('radius')

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(int(zipcode), timeout=None)
    lat=float(location.raw['lat'])
    lon=float(location.raw['lon']) 
    nearby_restaurants = [{'orig_lat':lat, 'orig_lon':lon}]

    METERS_PER_MILE = 1609.34

    pipeline = [
        { "$search": {
            "index": "restaurant_fts_sample",
            "compound":  {
                "must": {
                    "text": {
                        "query": restname,
                        "path": "name",
                        "fuzzy": {
                            "maxEdits":2
                        } } },
                "should": {
                    "near": {
                        "origin": {
                            "type": "Point",
                            "coordinates": [lat, lon]
                        },
                        "pivot": int(rad) * METERS_PER_MILE,
                        "path": "address.coord"     } } }} },
        { "$limit": 20}]

    documents = db.restaurants.aggregate(pipeline)

    for document in documents:
        nearby_restaurants.append({
                       'restaurant_name':document['name'] ,
                       'lat':document['address']['coord'][1],
                       'lon':document['address']['coord'][0]
                })

        

    return jsonify(nearby_restaurants)

@app.route('/api/v1.0/tasks/autoc2/restaurantfinder/autocomplete', methods=['GET'])
def suggest_restaurants(): 
    restname = request.args.get('restaurant')

    zipcode = request.args.get('zipcode')
    rad = request.args.get('radius')

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(int(zipcode), timeout=None)
    lat=float(location.raw['lat'])
    lon=float(location.raw['lon']) 
    nearby_restaurants = [{'orig_lat':lat, 'orig_lon':lon}]

    METERS_PER_MILE = 1609.34

    pipeline = [ { "$search": {
                        "index": "rest_name_autocomplete_sample",
                        "compound":  { 
                            "must": { 
                                    "autocomplete": {
                                        "query": restname,
                                        "path": "name",
                                        "tokenOrder": "any"
                                        }
                                    }
                        }
                    }
                },
                {"$limit": 20}]
    documents = db.restaurants.aggregate(pipeline)

    for document in documents:
        nearby_restaurants.append({
                       'restaurant_name':document['name'] ,
                       'lat':document['address']['coord'][1],
                       'lon':document['address']['coord'][0]
                })

        

    return jsonify(nearby_restaurants)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9763,debug=True)