from .. import graph, emojistyle
from flask_babel import gettext as _l
import pygal
import emoji

MAX_EMOJI_COUNT = 20


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


@graph(_l('Your emoji ranking'))
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
        if counter >= MAX_EMOJI_COUNT:
            break

    chart = pygal.Bar(style=emojistyle, show_legend=False, height=len(emoji_l)*20)
    chart.add('', emoji_v)
    chart.x_labels = emoji_l
    chart.x_title = 'Emoji'
    chart.y_title = 'Occurrence count'
    return chart
