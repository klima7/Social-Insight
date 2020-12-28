import json
import re
import pandas as pd
import numpy as np
import emoji

import pygal
from flask_babel import lazy_gettext as _l

from . import style, emojistyle, graph


def get_structure(zip):
    folders = {}
    for i in zip.namelist():
        entry = i.split('/')
        last = entry[-1]
        outer = folders
        for j in entry:
            if j != '':
                if j != last and j not in outer:
                    outer[j] = {}
                if j == last:
                    if '__files' not in outer:
                        outer['__files'] = []
                    outer['__files'].append((j, i))
                if j != last:
                    outer = outer[j]
    return folders


def get_messages(folder):
    message_files = []
    for i in folder.keys():
        files = folder[i]['__files']
        for i in files:
            if re.match(r'.+\.json', i[0]):
                message_files.append(i[1])
    return message_files


def analyse_file(file):
    # stats = {}
    # js = json.loads(file)
    # people = {}
    # for i in js['messages']:
    #     sender = i['sender_name'].encode('latin1').decode('utf8')
    #     if sender not in people:
    #         people[sender] = 0
    #     people[sender] += 1
    # stats['message_count'] = people
    # return stats
    js = json.loads(file)
    # js = json.loads(file)

    constants = [js['title'].encode('latin1').decode('utf8'), js['thread_type']] # wartości które są stałe dla danego czatu, ale może są warte zamieszczenia w tabeli.

    entries = []

    for i in js['messages']:
        content = i.get('content')
        if content:
            content = content.encode('latin1').decode('utf8')
        entries.append([i['sender_name'].encode('latin1').decode('utf8'), i['timestamp_ms'], content])

    entries = np.array(entries)

    data = pd.DataFrame({'conversation': constants[0], 'thread_type': constants[1], 'sender': entries[:, 0], 'time': entries[:, 1], 'content': entries[:, 2]})
    data['time'] = pd.to_datetime(data['time'], unit='ms')

    return data


def gen_pandas_table(zip):
    messages_table = None

    folders = get_structure(zip)
    message_files = get_messages(folders['messages']['inbox'])

    for i in message_files:
        temp_file = zip.getinfo(i)
        # with io.TextIOWrapper(zip.open(temp_file), 'utf-8') as f: # Otwieranie pliku jako tekst, żeby można było odrazu zamienić escapowane znaki na właściwe.
        with zip.open(temp_file) as f:
            stats = analyse_file(f.read())
            if messages_table is None:
                messages_table = stats
            else:
                messages_table = pd.concat([messages_table, stats])

    namefile = folders['profile_information']['__files'][0][1]
    username = ""
    with zip.open(namefile) as f:
        data = json.loads(f.read())
        username = data['profile']['name']['full_name'].encode('latin1').decode('utf8')

    friends_fname = folders['friends']['__files'][0][1]
    
    friends_table = pd.DataFrame()
    with zip.open(friends_fname) as f:
        json_file = json.loads(f.read())
        
        names = []
        dates = []
        for i in json_file['friends']:
            names.append(i['name'].encode('latin1').decode('utf8'))
            dates.append(i['timestamp'])
        friends_table = pd.DataFrame({'name': names, 'date_added': dates})
        friends_table['date_added'] = pd.to_datetime(friends_table['date_added'], unit='s')

    return {'messages': messages_table, 'friends': friends_table, 'username': username}


@graph('messages', _l('Number of interchanged messages'))
def bar_chart(data):
    table = data['messages']

    regs = table[(table['thread_type'] == 'Regular') & (table['sender'] == data['username'])]
    group = regs.groupby('conversation')

    counts = group['content'].count().sort_values(ascending=False).head(15)

    chart = pygal.HorizontalBar(style=style, show_legend=False, height=len(list(counts.keys())*35))
    chart.x_labels = list(counts.keys()[::-1])
    chart.add('', counts.values[::-1])

    return chart


# Helper function for emoji ranking
def check_emojis(s):
    found = {}
    if s is None:
        return found
    for i in s:
        if i in emoji.UNICODE_EMOJI:
            if i in found:
                found[i] += 1
            else:
                found[i] = 1
    return found


@graph('messages', _l('The most frequent used emoji'))
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

    counter = 0
    for k, v in sorted(all_emojis.items(), key=lambda i: i[1], reverse=True):
        emoji_v.append(v)
        emoji_l.append(k)
        counter += 1
        if counter >= 15:
            break

    chart = pygal.Bar(style=emojistyle, show_legend=False, height=600)
    chart.add('', emoji_v)
    chart.x_labels = emoji_l
    return chart


def determine_avg_reply_time(sample, my_username): # sample to tabela wiadomości. W zamyśle są tam wiadomości tylko 2 użytkowników. (time, sender required)
    if len(sample) > 0:
        print(sample.index)
        senders = {k: v for v, k in enumerate(sample['sender'].unique())} # Słownik nazw użytkowników i ich unikalnych indeksów liczbowych.
        sample['sender2'] = sample['sender'].map(senders) # Zamiana nazwy użytkownika na unikalnego, bo nie można użyć diff'a na stringach.
        # sample['sender2_test'] = sample['sender2'][::-1].diff() # Można usunąć (debug purposes)
        temp = sample['time'][::-1].diff() # Czas który upłynął od ostatniej wiadomości.
        print(sample.index)
        sample['time2'] = temp
        sample = sample[(sample['sender2'][::-1].diff() != 0)[::-1]] # Usuwanie kilku wiadomości użytkownika pod rząd. (Nie może przecież odpowiedzieć sam
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


# @graph('messages', _l('Average messages in conversation'))
def conversation_length(data): # Skopiowane reply_time, więc nazwy zmiennych nie mają sensu
    messages = data['messages']
    reply_times = pd.DataFrame();
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


# wykres liczby znajomych 2
@graph('other', _l('Friends count'))
def friends_cumsum(data):
    frens = data['friends']
    a = frens.groupby([frens.date_added.dt.year, frens.date_added.dt.dayofyear])
    t = pd.date_range(frens.date_added.min(), frens.date_added.max())

    t = pd.Series(t.date)
    days_with_frens = t.isin(frens.date_added.dt.date)
    days_with_frens = ~days_with_frens
    # Dodawanie '-1', jako nazwy użytkownika, ponieważ pandas nie grupuje wartości None/np.nan
    frens2 = pd.concat([frens, pd.DataFrame({'date_added': t[days_with_frens], 'name': ['-1'] * len(t[days_with_frens])})])
    frens2 = frens2.sort_values(['date_added']).reset_index(drop=True)
    frens2['date_added'] = pd.to_datetime(frens2['date_added'])

    grouped = None

    timespan = frens.date_added.max() - frens.date_added.min()
    time_index = []

    # Grupowanie przedziałów zliczania liczby znajomych, w zależności od tego jak stare jest konto
    if timespan.days > 360 * 10:
        distance = 'Y'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.year])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='Y')
    elif timespan.days > 360 * 2:
        distance = 'QS'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.quarter])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='QS')
    elif timespan.days > 40:
        distance = 'W'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.isocalendar().week])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='W')
    elif timespan.days > 90:
        distance = 'M'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.month])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='M')
    else:
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.day])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='D')

    # zliczanie elementów które nie są '-1'
    b = grouped['name'].agg(lambda x: len(x[x != '-1']))

    # cum sumowanie
    b = b.cumsum()

    chart = pygal.Line(x_label_rotation=-45, fill=True)
    time_index = list(map(lambda a: "{}/{}/{}".format(a.year, a.month, a.day), time_index))

    if len(b) > len(time_index):
        last_day = frens.date_added.max()
        time_index.append("{}/{}/{}".format(last_day.year, last_day.month, last_day.day))
        
    chart.x_labels = time_index
    chart.add('', b.to_list(), dots_size=0)

    return chart


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
    chart = pygal.Pie(style=style)
    for k, v in messages_to.items():
        chart.add(k, v)

    return chart
