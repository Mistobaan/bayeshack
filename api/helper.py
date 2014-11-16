import csv, requests

def location_csv(filen):
    with open(filen) as f:
        dr = csv.DictReader(f)
        locs = dict()
        for r in dr:
            locs[r['location']] = {'lat':r['lat'], 'long':r['long']}
        return locs
        
def loc_lookup(loc):
    if loc:
        q = requests.get('http://api.tiles.mapbox.com/v4/geocode/mapbox.places-v1/'+loc+'.json?access_token=pk.eyJ1IjoiYmVsbG1hciIsImEiOiJVTEw4blc0In0.LmVGYsloyWfYTtyPMVehHA')
        d = q.json()
    else:
        return False
    try:
        item = {'location': loc, 'lat': d['features'][0]['center'][1], 'long': d['features'][0]['center'][0]}
        with open('data/latlong.csv', 'a') as f:
            dw.write('\n"'+loc+'",'+d['features'][0]['center'][1]+','+d['features'][0]['center'][0])
        return item
    except:
        return False
        
def distribute_loc(lat1, lon1, d, b=30):
    import geopy
    from geopy.distance import VincentyDistance
    origin = geopy.Point(lat1, lon1)
    destination = VincentyDistance(kilometers=d).destination(origin, b)

    lat2, lon2 = destination.latitude, destination.longitude
    return (lat2,lon2)
    
def race(x):
    import re
    x=x.lower()
    white=re.compile('(white|caucasian|caucasians|blonde|brunette|red|blond|blondie)')
    if white.search(x):
        return("white")
    black=re.compile('(black|african|ebony|blk|creole|creol|African American|chocolate|chocalate)')
    if black.search(x):
        return("black")
    hispanic=re.compile('(hispanic|latina|mexican|puerto rican|cuban|latin)')
    if hispanic.search(x):
        return("hispanic")
    asian=re.compile('(asian|asain|oriental)')
    if asian.search(x):
        return("asian")
    indian=re.compile('(indian|lakota|cherokee|navajo|sioux)')
    if indian.search(x):
        return("indian")
    else:
        return("unidentified/other")