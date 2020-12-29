import json
import re
import zipfile as zp
import pandas as pd
import numpy as np
import user_agents

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

def format_user_agent(t):
    t = user_agents.parse(t)
    dev = str(t.device.brand) + ' ' + str(t.device.model)
    if t.device.brand == None and t.device.model == None:
        if t.is_pc:
            dev = 'PC'
        else:
            dev = 'Other'
    # t.os.family, t.browser.family, dev
    return  dev + ' / ' + str(t.os.family) + ' / ' + t.browser.family

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
        
    acc_activity = None
    acc_activity_path = None
    for i in folders['security_and_login_information']['__files']:
        if i[0] == 'account_activity.json':
            acc_activity_path = i[1]
            break
            
    with zip.open(acc_activity_path) as f:
        actions = []
        times = []
        agents = []
        jdata = json.loads(f.read())
        for j in jdata['account_activity']:
#             print(j['action'] + ", " + j['user_agent'])
            actions.append(j['action'])
            parsed_agent = format_user_agent(j['user_agent'])
#             parsed_agent = str(user_agents.parse(j['user_agent']))
#             print(j['user_agent'])
#             if 'Facebook' in parsed_agent:
#                 parsed_agent = re.sub('Facebook.*', 'Facebook', parsed_agent)
                
            agents.append(str(parsed_agent))
            times.append(j['timestamp'])
            
        acc_activity = pd.DataFrame({'time': times, 'agent': agents, 'action': actions})
        acc_activity.time = pd.to_datetime(acc_activity.time, unit='s')

    return {'messages': messages_table, 'friends': friends_table, 'username': username, 'account_activity': acc_activity}

