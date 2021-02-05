from .. import graph, using, style
from ..util import shorten_strings, calc_bar_chart_height
from flask_babel import gettext as _l
import pygal
import pandas as pd
import numpy as np


def determine_avg_reply_time(sample, my_username): # sample to tabela wiadomości. W zamyśle są tam wiadomości tylko 2 użytkowników. (time, sender required)
    if len(sample) > 0:
        senders = {k: v for v, k in enumerate(sample['sender'].unique())} # Słownik nazw użytkowników i ich unikalnych indeksów liczbowych.
        sample['sender2'] = sample['sender'].map(senders) # Zamiana nazwy użytkownika na unikalnego, bo nie można użyć diff'a na stringach.
        temp = sample['time'].diff(periods=-1) # Czas który upłynął od ostatniej wiadomości.
        sample['time2'] = temp
        sample = sample[(sample['sender2'][::-1].diff() != 0)[::-1]] # Usuwanie kilku wiadomości użytkownika pod rząd. (Nie może przecież odpowiedzieć sam
        conv_end_threshold = pd.Timedelta(hours=2)
        sample = sample[sample['time2'] <= conv_end_threshold] # Odrzucanie wartości które są początkami rozmów. (Długi czas upłynął od ostatniej wiadomości. Improve if know how.)
        sample = sample[sample['sender'] != my_username] # Interesuje nas jak szybko ta osoba odpowiada, ale można zamienić i dowiemy się jak szybko my jej odpowiadamy.
        return sample['time2'].median()
    return np.Nan


def create_chart(reply_times, limit=None):
    if limit is not None:
        reply_times = reply_times.tail(limit)

    height = calc_bar_chart_height(reply_times)
    gr = pygal.HorizontalBar(style=style, height=height)
    gr.add('', reply_times['time'].dt.seconds)
    gr.x_labels = shorten_strings(reply_times['user'])
    gr.human_readable = True
    gr.show_legend = False
    gr.print_values = True
    gr.print_values_position = 'top'
    gr.x_title = 'Reply time in seconds'
    gr.y_title = 'User'
    return gr


@graph(_l('Reply time by user'))
@using('messages', 'username')
def reply_time(data):
    messages = data['messages']
    reply_times = pd.DataFrame()
    convos = messages[messages['thread_type'] == 'Regular'].groupby('conversation')
    for user, msg in convos:
        t = pd.DataFrame({'user': [user], 'time': [determine_avg_reply_time(msg.loc[:, ('sender', 'time')], data['username'])]})
        reply_times = reply_times.append(t)

    reply_times = reply_times.dropna()  # Usuwa osoby które nigdy nie odpowiedziały :(
    reply_times = reply_times.sort_values(['time'], ascending=[0])

    return create_chart(reply_times, 35), create_chart(reply_times)
