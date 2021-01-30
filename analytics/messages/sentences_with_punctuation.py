from .. import graph, using, style
from flask_babel import gettext as _l
import pygal
import re
import pandas as pd


MAX_PEOPLE = 30


def get_percent_of_messages_with_punctuation(mess):
    n_messages = len(mess)
    msg_with_punctuation = sum(1 for k in mess if re.findall(r'[,.?!;:]', k))
    return round(msg_with_punctuation / n_messages * 100)


@graph(_l('Percent of sentences with punctuation'))
@using('messages')
def words_count_in_message(data):
    all_messages = data['messages']
    messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender != data['username'])].dropna()

    names = []
    percents = []

    for conv, msgs in messages.groupby(messages.conversation):
        if msgs.content is not None and len(msgs.content) > 1:

            # Omijanie użytkowników o długich nazwach(np. weeia), bo psują formatowanie
            if len(conv) > 25:
                continue

            percent = get_percent_of_messages_with_punctuation(msgs.content)
            names.append(conv)
            percents.append(percent)

    df = pd.DataFrame({'name': names, 'percent': percents})
    df = df.sort_values('percent', ascending=True).tail(MAX_PEOPLE)

    height = len(df.name)*25
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = df.name
    chart.add('', df.percent)
    chart.x_title = 'Percent of sentences with punctuation'
    chart.y_title = 'User'
    return chart
