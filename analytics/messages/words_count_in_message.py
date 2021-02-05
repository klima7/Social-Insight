from .. import graph, using, style
from ..util import shorten_strings, calc_bar_chart_height
from flask_babel import gettext as _l
import pygal
import re
import pandas as pd


def get_avg_message_length(message):
    msg_lens = [len(list(filter(lambda i: len(i) > 0, re.split(r'[\s,]', i)))) for i in message if i is not None]
    avg_word_count = sum(msg_lens)/len(msg_lens) if len(msg_lens) != 0 else 0
    return round(avg_word_count, 1)


def create_chart(df, limit=None):
    if limit is not None:
        df = df.tail(limit)

    height = calc_bar_chart_height(df.name)
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = shorten_strings(df.name)
    chart.add('', df.avg_word)
    chart.x_title = 'Average count of words in sentence'
    chart.y_title = 'User'
    return chart


@graph(_l('Average words count in message'))
@using('messages', 'username')
def words_count_in_message(data):
    all_messages = data['messages']
    messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender != data['username'])].dropna()

    names = []
    lengths = []

    for conv, msgs in messages.groupby(messages.conversation):
        if msgs.content is not None and len(msgs.content) > 1:

            length = get_avg_message_length(msgs.content)
            names.append(conv)
            lengths.append(length)

    df = pd.DataFrame({'name': names, 'avg_word': lengths})
    df = df.sort_values('avg_word', ascending=True)

    return create_chart(df, 25), create_chart(df)
