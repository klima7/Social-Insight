from .. import graph, using, style
from ..util import shorten_strings, calc_bar_chart_height
from flask_babel import gettext as _l
import pygal
import re
import pandas as pd


def get_percent_of_messages_with_punctuation(mess):
    if len(mess) == 0:
        return 0
    n_messages = len(mess)
    msg_with_punctuation = sum(1 for k in mess if re.findall(r'[,.?!;:]', k))
    return round(msg_with_punctuation / n_messages * 100)


def create_chart(df, limit=None):
    if limit is not None:
        df = df.tail(limit)

    height = calc_bar_chart_height(df.name)
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = shorten_strings(df.name)
    chart.add('', df.percent)
    chart.x_title = 'Percent of sentences with punctuation'
    chart.y_title = 'User'
    return chart


@graph(_l('Percent of sentences with punctuation'))
@using('messages', 'username')
def words_count_in_message(data):
    all_messages = data['messages']
    messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender != data['username'])].dropna()

    names = []
    percents = []

    for conv, msgs in messages.groupby(messages.conversation):
        if msgs.content is not None and len(msgs.content) > 1:

            percent = get_percent_of_messages_with_punctuation(msgs.content)
            names.append(conv)
            percents.append(percent)

    df = pd.DataFrame({'name': names, 'percent': percents}).sort_values('percent', ascending=True)

    return create_chart(df, 25), create_chart(df)
