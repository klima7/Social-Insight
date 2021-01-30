from .. import graph, using, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Percent of notifications by day'))
@using('notifications')
def notifications_by_day(data):
    notify_table = data['notifications']

    if notify_table is None:
        return None

    by_day = notify_table.time.dt.dayofweek.value_counts()
    by_day = by_day / by_day.sum() * 100

    empty_series = pd.Series([0]*7, list(range(7)))
    by_day = by_day.add(empty_series, fill_value=0)

    days_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    pie_chart = pygal.Pie(style=style)
    for day, count in zip(days_names, round(by_day, 2)):
        pie_chart.add(day, count)

    return pie_chart
