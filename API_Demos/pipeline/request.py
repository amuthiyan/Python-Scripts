import requests
import argparse
from flask import json

import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score

args = argparse.ArgumentParser()
args.add_argument("-f", "--file", required = True, default = "")
args = vars(args.parse_args())

#Read in file as pandas dataframe
file = args["file"]
df1 = pd.read_excel(file)
print('Data read')

#Basic Cleanup of dataframe
df1['DOL'] = df1.DOL.apply(lambda x: 0 if x=='No' else 1 if x=='Yes' else 0 if x==0 else 1)
df1=df1.rename(columns={'Productivity%':'Productivity','Quality%':'Quality'})

#Split into X and y
y = df1['DOL']
X = df1.drop('DOL',axis=1)
print('Data Split')

#Output X as json file
X.reset_index().to_json('app/static/X.json',orient='records')
print('JSON File Generated')

#Send JSON to Pipeline and get predictions
up_files = {'file':open('app/static/X.json','rb')}
headers = {'Host':'45.55.186.198:5000', 'Accept': '*/*'}
#headers = {'Host':'localhost:5000', 'Accept': '*/*'}
pred_tab = requests.request('post', 'http://localhost:5000/pipeline',files = up_files,headers = headers)
#pred_tab = requests.request('post', 'http://localhost:5000/pipeline',files = up_files,headers = headers)
#print(pred_tab)
print('JSON File Sent')

#Create results table with predictions and actual results
pred_tab = pd.read_json(pred_tab.json())
pred_tab = pd.merge(left=pred_tab,right=df1[['DOL']],left_on=['Empcode'],right_on=df1['Empcode'],how='left')
pred_tab = pred_tab.rename(columns={'DOL':'Actual'})
pred_tab = pred_tab.drop(['index'],axis=1)
print('Predictions Received')

#Compare predictions to actual results and get accuracy score
score = accuracy_score(pred_tab['Prediction'],pred_tab['Actual'])
print(pred_tab)
print('Accuracy: '+ str(score))
