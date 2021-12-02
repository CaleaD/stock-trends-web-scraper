from flask import Flask
from flask_restful import Resource,Api,reqparse
import pandas as pd
import json
import ast

app=Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        df = pd.read_json('articles.txt')
        data = df.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('symbol', required=True)
        #parser.add_argument('sth1', required=True)
        #parser.add_argument('sth2', required=True)
        pass

class Locations(Resource):
    # methods go here
    pass


api.add_resource(Users, '/users')  # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations

if __name__ == '__main__':
    app.run()  # run our Flask app