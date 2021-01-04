from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
import numpy as np


MAX_PEOPLE = 35


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


@graph(_l('Reply time by user'))
def reply_time(data):
    messages = data['messages']
    reply_times = pd.DataFrame()
    convos = messages[messages['thread_type'] == 'Regular'].groupby('conversation')
    for user, msg in convos:
        t = pd.DataFrame({'user': [user], 'time': [determine_avg_reply_time(msg.loc[:, ('sender', 'time')], data['username'])]})
        reply_times = reply_times.append(t)

    reply_times = reply_times.dropna()  # Usuwa osoby które nigdy nie odpowiedziały :(
    reply_times = reply_times.sort_values(['time'], ascending=[0])

    # Odfiltrowanie użytkowników o zbyt długich nazwach
    reply_times = reply_times.loc[reply_times.user.str.len() <= 25]



    height = len(reply_times.user)*25
    gr = pygal.HorizontalBar(style=style, height=height)
    gr.add('', reply_times['time'].dt.seconds)
    gr.x_labels = list(reply_times['user'])
    gr.human_readable = True
    gr.show_legend = False
    gr.print_values = True
    gr.print_values_position = 'top'
    gr.x_title = 'Reply time in seconds'
    gr.y_title = 'User'

    return gr
