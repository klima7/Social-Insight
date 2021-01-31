import re
import json
import pandas as pd
from . import preprocessor

def _aux_get_messages_filenames(folder):
    message_files = []
    for i in folder.keys():
        files = folder[i]['__files']
        for file in files:
            if re.match(r'.+\.json', file[0]):
                message_files.append(file[1])
    return message_files


def _aux_analyse_messages_file(file):
    js = json.loads(file)

    # wartości które są stałe dla danego czatu, ale może są warte zamieszczenia w tabeli.
    constants = [js['title'].encode('latin1').decode('utf8'), js['thread_type']]

    entries = [[], [], [], []]
    react_list = [[], [], [], [], []]   # giver, receiver, time, conversation, reaction

    for i in js['messages']:
        content = i.get('content')
        photos = 0
        if content:
            content = content.encode('latin1').decode('utf8')
        if 'reactions' in i:
            for r in i['reactions']:
                react_list[4].append(r['reaction'].encode('latin1').decode('utf8'))
                react_list[0].append(r['actor'])
                react_list[2].append(i['timestamp_ms'])
                react_list[1].append(i['sender_name'])
                react_list[3].append(constants[0])
        if 'photos' in i:
            photos = len(i['photos'])

        # entries.append([, , content, ])
        entries[0].append(i['sender_name'].encode('latin1').decode('utf8'))
        entries[1].append(i['timestamp_ms'])
        entries[2].append(content)
        entries[3].append(photos)

    # entries = np.array(entries)

    data = pd.DataFrame(
        {
            'conversation': constants[0],
            'thread_type': constants[1],
            'sender': entries[0],
            'time': entries[1],
            'content': entries[2],
            'photos': entries[3]
        }
    )

    data['time'] = pd.to_datetime(data['time'], unit='ms')
    reactions = pd.DataFrame({'giver': react_list[0], 'reciver': react_list[1], 'time': react_list[2], 'conversation': react_list[3], 'reaction': react_list[4], })
    reactions.time = pd.to_datetime(reactions.time, unit='ms')

    return data, reactions


@preprocessor('messages', 'reactions')
def get_messages_and_reactions_table(zip_file, folders):
    messages_table = None
    reactions_table = None

    message_files = _aux_get_messages_filenames(folders['messages']['inbox'])

    for i in message_files:
        temp_file = zip_file.getinfo(i)
        # with io.TextIOWrapper(zip.open(temp_file), 'utf-8') as f: # Otwieranie pliku jako tekst, żeby można było odrazu zamienić escapowane znaki na właściwe.
        with zip_file.open(temp_file) as f:
            stats, react_stats = _aux_analyse_messages_file(f.read())
            if messages_table is None:
                messages_table = stats
                reactions_table = react_stats
            else:
                messages_table = pd.concat([messages_table, stats])
                reactions_table = pd.concat([reactions_table, react_stats])

    reactions_table.reciver = reactions_table.reciver.transform(lambda text: text.encode('latin1').decode('utf8'))
    reactions_table.giver = reactions_table.giver.transform(lambda text: text.encode('latin1').decode('utf8'))

    return messages_table, reactions_table
