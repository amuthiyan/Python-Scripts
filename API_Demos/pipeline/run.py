#!flask/bin/python

from app import app

from app.Healthcare_EDA_functions import *
from app.Pipeline_Classes import *
from sklearn.externals import joblib

#Load model columns for get_dummies in the pipeline
d_accepted = joblib.load('app/static/column_vals.pkl')

#Load list of good/bad supervisors for pipeline
d_supervisors = joblib.load('app/static/sup_dict.pkl')

#app.run(debug=True,host='0.0.0.0',port=80)

app.run(debug=True)
