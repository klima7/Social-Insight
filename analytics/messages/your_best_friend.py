from analytics import graph, using, style
from flask_babel import gettext as _l
import pygal


MAX_PEOPLE_COUNT = 40


@graph(_l('The people you write with most frequent'))
@using('messages')
def your_best_friends(data):
    table = data['messages']
    regs = table[(table['thread_type'] == 'Regular') & (table['sender'] == data['username'])]
    group = regs.groupby('conversation')

    counts = group['content'].count().sort_values(ascending=False).head(MAX_PEOPLE_COUNT)

    for i in counts.index:
        if len(i) > 25:
            counts.drop(index=i, inplace=True)

    height = len(list(counts.keys()))*25
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = list(counts.keys()[::-1])
    chart.add('', counts.values[::-1])
    chart.x_title = 'Count of messages in conversation'
    chart.y_title = 'User'
    return chart
