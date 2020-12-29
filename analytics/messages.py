# import json
# import re
# import zipfile as zp
import pandas as pd
import numpy as np
import emoji

import pygal
from flask_babel import lazy_gettext as _l

from . import style, emojistyle, graph

@graph('messages', _l('The people you write with most frequent'))
def your_best_friends(data):
    table = data['messages']
    #print(table.head())
    regs = table[(table['thread_type'] == 'Regular') & (table['sender'] == data['username'])]
    group = regs.groupby('conversation')

    counts = group['content'].count().sort_values(ascending=False)

    chart = pygal.HorizontalBar(style=style, show_legend=False, height=len(list(counts.keys())*20))
    chart.x_labels = list(counts.keys()[::-1])
    chart.add('', counts.values[::-1])

    return chart


# Helper function for emoji ranking
def check_emojis(s):
    found = {}
    if s == None:
        return found
    for i in s:
        if i in emoji.UNICODE_EMOJI:
            if i in found:
                found[i] += 1
            else:
                found[i] = 1
    return found


@graph('messages', _l('Your emoji ranking'))
def emoji_ranking(data):
    table = data['messages']
    my_name = data['username']
    msgs = table[table['sender'] == my_name]['content']
    
    all_emojis = {}
    for i in msgs:
        emojis = check_emojis(i)
        for j in emojis:
            if j in all_emojis:
                all_emojis[j] += 1
            else:
                all_emojis[j] = 1
    emoji_v = []
    emoji_l = []
    for k, v in sorted(all_emojis.items(), key=lambda i: i[1], reverse=True):
        emoji_v.append(v)
        emoji_l.append(k)
                             
    
    chart = pygal.Bar(style=emojistyle, show_legend=False, height=len(emoji_l)*20)
    chart.add('', emoji_v)
    chart.x_labels =  emoji_l
    return chart


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
@graph('messages', _l('Reply time by user'))
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
    # sample.to_csv("dump.csv")

    # indeks końca ostatniej rozmowy to -1
    conversation_begs.insert(0, -1)
    # indeks początku pierwszej rozmowy to len()-1
    conversation_begs.insert(len(conversation_begs), len(sample) - 1)
    conversation_begs
    conversation_lens = [ conversation_begs[i] - conversation_begs[i - 1] for i in range(1, len(conversation_begs)) ]
    return np.array(conversation_lens).mean()


@graph('messages', _l('Average messages in conversation'))
def conversation_length(data): # Skopiowane reply_time, więc nazwy zmiennych nie mają sensu
    messages = data['messages']
    reply_times = pd.DataFrame();
    convos = messages[messages['thread_type'] == 'Regular'].groupby('conversation')
    for user, msg in convos:
        t = pd.DataFrame({'user': [user], 'time': [determine_conversation_length(msg.loc[:, ('sender', 'time')], data['username'])]})
    #     print(t)
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


@graph('messages', _l('Example table'))
def example_table(data):
    s1 = pd.Series([1, 2, 3, 4, 5])
    s2 = pd.Series(['Ala', 'ma', 'kota', 'foo', 'bar'])
    f1 = pd.DataFrame({_l('header 1'): s1, _l('header 2'): s2, _l('header 3'): s1})
    return f1


# Działa w polsce, 
@graph('messages', _l('Messages sent by sex'))
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
    chart = pygal.Pie()
    for k, v in messages_to.items():
        chart.add(k, v)

    return chart