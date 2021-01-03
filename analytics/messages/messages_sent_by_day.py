from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Messages sent by day of week'))
def messages_sent_by_day_of_week(data): #
    messages = data['messages']
    messages_for_day = messages.time.dt.dayofweek.value_counts()
    percent_for_day = messages_for_day / messages_for_day.sum() * 100

    days_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    pie_chart = pygal.Pie(style=style)
    for day, count in zip(days_names, round(percent_for_day, 2)):
        pie_chart.add(day, count)

    return pie_chart
