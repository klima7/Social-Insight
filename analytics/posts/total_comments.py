from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from .total_posts_graph import get_cum_graph

@graph(_l('Cumulated number of comments'))
def device_usage(data):
    comment_data = data['comments']
    vals, index = get_cum_graph(comment_data['time'])
    char = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    char.x_labels = index.date
    char.add('', list(vals))

    return char
