from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Event responses'))
def device_usage(data):
    events = data['event_responses']

    if events is None:
        return None

    pie_chart = pygal.Pie(style=style)
    for k, v in events.items():
        pie_chart.add(k.replace("_", " "), v)

    return pie_chart
