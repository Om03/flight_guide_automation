# app.py
from flask import Flask, session, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta
import gmplot
from datetime import datetime
import requests, json
from tokenize import String
from collections import Counter

def getdetail(name):
    days= {"Monday": 0, 'Tuesday':1 , 'Wednesday':2 , 'Thursday': 3, 'Friday' : 4, 'Saturday': 5, 'Sunday' : 6}
    day = datetime.now()
    num= days[day.strftime("%A")]
    api_key = 'AIzaSyCvUo5G2lpWno3rMu0jNb8-4jGVs_dHxJo'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query = name
    r = requests.get(url + 'query=' + name +
                 '&key=' + api_key)
    x = r.json()
    y = x['results']
    id = y[0]['place_id']
    url2 = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&fields=name,rating,formatted_phone_number,opening_hours,website,formatted_address&key={api_key}"
    c= requests.get(url2)
    result = c.json()
    i= 'result'
    dict =result[i].keys()
    if 'formatted_phone_number' not in dict:
        result[i]['formatted_phone_number'] = "None"
    if 'website'not in dict:
        result[i]['website'] ="None"
    if 'formatted_address' not in dict:
        result[i]['formatted_address'] = "None"
    list =[result[i]['name'] ,result[i]['formatted_phone_number'] , result[i]['website'],result[i]['formatted_address']]
    return list
def get_airports():
    api_key = 'AIzaSyCvUo5G2lpWno3rMu0jNb8-4jGVs_dHxJo'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query = 'Airports near me'
    r = requests.get(url + 'query=' + query +
                     '&key=' + api_key)
    x = r.json()
    y = x['results']
    ans =[]

    for i in range(len(y)):
        ans.append(y[i]['name'])
    return ans

z_list = []
y_list = []
app = Flask(__name__)
app.secret_key = "yupjenil"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'OM@95.60'
app.config['MYSQL_DATABASE_DB'] = 'jetlag'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect() 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE user = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['user']
            return render_template('feature_page/index.html')
        else:
            pass
    return render_template('Login/index.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect() 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('INSERT INTO login VALUES (%s, %s)', (username, password,))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('Login/signup.html')

@app.route('/jet_lag')
def jet_lag():
    with open('Airport_list - Sheet1.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        readers = list(reader)
        return render_template('jetlag_form/lag_form.html',reader = readers)

@app.route('/create',methods=['GET', 'POST'])
def create():
    jetlag_input = defaultdict(lambda: None)
    jetlag_input["airport_from"] = request.form['airport_from']
    jetlag_input["airport_to"] = request.form['airport_to']
    jetlag_input["departing_on_date"] = request.form['departing_on_date']
    jetlag_input["departing_on_time"] = request.form['departing_on_time']
    jetlag_input["arriving_on_date"] = request.form['arriving_on_date']
    jetlag_input["arriving_on_time"] = request.form['arriving_on_time']
    jetlag_input["bed_at"] = request.form['bed_at']
    jetlag_input["wake_at"] = request.form['wake_at']
    with open('Airport_list - Sheet1.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        readers = list(reader)
    from_place = "lol"
    to_place = "lol"
    for i in range(len(readers)):
        if readers[i][0] == jetlag_input["airport_from"].split(", ")[0]:
            from_place = readers[i]
            break
    for i in range(len(readers)):
        if readers[i][0] == jetlag_input["airport_to"].split(", ")[0]:
            to_place = readers[i]
            break
    print(from_place)
    print(to_place)
    utcnow = timezone('utc').localize(datetime.utcnow())  # generic time
    here = utcnow.astimezone(timezone(from_place[-1])).replace(tzinfo=None)
    there = utcnow.astimezone(timezone(to_place[-1])).replace(tzinfo=None)

    offset = relativedelta(here, there).hours

    dept_date = datetime.strptime(jetlag_input["departing_on_date"], "%Y-%m-%d").date()
    dept_time = datetime.strptime(jetlag_input["departing_on_time"], "%H:%M")

    arrv_date = datetime.strptime(jetlag_input["arriving_on_date"], "%Y-%m-%d").date()
    arr_time = datetime.strptime(jetlag_input["arriving_on_time"], "%H:%M")

    new_sleep = usual_sleep = datetime.strptime(jetlag_input["bed_at"], "%H:%M")
    usual_awake = datetime.strptime(jetlag_input["wake_at"], "%H:%M")
    sleep_duration = usual_awake - usual_sleep
    schedule = []
    for i in range(7,0,-1):
        new_sleep += timedelta(hours = offset/7)
        wake_up = new_sleep + sleep_duration
        schedule.append([dept_date - timedelta(i), " Seek Light-", str((new_sleep - timedelta(hours = 4)).time()), " Sleep well-",str(new_sleep.time()), " Wake up-",str(wake_up.time())])
    new_sleep += timedelta(hours = offset/7)
    wake_up = new_sleep + sleep_duration
    schedule_departure = []
    schedule_departure.append([dept_date, dept_time.time(), " Seek Light -", str((usual_sleep - timedelta(hours = 8)).time()), " Avoid Light-",str((usual_sleep - timedelta(hours = 4)).time()), " Wake up-",str(usual_sleep.time())])
    return render_template('jetlag_schedule/jetlag_schd.html', schedule = schedule, schedule_departure = schedule_departure, from_place = from_place[1], to_place = to_place[1])

@app.route('/show_port', methods=['GET', 'POST'])
def show_port():
    with open('Airport_list - Sheet1.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        readers = list(reader)
    z = request.form['z_cordt']
    y = request.form['y_cordt']
    z_list.append(z)
    y_list.append(y)
    return render_template('map_form/map_select.html',z=z, y=y,flag = 1, readers=readers)

@app.route('/show_port_selected', methods=['GET', 'POST'])
def show_port_selected():
    with open('Airport_list - Sheet1.csv', 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        readers = list(reader)
    airport_to = request.form['airport_to']
    def get_loc(lat,long,dest):
        apikey = 'AIzaSyCvUo5G2lpWno3rMu0jNb8-4jGVs_dHxJo' # (your API key here)\
        location2 = gmplot.GoogleMapPlotter.geocode(dest, apikey=apikey)
        gmap = gmplot.GoogleMapPlotter(lat, long, 13, apikey=apikey)
        gmap.directions(
            (lat,long),
            location2
        )
        gmap.draw(r'C:\Users\Om Parab\OneDrive\Desktop\mini_proj_sem-4\mini_proj_sem-4\templates\map.html')
    get_loc(float(z_list[-1]), float(y_list[-1]),airport_to)
    return render_template('map.html')

@app.route('/airport_near')
def airport_near():
    list_of_airports = get_airports()

    airport_info = []
    for i in list_of_airports:
        airport_info.append(getdetail(i))

    return render_template('airports_near_me/index.html',airport_info = airport_info)

if __name__ == '__main__':
    app.run(debug=True)
