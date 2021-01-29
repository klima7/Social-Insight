from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Usage statistics'))
def device_usage(data):
    acc_act = data['account_activity']
    acc_act['agent'] = acc_act.device + ' / ' + acc_act.os + ' / ' + acc_act.browser
    acc_act.agent.unique()
    device_usage = acc_act.groupby(acc_act.agent).action.count().sort_values(ascending=True)
    total_uses = device_usage.sum()

    chart = pygal.HorizontalBar(style=style, show_legend=False)
    chart.x_labels = list(device_usage.index)
    chart.add('', [round((i / total_uses) * 100, 1) for i in list(device_usage)])
    chart.x_title = 'Percent of usage'
    chart.y_title = 'Device'

    return chart
