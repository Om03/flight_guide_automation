from flask import *
from werkzeug.utils import import_string
import requests
import googlmap
import Googlemap2
app = Flask(__name__)

@app.route('/')
def pass_val():
    if request.method == 'POST':
        return jsonify('hello')
    return render_template('index.html')

@app.route('/get_ans',methods = ['POST','GET'])
def get_ans():
    if request.method == 'POST':
        return jsonify(googlmap.get_airports())
    if request.method == 'GET':
        req =request.get_json()
        print(req)
        return jsonify("helloooo")

@app.route('/get_airport',methods = ['POST','GET'])
def get_airport():
    if request.method == 'POST':
        req =request.get_json()
        return jsonify(Googlemap2.getdetail(req))

if __name__ == '__main__':
   app.run(debug=True)