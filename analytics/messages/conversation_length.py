from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
import numpy as np


def determine_conversation_length(sample, my_username): # sample to tabela wiadomości. W zamyśle są tam wiadomości tylko 2 użytkowników. (time, sender required)
    # Słownik nazw użytkowników i ich unikalnych indeksów liczbowych.
    senders = {k: v for v, k in enumerate(sample['sender'].unique())}

    # Zamiana nazwy użytkownika na unikalnego, bo nie można użyć diff'a na stringach.
    sample['sender2'] = sample['sender'].map(senders)

    # sample['sender2_test'] = sample['sender2'][::-1].diff() # Można usunąć (debug purposes)
    sample['time2'] = sample['time'][::-1].diff() # Czas który upłynął od ostatniej wiadomości.

    # Usuwanie kilku wiadomości użytkownika pod rząd. (Nie może przecież odpowiedzieć sam sobie)
    # sample = sample[ (sample['sender2'][::-1].diff() != 0)[::-1]]
    # sample[:50]

    conv_end_threshold = pd.Timedelta(hours=2)
    # Odrzucanie wartości które są początkami rozmów. (Długi czas upłynął od ostatniej wiadomości. Improve if know how.)
    sample['conversation_start'] = sample['time2'] > conv_end_threshold

    conversation_begs = sample.index[sample['time2'] > conv_end_threshold].tolist()

    # indeks końca ostatniej rozmowy to -1
    conversation_begs.insert(0, -1)
    # indeks początku pierwszej rozmowy to len()-1
    conversation_begs.insert(len(conversation_begs), len(sample) - 1)
    conversation_begs
    conversation_lens = [ conversation_begs[i] - conversation_begs[i - 1] for i in range(1, len(conversation_begs)) ]
    return np.array(conversation_lens).mean()


@graph(_l('Average messages in conversation'))
def conversation_length(data): # Skopiowane reply_time, więc nazwy zmiennych nie mają sensu
    messages = data['messages']
    reply_times = pd.DataFrame()
    convos = messages[messages['thread_type'] == 'Regular'].groupby('conversation')
    for user, msg in convos:
        t = pd.DataFrame({'user': [user], 'time': [determine_conversation_length(msg.loc[:, ('sender', 'time')], data['username'])]})
        reply_times = reply_times.append(t)

    reply_times = reply_times.dropna() # Usuwa osoby które nigdy nie odpowiedziały :(
    reply_times = reply_times.sort_values(['time'])

    gr = pygal.HorizontalBar(style=style)
    gr.add('', reply_times['time'])
    gr.x_labels = list(reply_times['user'])
    gr.human_readable = True
    gr.show_legend = False
    gr.print_values = True
    gr.print_values_position = 'top'

    return gr
