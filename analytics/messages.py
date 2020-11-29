import pygal
import re
import json
from db import *
from . import style, analyser


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
    stats = {}
    js = json.loads(file)
    people = {}
    for i in js['messages']:
        sender = i['sender_name'].encode('latin1').decode('utf8')
        if sender not in people:
            people[sender] = 0
        people[sender] += 1
    stats['message_count'] = people
    return stats


@analyser(GraphNames.PEOPLE_MOST_WRITE)
def bar_chart(zip):
    print('start bar')
    folders = get_structure(zip)

    message_files = get_messages(folders['messages']['inbox'])
    print(message_files)
    total_message_count = {}

    for i in message_files:
        temp_file = zip.getinfo(i)
        with zip.open(temp_file) as f:
            stats = analyse_file(f.read())
            for j in stats['message_count'].keys():
                if j not in total_message_count:
                    total_message_count[j] = stats['message_count'][j]
                else:
                    total_message_count[j] += stats['message_count'][j]

    labels = []
    values = []

    for k, v in sorted(total_message_count.items(), key=lambda item: item[1]):
        if len(k) > 30:
            continue

        labels.append(k)
        values.append(v)

    if len(labels) > 20:
        labels = labels[-20:]
        values = values[-20:]

    bar_chart = pygal.HorizontalBar(style=style, show_legend=False, height=len(labels)*20)
    bar_chart.x_labels = list(labels)
    bar_chart.add('', values)
    print('end bar')
    return bar_chart


@analyser(GraphNames.EXAMPLE_PIE_CHART)
def pie_chart(zip):
    pie_chart = pygal.Pie(legend_at_bottom=True, style=style)
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    return pie_chart


@analyser(GraphNames.EXAMPLE_BAR_CHART)
def bar_chart(zip):
    bar_chart = pygal.Bar(legend_at_bottom=True, style=style)
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 34, 21, 13, 8, 5, 3, 2, 1, 1, 0])
    return bar_chart


@analyser(GraphNames.EXAMPLE_LINE_CHART)
def line_chart(zip):
    line_chart = pygal.Line(legend_at_bottom=True, style=style)
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    return line_chart


@analyser(GraphNames.EXAMPLE_RADAR_CHART)
def radar_chart(zip):
    radar_chart = pygal.Radar(legend_at_bottom=True, style=style)
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                            'NavierStokes']
    radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    return radar_chart
