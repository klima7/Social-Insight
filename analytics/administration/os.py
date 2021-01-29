from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Operating system'))
def device_usage(data):
    acc_act = data['account_activity']
    os = acc_act.os.value_counts()
    os = os / os.sum() * 100
    os = os.round(2)

    pie_chart = pygal.Pie(style=style, inner_radius=.4)
    for os, count in zip(os.index, os):
        pie_chart.add(os, count)

    return pie_chart
