from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from ..posts.total_posts_graph import get_cum_graph

@graph(_l('Cumulated number of likes'))
def number_of_likes(data):
    comment_data = data['likes']
    vals, index = get_cum_graph(comment_data['time'])
    char = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    char.x_labels = index.date
    char.add('', list(vals))

    return char
