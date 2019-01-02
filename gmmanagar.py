import googlemaps
import googlemaps.exceptions
import haversine
import kcparser

key = kcparser.get_google_api_key()

g_maps: googlemaps.Client = None
center = tuple()
center_id = ''


def init():
    global center, center_id
    create_client_instance()
    # Locate to NCTU
    center = 24.7884, 120.99947
    center_id = 'ChIJMV8k71c2aDQRmj5yOn_aKTk'


def create_client_instance():
    global g_maps
    g_maps = googlemaps.Client(key=key)


def search(radius=1000, location=None, language='zh-TW'
           , min_price=0, max_price=0, name=None, open_now=None, type_=None, page_token=None):
    kwargs = dict()
    kwargs['location'] = location if location else center
    kwargs['radius'] = radius
    kwargs['language'] = language
    if min_price > 0:
        kwargs['min_price'] = min_price
    if max_price > 0:
        kwargs['max_price'] = max_price
    if name:
        kwargs['name'] = name
    if open_now:
        kwargs['open_now'] = open_now
    if type_:
        kwargs['type'] = type_
    if page_token:
        kwargs['page_token'] = page_token
    return g_maps.places_nearby(**kwargs)


def get_distance(p1, p2=None):
    if not p2:
        global center
        p2 = center
    return float(str(haversine.haversine(p1, p2))[:3])


def relocate_center_latlng(lat, lng):
    global center, center_id
    center_id = ''
    center = lat, lng


def relocate_center_place_id(place_id):
    global center, center_id
    center_id = place_id
    place = g_maps.place(place_id=place_id)
    location = place['result']['geometry']['location']
    center = location['lat'], location['lng']


def relocate_center_query(query):
    global center
    place_id = g_maps.find_place(input=query, input_type='textquery', location_bias='ipbias', language='zh-TW')
    place = g_maps.place(place_id=place_id['candidates'][0]['place_id'])
    location = place['result']['geometry']['location']
    center = location['lat'], location['lng']
