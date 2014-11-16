from flask import Flask, request, jsonify, Response
from flask.ext.restful import Resource, Api
import json
import helper

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        #Just say hello
        return {'status':200, 'message': "Hello! I'm a quick api to parse Backpage ad data"}

class Parse(Resource):
    #Parse a message and return analysis
    def post(self):
        # {'text':"Here's some text"}
        data = json.loads(request.data)
        return {'status':200, 'message': "Here's what you sent:"+data['text']}
        
class Location(Resource):
    #For a given location(state?) provide average price/age
    def get(self, location):
        return {'status':200, 'location':location, 'avg_prive':0, 'avg_age':0 }

class Add(Resource):
    #Add this ad to the dictionary
    def post(self):
        

class Heatmap(Resource):
    def post(self):
        import geopy
        from geopy.distance import VincentyDistance
        
        locs = helper.location_csv('data/latlong.csv')
        data = json.loads(request.data)
        rdata = []
        for d in data.data:
            if d['location'] in locs:
                rdata.append({'lat':locs[d['location']]['lat'],'long':locs[d['location']]['long']})
            else:
                #look it up and add to csv
                lkup = helper.loc_lookup(d['location']
                if lkup:
                    rdata.append({'lat':lkup['lat'],'long':lkup['long']})
                #Else disregard
                    
                
        origin = geopy.Point(lat1, lon1)
        destination = VincentyDistance(kilometers=d).destination(origin, b)

        lat2, lon2 = destination.latitude, destination.longitude
        #Post an array of locations, grab latlong for place, add variable distance (for nicer visual)
            
        
api.add_resource(Hello, '/')
api.add_resource(Parse, '/ad')
api.add_resource(Heatmap, '/visual/heatmap')

if __name__ == '__main__':
    app.run(debug=True)