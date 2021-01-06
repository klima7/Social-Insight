import pandas as pd
import numpy as np
import json
import re
import user_agents


# Funkcja preprocess ma wydobywać z pliku zip wszystkie istotne dane, które mogą się przypadać w wykresach.
# To co zwróci ta funkcja jest przekazywane jako parametr do wszystkich funkcji generujących wykresy.
# W razie potrzeby wydobycia z pliku zip jakiś nowych danych należy zmodyfikować ten plik .py
def preprocess(zip_file):
    folders = _aux_get_structure(zip_file)

    messages, reactions = _get_messages_and_reactions_table(zip_file, folders)
    friends = _get_friends_table(zip_file, folders)
    username = _get_username(zip_file, folders)
    account_activity = _get_acc_activity_table(zip_file, folders)
    off_facebook_activity = _get_off_facebook_activity_table(zip_file, folders)

    return {
        'messages': messages,
        'reactions': reactions,
        'friends': friends,
        'username': username,
        'account_activity': account_activity,
        'off_facebook_activity': off_facebook_activity
    }


def _aux_get_structure(zip_file):
    folders = {}
    for i in zip_file.namelist():
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

    entries = []
    react_list = [[], [], [], [], []]   # giver, receiver, time, conversation, reaction

    for i in js['messages']:
        content = i.get('content')
        if content:
            content = content.encode('latin1').decode('utf8')
        if 'reactions' in i:
            for r in i['reactions']:
                react_list[4].append(r['reaction'].encode('latin1').decode('utf8'))
                react_list[0].append(r['actor'])
                react_list[2].append(i['timestamp_ms'])
                react_list[1].append(i['sender_name'])
                react_list[3].append(constants[0])
        entries.append([i['sender_name'].encode('latin1').decode('utf8'), i['timestamp_ms'], content])

    entries = np.array(entries)

    data = pd.DataFrame({'conversation': constants[0], 'thread_type': constants[1], 'sender': entries[:, 0], 'time': entries[:, 1], 'content': entries[:, 2]})
    data['time'] = pd.to_datetime(data['time'], unit='ms')
    reactions = pd.DataFrame({'giver': react_list[0], 'reciver': react_list[1], 'time': react_list[2], 'conversation': react_list[3], 'reaction': react_list[4], })
    reactions.time = pd.to_datetime(reactions.time, unit='ms')

    return data, reactions


def _get_messages_and_reactions_table(zip_file, folders):
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


def _get_friends_table(zip_file, folders):
    friends_file_name = folders['friends']['__files'][0][1]

    with zip_file.open(friends_file_name) as f:
        json_file = json.loads(f.read())

        names = []
        dates = []
        for i in json_file['friends']:
            names.append(i['name'].encode('latin1').decode('utf8'))
            dates.append(i['timestamp'])
        friends_table = pd.DataFrame({'name': names, 'date_added': dates})
        friends_table['date_added'] = pd.to_datetime(friends_table['date_added'], unit='s')

    return friends_table


def _get_username(zip_file, folders):
    name_file = folders['profile_information']['__files'][0][1]
    with zip_file.open(name_file) as f:
        data = json.loads(f.read())
        username = data['profile']['name']['full_name'].encode('latin1').decode('utf8')
    return username


def _aux_get_device_os_browser(t):
    t = user_agents.parse(t)
    dev = str(t.device.brand) + ' ' + str(t.device.model)
    if t.device.brand is None and t.device.model is None:
        if t.is_pc:
            dev = 'PC'
        else:
            dev = 'Other'
    return dev, str(t.os.family), t.browser.family


def _get_acc_activity_table(zip_file, folders):
    acc_activity_path = None
    for i in folders['security_and_login_information']['__files']:
        if i[0] == 'account_activity.json':
            acc_activity_path = i[1]
            break

    with zip_file.open(acc_activity_path) as f:
        actions = []
        times = []
        devices = []
        oss = []
        browsers = []
        json_data = json.loads(f.read())
        for j in json_data['account_activity']:
            actions.append(j['action'])
            device, os, browser = _aux_get_device_os_browser(j['user_agent'])

            devices.append(device)
            oss.append(os)
            browsers.append(browser)
            times.append(j['timestamp'])

        acc_activity = pd.DataFrame({'time': times, 'device': devices, 'os': oss, 'browser': browsers, 'action': actions})
        acc_activity.time = pd.to_datetime(acc_activity.time, unit='s')
    return acc_activity


def _get_off_facebook_activity_table(zip_file, folders):
    json_filename = None
    for name in folders['ads_and_businesses']['__files']:
        if name[0] == 'your_off-facebook_activity.json':
            json_filename = name[1]
            break

    if json_filename:
        names = []
        types = []
        times = []
        with zip_file.open(json_filename) as f:
            json_data = json.loads(f.read())
            for act in json_data['off_facebook_activity']:
                name = act['name']
                for i in act['events']:
                    names.append(name)
                    types.append(i['type'])
                    times.append(i['timestamp'])
        table = pd.DataFrame({'name': names, 'type': types, 'time': times})
        table.time = pd.to_datetime(table.time, unit='s')
        return table
