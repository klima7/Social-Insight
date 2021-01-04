from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Percent of logins by hour'))
def logins_by_hour(data):
    acc_act = data['account_activity']
    hour_active = acc_act[(acc_act.action == 'Login') | (acc_act.action == 'Session updated')].groupby(acc_act.time.dt.hour)
    hour_active = hour_active.action.count()
    total_hours = hour_active.sum()

    hour_active = dict(hour_active)
    for i in range(24):
        if i not in hour_active:
            hour_active[i] = 0
    chart = pygal.Bar(style=style, show_legend=False)
    chart.x_labels = [i for i in range(24)]
    chart.add('', [round((hour_active[i] / total_hours) * 100, 1) for i in range(24)])
    chart.y_title = 'Percent of activity'
    chart.x_title = 'Hour'

    return chart
