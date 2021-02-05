from .. import graph, using
from ip2geotools.databases.noncommercial import DbIpCity
from flask_babel import gettext as _l
import pandas as pd


@graph(_l('Mobile devices'))
@using('mobile_devices')
def device_usage(data):
    devices = data['mobile_devices']
    return devices
