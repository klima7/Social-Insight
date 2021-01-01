from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd
import numpy as np


def determine_avg_reply_time(sample, my_username): # sample to tabela wiadomości. W zamyśle są tam wiadomości tylko 2 użytkowników. (time, sender required)
    if len(sample) > 0:
        senders = {k: v for v, k in enumerate(sample['sender'].unique())} # Słownik nazw użytkowników i ich unikalnych indeksów liczbowych.
        sample['sender2'] = sample['sender'].map(senders) # Zamiana nazwy użytkownika na unikalnego, bo nie można użyć diff'a na stringach.
        # sample['sender2_test'] = sample['sender2'][::-1].diff() # Można usunąć (debug purposes)
        sample['time2'] = sample['time'][::-1].diff() # Czas który upłynął od ostatniej wiadomości.
        sample = sample[ (sample['sender2'][::-1].diff() != 0)[::-1]] # Usuwanie kilku wiadomości użytkownika pod rząd. (Nie może przecież odpowiedzieć sam
        # sample.to_csv("dump.csv")
        # sample[:50]
        conv_end_threshold = pd.Timedelta(hours=2)
        sample = sample[sample['time2'] <= conv_end_threshold] # Odrzucanie wartości które są początkami rozmów. (Długi czas upłynął od ostatniej wiadomości. Improve if know how.)
        # sample = sample[sample['sender'] != data['username']] # Interesuje nas jak szybko ta osoba odpowiada, ale można zamienić i dowiemy się jak szybko my jej odpowiadamy.know how.)
        sample = sample[sample['sender'] != my_username] # Interesuje nas jak szybko ta osoba odpowiada, ale można zamienić i dowiemy się jak szybko my jej odpowiadamy.
        # sample['time2'].median(), sample['time2'].std(), sample['time2'].mean() # W sample['time2'] mogą nadal być duże wartości (w moich danych obok średnio 24s na odpowiedź, znalazł się czas 8h), ale wydaje mi się, że median zwraca wiarygodny wynik.
        return sample['time2'].median()
    return np.Nan


# UWAGA!!!!
# Nie działa jak jest więcej niż jeden użytkownik o takiej samej nazwie. (Najczęściej ktoś zbanowany o nazwie Użytkownik Facebooka)
# To jest do poprawienia w funkcji wczytującej. Ale nie chciało mi się tego dzisiaj już robić
# Określanie czasu odpowiedzi nie jest dokładne, zwłaszcza jeżeli w konwersacji jest mało wiadomości.
# I przez to zdarza się, że jedna osoba ma 1000x większy słupek na wykresie. (Można spróbować wykres log?¿?¿?¿¿??)
@graph(_l('Reply time by user'))
def reply_time(data):
    messages = data['messages']
    reply_times = pd.DataFrame();
    convos = messages[messages['thread_type'] == 'Regular'].groupby('conversation')
    for user, msg in convos:
        t = pd.DataFrame({'user': [user], 'time': [determine_avg_reply_time(msg.loc[:, ('sender', 'time')], data['username'])]})
    #     print(t)
        reply_times = reply_times.append(t)

    reply_times = reply_times.dropna() # Usuwa osoby które nigdy nie odpowiedziały :(
    reply_times = reply_times.sort_values(['time'], ascending=[0])

    gr = pygal.HorizontalBar(style=style)
    gr.add('', reply_times['time'].astype('int') / 1e9)
    gr.x_labels = list(reply_times['user'])
    gr.human_readable = True
    gr.show_legend = False
    gr.print_values = True
    gr.print_values_position = 'top'

    return gr
