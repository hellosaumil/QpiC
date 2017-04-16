from flask import Flask, request, render_template
import requests
import json
app = Flask(__name__)

@app.route('/')									# maps url to rturn statement of the function, @ is decorator		
@app.route('/<user>')
def index(user=None):
	return render_template('user.html',user=user)

@app.route('/run_post')
def post_json():
    url = 'http://localhost:5000/receive'
    data = {'query':['java','android','html','css','spring','spring-mvc','bobbo']}
    headers = {'Content-Type' : 'application/json'}
    print ('hi')
    r = requests.post(url, data=json.dumps(data), headers=headers)
    #return json.dumps(r.json(), indent=4)
    return r.text

if __name__ == '__main__':
	app.run(port=5001,debug=True)							# debug=True: developer mode