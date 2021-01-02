from .. import graph, style
from ..util import get_structure
from flask_babel import gettext as _l
import pygal
import pandas as pd
import json
import zipfile as zp

# To nie jest używane nigdzie indziej więc narazie tutaj jest otwierany ten plik
def load_off_facebook_activity(zip):
    folders = get_structure(zip)
    
    json_fname = None
    for name in folders['ads_and_businesses']['__files']:
#         print(name[0])
        if name[0] == 'your_off-facebook_activity.json':
            json_fname = name[1]
            break
    
    if json_fname:
#         print('json fname')
        names = []
        types = []
        times = []
        with zip.open(json_fname) as f:
            jdata = json.loads(f.read())
            for act in jdata['off_facebook_activity']:
#                 print(act['name'])
                name = act['name']
                for i in act['events']:
                    names.append(name)
                    types.append(i['type'])
                    times.append(i['timestamp'])
            table = pd.DataFrame({'name': names, 'type': types, 'time': times})
            table.time = pd.to_datetime(table.time, unit='s')
            return table

# Wyświetla się max 10, ale jak jest więcej to fajnie by było dać możliwość rozwinięcia tabelki czy coś.
@graph(_l('Pages you visited while being logged into facebook'))
def device_usage(data):
    activ = load_off_facebook_activity(data['zip_obj'])
    if activ is None:
        return pd.DataFrame({'Info': ['No data']})
    display = None
    arrs = [[], [], [], []]
    for name, info in activ.groupby(activ.name):
        arrs[0].append(name)
        arrs[1].append(info.name.count())
        arrs[2].append(info.time.min())
        arrs[3].append(info.time.max())
    display = pd.DataFrame({'name': arrs[0], 'number of visits': arrs[1], 'first visited': arrs[2], 'last visit': arrs[3]})
    return display.sort_values('number of visits', ascending=False)[:10]
