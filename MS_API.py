from flask import Flask, render_template
from flask_restful import Resource,Api,reqparse
import pandas as pd
import os
import json
import ast

# template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print(template_dir)

app = Flask(__name__)
api = Api(app)
app.static_folder = 'static'

@app.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/display')
def display_page():
    return render_template('display.html')

@app.route('/table')
def table_page():
    return render_template('table.html')

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
    #TODO: Delete debug in finalized stage!
    app.run(debug=True)  # run our Flask app