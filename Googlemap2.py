
from tokenize import String

import requests, json
import datetime
def getdetail(name):
    days= {"Monday": 0, 'Tuesday':1 , 'Wednesday':2 , 'Thursday': 3, 'Friday' : 4, 'Saturday': 5, 'Sunday' : 6}
    day = datetime.datetime.now()
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

