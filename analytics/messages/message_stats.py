import pygal
from .. import graph, style
from flask_babel import gettext as _l
import re
import pandas as pd


def get_messages_stats(mess):
    n_messages = len(mess)
    msg_with_punct = sum(1 for k in mess if re.findall(r'[,.?!;:]', k)) # Wiadomości ze znakami interpunkcyjnymi

    msg_lens = [len(list(filter(lambda i: len(i) > 0, re.split(r'[\s,]', i)))) for i in mess if i is not None] # liczba słów w wiadomości.
    avg_word_count = sum(msg_lens)/len(msg_lens)

    sentences = [] # 1 - zdanie zaczęte wielką literą, 0 - zdanie zaczęte niewielką literą
    for s in mess:
        t = [1 if i.strip()[0].isupper() else 0 for i in list(filter(lambda i: len(i) > 0, re.split(r'[.?!]', s)))] # zdania w wiadomości
        sentences.extend(t)

    stats = (msg_with_punct, (msg_with_punct / n_messages) * 100, sum(sentences), (sum(sentences)/len(sentences)) * 100, avg_word_count)
    return stats


@graph('messages', _l('Message statistics'))
def message_stats(data):
    mess = data['messages']
    # mess = mess[(mess.sender == 'Wiktor Kania') & (mess.thread_type == 'Regular')].dropna()

    user_stats = {}

    messes = mess[(mess.thread_type == 'Regular') & (mess.sender != data['username'])].dropna()
    for conv, msgs in messes.groupby(messes.conversation):

        if msgs.content is not None and len(msgs.content) > 1:
            user_stats[conv] = get_messages_stats(msgs.content)

    df1 = [[], [], [], [], [], []]

    for k, v in user_stats.items():
        df1[0].append(k)
        for i, iv in enumerate(v, start=1):
            df1[i].append(iv)
    df = pd.DataFrame({'name': df1[0], "zn_int": df1[1],'% zn_int': df1[2], 'zd_wl': df1[3], '% zd_wl': df1[4], 'avg_word': df1[5]})
    df = df.round({'% zn_int': 2, '% zd_wl': 2, 'avg_word': 1})

    data['friends_stats_mean'] = df.mean()

    chart = pygal.HorizontalBar(style=style, legend_at_bottom=True)
    chart.x_labels = list(df.name)
    chart.add('% Zdań ze znakami interpunkcyjnymi', df['% zn_int'])
    chart.add('% Zdań zaczętych wielką literą', df['% zd_wl'])
    chart.add('Średnia liczba słów w wiadomości', df['avg_word'], secondary=True)
    return chart
