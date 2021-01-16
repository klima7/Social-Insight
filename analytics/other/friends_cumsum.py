from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from ..posts.total_posts_graph import get_cum_graph


# wykres liczby znajomych 2
@graph(_l('Friends count'))
def friends_cumsum(data):
    frens = data['friends']
    if frens is None: # User has no friends. :(
        return None 

    chart = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    vals, index = get_cum_graph(frens[frens.type == 'friends'].time)
    chart.x_labels = index.date
    chart.add('', list(vals), dots_size=0)
    chart.y_title = 'Friends count'
    chart.x_title = 'Date'

    return chart
