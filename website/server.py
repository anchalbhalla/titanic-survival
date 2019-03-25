from flask import Flask, jsonify, request, render_template,json
import urllib3, requests

app = Flask(__name__)
#HOST = '0.0.0.0'
PORT = 8080

wml_credentials={
  "password": "31dbf7ca-13bc-4b59-97ad-93db13a5c5f3",
  "url": "https://us-south.ml.cloud.ibm.com",
  "username": "59f50ecd-4ee3-4410-a687-077315fa06c3"
}

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/watson', methods=['POST','GET'])
def api_call():

	if request.method == 'POST':
		# PassengerId = request.args.get('passengerid')
		Pclass = request.form.get('pclass')
		Name = request.form.get('name')
		Sex = request.form.get('sex')
		Age = request.form.get('age')
		SibSp = request.form.get('sb') 

		Parch = request.form.get('parent')
		# Ticket = request.args.get('ticket') 
		Fare = request.form.get('fare')
		Cabin = request.form.get('cabin')
		Embark = request.form.get('embark') 


		headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
		url = '{}/v3/identity/token'.format(wml_credentials['url'])
		response = requests.get(url, headers=headers)
		mltoken = json.loads(response.text).get('token')
		header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
		# NOTE: manually define and pass the array(s) of values to be scored in the next line
		payload_scoring = {"fields": ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"], "values": [[1, int(Pclass), Name, Sex, float(Age), int(SibSp), int(Parch), str(456), float(Fare),int(Cabin), Embark]]}
		response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/v3/wml_instances/1f796ca3-54a1-494b-8e35-6dde99cf5888/deployments/6c93fe78-4a48-46c6-9456-e441a1237065/online', json=payload_scoring, headers=header)
		jsonResult = json.loads(response_scoring.text) 
		print (jsonResult)
		print (jsonResult['values'][0][14]) 

		if (jsonResult['values'][0][14]) == 1.0:
			prob = (jsonResult['values'][0][13][1])*100
			return ("Congratulations you have survived the Titanic with " + str(prob) + " probabilty") 

		elif (jsonResult['values'][0][14]) == 0.0: 
			probb = (jsonResult['values'][0][13][0])*100
			return ("Uh Oh! Sorry you could not survive the Titanic with " + str(probb) + " probabilty")

		return "200"



if __name__ == '__main__':
	app.run(debug=True, port=PORT)