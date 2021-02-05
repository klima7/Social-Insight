from .. import graph, using, style
from ..util import shorten_strings
from flask_babel import gettext as _l
import pygal


def create_chart(photo_count, limit=None):
    if limit is not None:
        photo_count = photo_count.tail(limit)

    height = len(photo_count)*25
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = shorten_strings(photo_count.index)
    chart.add('', photo_count)
    return chart


@graph(_l('Number of photos in conversations'))
@using('messages')
def recived_reactions(data):
    msg = data['messages']
    photo_count = msg.groupby(msg.conversation).photos.sum().sort_values()
    photo_count = photo_count[photo_count != 0]

    return create_chart(photo_count, 10), create_chart(photo_count)
