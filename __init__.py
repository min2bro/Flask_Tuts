from flask import Flask,render_template,request,make_response,jsonify
from geopy.geocoders import Nominatim
import pymongo

class mongo_connection:
  conn = None

  def connect(self):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["flask_tutorial"]
    self.conn = mydb["restaurants"]

  def query(self, sql):
      cursor = self.conn.find(sql)  
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
    city = request.args.get('city')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    rad = request.args.get('radius')
    print(rad)
    print(type(rad))

    print(restname,city,state,zipcode)

    zip_or_addr = city +' ' +state +' ' +zipcode

    print(f'zip_or_addr: {zip_or_addr}')

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(zip_or_addr)
    lat=float(location.raw['lat'])
    lon=float(location.raw['lon']) 
    nearby_restaurants = [{'orig_lat':lat,'orig_lon':lon}]

    print(lat,lon)   

    METERS_PER_MILE = 1609.34

    filters = { 'location': { '$nearSphere': { '$geometry': { 'type': "Point", 
                                     'coordinates': [ lon, lat ] }, 
                                    '$maxDistance': int(rad) * METERS_PER_MILE } },
     'name': {'$regex': restname, "$options" : "i"} }
    
    cursor = db.query(filters)
    

    for cur in cursor:
        nearby_restaurants.append({
                       'restaurant_name':cur['name'] ,
                       'lat':cur['location']['coordinates'][1],
                       'lon':cur['location']['coordinates'][0]
                })

        

    return jsonify(nearby_restaurants)


if __name__ == "__main__":
   app.run(host='0.0.0.0',port=9763,debug=True)
