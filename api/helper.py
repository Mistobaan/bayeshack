import csv, request

def location_csv(filen):
    with open(filen) as f:
        dr = csv.DictReader(f)
        locs = list()
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
        item = {'location': loc, 'lat': d['features'][0]['center'][0], 'long': d['features'][0]['center'][0]}
        with open('data/latlong.csv', 'a') as f:
            dw.write('\n"'+loc+'",'+d['features'][0]['center'][0]+','+d['features'][0]['center'][0])
        return item
    except:
        return False