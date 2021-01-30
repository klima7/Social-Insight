from .. import graph, using, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Percent of notifications by hour'))
@using('notifications')
def notifications_by_hour(data):
    notify_table = data['notifications']

    if notify_table is None:
        return None

    by_hour = notify_table.groupby(notify_table.time.dt.hour)
    total = len(notify_table)
    by_hour = dict(by_hour.count().time)
    index = range(24)
    values = [(by_hour[i] / total) * 100 if i in by_hour else 0 for i in index]

    radar_chart = pygal.Radar(show_legend=False, fill=True, height=800, style=style)
    radar_chart.x_labels = index
    radar_chart.add('', values)

    return radar_chart
