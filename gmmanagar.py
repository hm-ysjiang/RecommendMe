import googlemaps

g_maps: googlemaps.Client = None
center = tuple()


def init(key: str):
    global center
    create_client_instance(key)
    center = 24.7884, 120.99947


def create_client_instance(key: str):
    global g_maps
    g_maps = googlemaps.Client(key=key)


def search(radius, location=None, language='zh-TW'
           , min_price=0, max_price=0, name=None, open_now=None, type_=None):
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
    return g_maps.places_nearby(**kwargs)


def relocate_center(*query):
    global center
    place_id = g_maps.find_place(input=query, input_type='textquery', location_bias='ipbias', language='zh-TW')
    place = g_maps.place(place_id=place_id['candidates'][0]['place_id'])
    location = place['result']['geometry']['location']
    center = location['lat'], location['lng']
