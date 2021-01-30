from .. import graph, using, style
from flask_babel import gettext as _l
import pygal

MAX_GROUP_COUNT = 40
MAX_TITLE_LEN = 40


def shorten_title(s):
    if len(s) > MAX_TITLE_LEN:
        s = s[:MAX_TITLE_LEN] + '...'
    return s


@graph(_l('Number of interactions with groups'))
@using('group_interactions')
def group_interactions(data):
    group_inter = data['group_interactions'].sort_values(by='value').tail(MAX_GROUP_COUNT)

    group_chart = pygal.HorizontalBar(style=style, show_legend=False)
    group_chart.x_labels = list(map(shorten_title, list(group_inter.name)))
    group_chart.add('', list(group_inter.value))

    return group_chart
