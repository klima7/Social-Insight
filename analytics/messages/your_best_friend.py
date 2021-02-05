from analytics import graph, using, style
from ..util import shorten_strings, calc_bar_chart_height
from flask_babel import gettext as _l
import pygal


def create_chart(counts, limit=None):
    if limit is not None:
        counts = counts.head(limit)

    height = calc_bar_chart_height(list(counts.keys()))
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = shorten_strings(counts.keys()[::-1])
    chart.add('', counts.values[::-1])
    chart.x_title = 'Number of messages in conversation'
    chart.y_title = 'User'
    return chart


@graph(_l('The people you write with most frequent'))
@using('messages', 'username')
def your_best_friends(data):
    table = data['messages']
    regs = table[(table['thread_type'] == 'Regular') & (table['sender'] == data['username'])]
    group = regs.groupby('conversation')
    counts = group['content'].count().sort_values(ascending=False)

    return create_chart(counts, 30), create_chart(counts)
