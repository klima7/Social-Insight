from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph('other', _l('Device usage statistics'))
def device_usage(data):
    acc_act = data['account_activity']
    acc_act.agent.unique()
    device_usage = acc_act.groupby(acc_act.agent).action.count().sort_values(ascending=True)
    total_uses = device_usage.sum()

    chart = pygal.HorizontalBar(style=style, show_legend=False)
    chart.x_labels = list(device_usage.index)
    chart.add('', [ (i / total_uses) * 100 for i in list(device_usage)])
    # chart.y_title = 'device name'
    chart.x_title = '% of usage'

    return chart
