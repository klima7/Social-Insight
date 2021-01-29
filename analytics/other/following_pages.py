from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from ..posts.total_posts_graph import get_cum_graph

@graph(_l('Number of followed pages'))
def following_people(data):
    follows = data['following']

    if follows is None:
        return None

    vals, index = get_cum_graph(follows[follows.type == 'page'].time)
    chart = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    chart.x_labels = index.date
    chart.add('', list(vals))

    return chart