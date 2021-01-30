from .. import graph, using, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Number of each notification type'))
@using('notifications')
def types_of_notifications(data):
    notify_table = data['notifications']

    if notify_table is None:
        return None

    not_type = notify_table.groupby(notify_table.url_type).count().time

    type_chart = pygal.Pie(style=style)
    for i, t in zip(not_type.index, list(not_type)):
        type_chart.add(i, t)
        
    return type_chart
