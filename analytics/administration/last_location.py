from .. import graph, using
from geopy.geocoders import Nominatim
from flask_babel import gettext as _l
import pandas as pd


@graph(_l('Last known location'))
@using('last_location')
def device_usage(data):
    location = data['last_location']

    geolocator = Nominatim(user_agent="Social Insight")
    place = geolocator.reverse((location['latitude'], location['longitude']))

    table = pd.DataFrame(
        {
            'Attribute': ['Time', 'Latitude', 'Longitude', 'Place'],
            'Value': [str(location['time']), location['latitude'], location['longitude'], place.address]
        })

    return table
