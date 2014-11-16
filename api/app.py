from flask import Flask, request, jsonify, Response
from flask.ext.restful import Resource, Api
from flask.ext.cors import CORS, cross_origin
import json, random
import helper

app = Flask(__name__)
app.config['CORS_HEADERS'] = "Content-Type"
api = Api(app)
cors = CORS(app)


class Hello(Resource):
    def get(self):
        #Just say hello
        return {'status':200, 'message': "Hello! I'm a quick api to parse Backpage ad data"}

class Parse(Resource):
    #Parse a message and return analysis
    def post(self):
        # {'text':"Here's some text"}
        data = json.loads(request.data)
        race = helper.race(data['title']+' '+data['text'])
        return {'status':200, 'title':data['title'], 'message': data['text'], 'race':race, 'estimated_prices':helper.price(data['title']+' '+ data['text']), 'estimated_age':helper.age(data['title'])}, 200, \
    { 'Access-Control-Allow-Origin': '*', \
      'Access-Control-Allow-Methods' : 'POST' }
        
class Location(Resource):
    #For a given location(state?) provide average price/age
    def get(self, location):
        location = location.lower()
        cheat = {
            'chicago':{'avg_price':90.89,
                        'max_price':4537.00,
                        'min_price':55.00},
            'san francisco':{'avg_price':447.20,
                        'max_price':4800.00,
                        'min_price':60.00},
            'dallas':{'avg_price':194.30,
                        'max_price':4800.00,
                        'min_price':55.00}
        }
        
        if location in cheat:
            return {'status':200, 'location':location, 'avg_prive':cheat[location]['avg_price'], 'max_price':cheat[location]['max_price'], 'min_price':cheat[location]['min_price']}
        else:
            return {'status':200, 'location':location, 'avg_prive':0, 'max_price':0, 'min_price':0}

#class Add(Resource):
    #Add this ad to the dictionary
    #def post(self):
        

class Heatmap(Resource):
    @cross_origin(origins="*")
    def post(self):
        locs = helper.location_csv('data/latlong.csv')
        data = json.loads(request.data)
        rdata = []
        for d in data['data']:
            if d['location'] in locs:
               coor = helper.distribute_loc(locs[d['location']]['lat'],locs[d['location']]['long'], random.uniform(0, 10))
               rdata.append({'lat':coor[0],'long':coor[1]})
            else:
                #look it up and add to csv
                lkup = helper.loc_lookup(d['location'])
                if lkup:
                    coor = helper.distribute_loc(lkup['lat'],lkup['long'], random.uniform(0, 10))
                    rdata.append({'lat':coor[0],'long':coor[1]})
                #Else disregard
        return jsonify({'data':rdata}), 200, \
    { 'Access-Control-Allow-Origin': '*', \
      'Access-Control-Allow-Methods' : 'POST, OPTIONS' }
            
        
api.add_resource(Hello, '/')
api.add_resource(Parse, '/ad')
api.add_resource(Location, '/stats/<location>')
api.add_resource(Heatmap, '/visual/heatmap')

if __name__ == '__main__':
    app.run(debug=True)