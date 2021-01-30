from .. import graph, using, style
from flask_babel import gettext as _l
import pygal
from ..posts.total_posts_graph import get_cum_graph


@graph(_l('Number of group memberships'))
@using('groups_join')
def numer_of_groups(data):
    join_times = data['groups_join']

    vals, index = get_cum_graph(join_times.time)
    chart = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    chart.x_labels = index.date
    chart.add('', list(vals))

    return chart
