from .. import graph, using, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Messages sent by hour'))
@using('messages', 'username')
def messages_sent_by_day_of_week(data):
    messages = data['messages']
    messages = messages[messages.sender == data['username']]
    messages_for_hour = messages.time.dt.hour.value_counts().sort_index()
    percent_for_hour = (messages_for_hour / messages_for_hour.sum() * 100).round(2)

    empty_series = pd.Series([0]*24, list(range(24)))
    percent_for_hour = percent_for_hour.add(empty_series, fill_value=0)

    radar_chart = pygal.Radar(style=style, show_legend=False, fill=True, height=800)
    radar_chart.x_labels = percent_for_hour.index
    radar_chart.add('', percent_for_hour)

    return radar_chart
