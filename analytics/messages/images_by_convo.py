from .. import graph, style
from flask_babel import gettext as _l
import pygal
import emoji

MAX_PEOPLE_COUNT = 40

@graph(_l('Number of photos in conversations'))
def reacived_reactions(data):
    msg = data['messages']
    photo_count = msg.groupby(msg.conversation).photos.sum().sort_values().tail(MAX_PEOPLE_COUNT)
    photo_count = photo_count[photo_count != 0]
    chart = pygal.HorizontalBar(style=style, show_legend=False)
    chart.x_labels = list(photo_count.index)
    chart.add('', photo_count)

    return chart