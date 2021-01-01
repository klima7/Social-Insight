from analytics import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('The people you write with most frequent'))
def your_best_friends(data):
    table = data['messages']
    regs = table[(table['thread_type'] == 'Regular') & (table['sender'] == data['username'])]
    group = regs.groupby('conversation')

    counts = group['content'].count().sort_values(ascending=False)

    chart = pygal.HorizontalBar(style=style, show_legend=False, height=len(list(counts.keys())*20))
    chart.x_labels = list(counts.keys()[::-1])
    chart.add('', counts.values[::-1])

    return chart
