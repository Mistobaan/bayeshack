import csv, requests, re

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

def price(x):
    basic = re.findall(r"\$\d+|\d+\$", x)
    if basic:
        return basic
    hard = re.findall(r"\d+\s*[bucks|dollars|roses|dollar]", x)
    if hard:
        parts = hard[0].split(' ')
        return '$'+str(parts[0])
    harder = re.findall(r"([A-Za-z-]+\s*(bucks|dollars|roses|dollar)\s)", x)
    if harder:
        try:
            parts = harder[0].split(' ')
        except:
            parts = harder[0][0].split(' ')
        return convert_to_dollars(parts[0])
    return []

def age(x):
    age = re.findall(r"[-/]*\s?\d{2}$", x)
    return int(age[0].replace(' ','').replace('-','').replace('/',''))

def convert_to_dollars(x):
    d = text2int(x)
    if d:
        return "$"+str(d)
    else:
        return []
    
def text2int(textnum, numwords={}):
    if not numwords:
        units = [ "zero", "one", "two", "three", "four", "five", "six",
                "seven", "eight", "nine", "ten", "eleven", "twelve",
                "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", 
                "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion", 
                'quadrillion', 'quintillion', 'sexillion', 'septillion', 
                'octillion', 'nonillion', 'decillion' ]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 
            'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    current = result = 0
    tokens = re.split(r"[\s-]+", textnum)
    for word in tokens:
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                return False

            scale, increment = numwords[word]

        if scale > 1:
            current = max(1, current)

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
 
def race(x):
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