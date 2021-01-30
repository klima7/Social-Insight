from .. import graph, using, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Number of reactions'))
@using('likes')
def number_of_reactions(data):
    like_table = data['likes']
    
    name_to_e = {
        'ANGER': '😡',
        'HAHA': '😂',
        'LIKE': '👍',
        'LOVE': '❤️',
        'SORRY': '😢',
        'WOW': '😯'
    }

    by_type = like_table.groupby(like_table.type).count().time
    indexes = [i + ' ' + name_to_e[i] for i in by_type.index]

    chart = pygal.Pie(style=style)
    for i, t in zip(indexes, list(by_type)):
        chart.add(i, t)

    return chart
