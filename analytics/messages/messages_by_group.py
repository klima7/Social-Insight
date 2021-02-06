from .. import graph, using, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Number of messages in group conversations'))
@using('messages')
def n_of_messages_in_group(data):
    messages = data['messages']

    messages = messages[(messages.thread_type == 'RegularGroup')].conversation.value_counts()

    pie_chart = pygal.Pie(style=style)
    for i, v in zip(messages.index, messages):
        pie_chart.add(i, v)

    return pie_chart
