from .. import graph, using
from ip2geotools.databases.noncommercial import DbIpCity
from flask_babel import gettext as _l
import pandas as pd


@graph(_l('IP addresses'))
@using('ips')
def device_usage(data):
    ips = data['ips']

    countries = []
    cities = []

    for ip in ips.IP:
        response = DbIpCity.get(ip, api_key='free')
        countries.append(response.country)
        cities.append(response.city)

    table = pd.DataFrame({'IP': ips.IP, 'country': countries, 'city': cities})
    return table
