from .. import graph
from flask_babel import gettext as _l
import pandas as pd


# Wyświetla się max 10, ale jak jest więcej to fajnie by było dać możliwość rozwinięcia tabelki czy coś.
@graph(_l('Pages you visited while being logged into facebook'))
def device_usage(data):
    activity = data['off_facebook_activity']
    if activity is None:
        return pd.DataFrame({'Info': ['No data']})
    arrays = [[], [], [], []]
    for name, info in activity.groupby(activity.name):
        arrays[0].append(name)
        arrays[1].append(info.name.count())
        arrays[2].append(info.time.min())
        arrays[3].append(info.time.max())
    display = pd.DataFrame({'name': arrays[0], 'number of visits': arrays[1], 'first visited': arrays[2], 'last visit': arrays[3]})
    return display.sort_values('number of visits', ascending=False)[:10]
