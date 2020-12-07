import json
import re
import zipfile as zp
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

    return {'table': messages_table, 'username': username}

@graph('messages', _l('The people you write with most frequent'))
def bar_chart(data):
    table = data['table']
    print(table.head())
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
    table = data['table']
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
#     print( all_emojis[:])
    return chart