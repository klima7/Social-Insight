from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
from .total_posts_graph import get_cum_graph

MAX_GROUP_COUNT = 40
MAX_TITLE_LEN = 40

def shorten_title(s):
    if len(s) > MAX_TITLE_LEN:
        s = s[:MAX_TITLE_LEN] + '...'
    return s

@graph(_l('Comments in each group'))
def coments_in_group(data):
    comment_data = data['comments']
    comm_by_group = comment_data.groupby(comment_data.group).time.count().dropna()
    comm_by_group = comm_by_group.sort_values().head(MAX_GROUP_COUNT)

    group_chart = pygal.HorizontalBar(style=style, show_legend=False)
    group_chart.x_labels = list(map(shorten_title, comm_by_group.index))
    group_chart.add('', list(comm_by_group))    
    
    return group_chart