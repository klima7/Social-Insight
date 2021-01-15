from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from ..posts.total_posts_graph import get_cum_graph


# wykres liczby znajomych 2
@graph(_l('Friends invites, deleted and aquired.'))
def firends_pie(data):
    frens = data['friends']
    if frens is None: # User has no friends. :(
        return None 

    by_type = frens.groupby(frens.type)
    by_type = by_type.time.count()

    pie_chart = pygal.Pie()
    for k, v in zip(by_type.index, list(by_type)):
        pie_chart.add(k.replace("_", " "), v)
    pie_chart

    return pie_chart
