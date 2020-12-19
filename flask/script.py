import numpy as np
from flask import Flask, request, jsonify, render_template
import requests
import pickle
import os
'''
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
'''

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "****"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#app.config.from_object('config')

'''
lm= LoginManager()
lm.init_app(app)
oid = OpenID(app,os.path.join(basedir,'tmp'))
lm.login_view = 'login'
'''
#from app import views, models

@app.route('/')
def home():
    return render_template('index.html')
  
@app.route('/result', methods = ['POST']) 
def result():
	if request.method == 'POST':
		to_predict_list = request.form.to_dict()
		to_predict_list = list(to_predict_list.values())
		predict_list1 = []
		target_list = ["Exited"]
		for x in to_predict_list:
			predict_list1.append(str(x))
		geography = []
		gender = []
		print(predict_list1[1],predict_list1[2])
		if predict_list1[1] == '0':
			print("Geography = 0")
			geography = ['1', '0', '0']
		elif predict_list1[1] == '1':
			geography = ['0', '1', '0']
		elif predict_list1[1] == '2':
			geography = ['0', '0', '1']
		if predict_list1[2] == '0':
			gender = ['1', '0']
		elif predict_list1[2] == '1':
			gender = ['0', '1']
		predict_list = []
		predict_list.append(predict_list1[0])
		predict_list = predict_list + predict_list1[3:] 
		predict_list = predict_list + geography
		predict_list = predict_list + gender
		predict_dict = {}
		fields = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Geography_France', 'Geography_Germany', 'Geography_Spain', 'Gender_Female', 'Gender_Male']
		for i in range(0,len(predict_list)-1):
			predict_dict[fields[i]] = predict_list[i]
		#payload_scoring = {"input_data": [predict_dict], "target":{"type": 'parameter', "name":'Exited'}}
		print(fields)
		print(predict_list)
		print(len(predict_list))
		#payload_scoring = {"fields": fields, "values": [predict_list, predict_list]}
		payload_scoring = {"input_data": [{"fields": ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Geography_France', 'Geography_Germany', 'Geography_Spain', 'Gender_Female', 'Gender_Male'], "values": [predict_list]}]}
		response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/7646674b-02dd-4f8e-869c-06c6d8fa044f/predictions?version=2020-12-19', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
		print("Scoring response")
		print(response_scoring.json())
		predictions = response_scoring.json()
		result = predictions['predictions'][0]['values'][0][0]
		print(result)
		if int(result) == 1:
			prediction ='The customer will exit from the company'
		else:
			prediction ='The customer will continue in the company'
	return render_template("result.html", prediction = prediction) 
		
		
if __name__ == "__main__":
	app.run()



import requests