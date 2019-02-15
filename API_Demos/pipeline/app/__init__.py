from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage

import numpy as np
import pandas as pd

from sklearn.externals import joblib

app = Flask(__name__)
api = Api(app)


class API_Pipeline(Resource):
    def post(self):
        #Get json file from request
        parser = reqparse.RequestParser()
        parser.add_argument('file',location='files',type=FileStorage,required=True)
        args = parser.parse_args(strict=True)
        file = args['file']

        #Convert to pandas dataframe
        X = pd.read_json(file)
        print('File Read')

        #Load pipeline from pickle file
        model = joblib.load('app/static/model.pkl')
        print('Model Loaded')

        #Put dataframe through the pipeline for predictions
        pred = model.predict(X)
        print('Prediction Generated')

        #Create a dataframe from the predictions and return it
        Emps = X.loc[0::,['Empcode']]
        Emps['Prediction'] = pred
        Emps = Emps.reset_index().to_json(orient='records')
        print('Prediction Sent')
        #print(Emps)
        return Emps

api.add_resource(API_Pipeline,'/pipeline')
