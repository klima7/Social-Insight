from .. import graph, using, style
from ..util import shorten_strings
from flask_babel import gettext as _l
import pygal


def create_graph(group_inter, limit=None):
    if limit is not None:
        group_inter = group_inter.tail(limit)

    height = len(group_inter) * 25
    group_chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    group_chart.x_labels = shorten_strings(group_inter.name, width=40)
    group_chart.add('', group_inter.value)
    return group_chart


@graph(_l('Number of interactions with groups'))
@using('group_interactions')
def group_interactions(data):
    group_inter = data['group_interactions'].sort_values(by='value')

    return create_graph(group_inter, 30), create_graph(group_inter)
