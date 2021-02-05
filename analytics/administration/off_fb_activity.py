from .. import graph, using
from flask_babel import gettext as _l
import pandas as pd


def create_chart(df, limit=None):
    if limit is not None:
        df = df.tail(limit)
    return df


@graph(_l('Pages you visited while being logged into facebook'))
@using('off_facebook_activity')
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
    display = display.sort_values('number of visits', ascending=False)
    return create_chart(display, 10), create_chart(display)
