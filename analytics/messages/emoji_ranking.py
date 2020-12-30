from .. import graph, emojistyle
from flask_babel import gettext as _l
import pygal
import emoji


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
    chart.x_labels = emoji_l
    return chart
