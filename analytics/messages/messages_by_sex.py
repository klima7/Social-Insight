import pygal
from .. import graph, style
from flask_babel import gettext as _l


@graph(_l('Messages sent by sex'))
def messages_by_sex(data):
    messages = data['messages']

    messages_to = {'Male': 0, 'Female': 0, 'Unknown': 0}
    total_sent = 0

    convos = messages[(messages.thread_type == 'Regular') & (messages.sender == data['username'])].groupby('conversation')
    for user, msg in convos:
        name = user.split()
        sex = 'Unknown'
        if len(name) > 0 and name[0][-1] in ['a', 'A']:
            sex = 'Female'
        elif len(name) > 0:
            sex = 'Male'

        n_msg = msg.content.count()
        messages_to[sex] += n_msg
        total_sent += n_msg

    if messages_to['Unknown'] == 0:
        del messages_to['Unknown']
    messages_to
    chart = pygal.Pie(style=style)
    for k, v in messages_to.items():
        chart.add(k, v)
    return chart
