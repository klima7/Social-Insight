from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Device'))
def device_usage(data):
    acc_act = data['account_activity']
    device = acc_act.device.value_counts()
    device = device / device.sum() * 100
    device = device.round(2)

    pie_chart = pygal.Pie(style=style, inner_radius=.4)
    for device, count in zip(device.index, device):
        pie_chart.add(device, count)

    return pie_chart

    return chart
