import requests, json
from Googlemap2 import getdetail

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
