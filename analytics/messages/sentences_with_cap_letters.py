import pygal
from .. import graph, style
from flask_babel import gettext as _l
import re
import pandas as pd


MAX_PEOPLE = 30


def get_sentences_percent_with_cap_letter(message):
    sentences = []  # 1 - zdanie zaczęte wielką literą, 0 - zdanie zaczęte niewielką literą
    for s in message:
        t = [1 if len(i.strip()) > 0 and i.strip()[0].isupper() else 0 for i in list(filter(lambda i: len(i) > 0, re.split(r'[.?!]', s)))] # zdania w wiadomości
        sentences.extend(t)
    return round(sum(sentences) / len(sentences) * 100)


@graph(_l('Percent of sentences starting with capital letter'))
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

            percent = get_sentences_percent_with_cap_letter(msgs.content)
            names.append(conv)
            percents.append(percent)

    df = pd.DataFrame({'name': names, 'percent': percents})
    df = df.sort_values('percent', ascending=True).tail(MAX_PEOPLE)

    height = len(df.name)*25
    chart = pygal.HorizontalBar(style=style, show_legend=False, height=height)
    chart.x_labels = df.name
    chart.add('', df.percent)

    chart.x_title = 'Percent of sentences starting with capital letter'
    chart.y_title = 'User'

    return chart
