from .. import graph, using, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Your activity in group conversations'))
@using('messages', 'username')
def n_of_your_messages_in_group(data):
    messages = data['messages']

    messages = messages[(messages.thread_type == 'RegularGroup') & (messages.sender == data['username'])].conversation.value_counts()

    pie_chart = pygal.Pie(style=style)
    for i, v in zip(messages.index, messages):
        pie_chart.add(i, v)

    return pie_chart
