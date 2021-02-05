from .. import graph, using, style
from ..util import calc_bar_chart_height
from flask_babel import gettext as _l
import pygal


MAX_GROUP_COUNT = 40
MAX_TITLE_LEN = 40


def shorten_title(s):
    if len(s) > MAX_TITLE_LEN:
        s = s[:MAX_TITLE_LEN] + '...'
    return s


@graph(_l('Comments in each group'))
@using('comments')
def coments_in_group(data):
    comment_data = data['comments']
    comm_by_group = comment_data.groupby(comment_data.group).time.count().dropna()
    comm_by_group = comm_by_group.sort_values().tail(MAX_GROUP_COUNT)

    height = calc_bar_chart_height(comm_by_group)
    group_chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    group_chart.x_labels = list(map(shorten_title, comm_by_group.index))
    group_chart.add('', list(comm_by_group))    
    
    return group_chart
