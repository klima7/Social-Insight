from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Messages sent by hour'))
def messages_sent_by_day_of_week(data): #
    messages = data['messages']
    messages_for_hour = messages.time.dt.hour.value_counts().sort_index()
    percent_for_hour = (messages_for_hour / messages_for_hour.sum() * 100).round(2)

    radar_chart = pygal.Radar(style=style, show_legend=False, height=800)
    radar_chart.x_labels = percent_for_hour.index
    radar_chart.add('', percent_for_hour)

    return radar_chart
