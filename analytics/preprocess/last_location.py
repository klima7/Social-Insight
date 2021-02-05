import json
from . import preprocessor
from datetime import datetime


@preprocessor('last_location')
def get_last_location(zip_file, folders):
    with zip_file.open('location/last_location.json') as f:
        jdata = json.loads(f.read())
        longitude = jdata['last_location']['coordinate']['longitude']
        latitude = jdata['last_location']['coordinate']['latitude']
        time = datetime.fromtimestamp(jdata['last_location']['time'])
    location = {'longitude': longitude, 'latitude': latitude, 'time': time}
    return location
