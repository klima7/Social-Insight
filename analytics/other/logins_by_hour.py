from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Percent of logins by hour'))
def logins_by_hour(data):
    acc_act = data['account_activity']
    hour_active = acc_act[(acc_act.action == 'Login') | (acc_act.action == 'Session updated')].groupby(acc_act.time.dt.hour)
    hour_active = hour_active.action.count()
    percent_active = (hour_active / hour_active.sum() * 100).round(1)

    empty_series = pd.Series([0]*24, list(range(24)))
    percent_active = percent_active.add(empty_series, fill_value=0)

    radar_chart = pygal.Radar(style=style, show_legend=False, fill=True, height=800)
    radar_chart.x_labels = percent_active.index
    radar_chart.add('', percent_active)

    return radar_chart
