from flask import Flask, request, jsonify, Response
from flask.ext.restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        #Just say hello
        return {'status':200, 'message': "Hello! I'm a quick api to parse Backpage ad data"}

class Parse(Resource):
    def post(self):
        # {'text':"Here's some text"}
        data = json.loads(request.data)
        return {'status':200, 'message': "Here's what you sent:"+data['text']}

api.add_resource(Hello, '/')
api.add_resource(Parse, '/ad')

if __name__ == '__main__':
    app.run(debug=True)