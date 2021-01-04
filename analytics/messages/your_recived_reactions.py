from .. import graph, emojistyle
from flask_babel import gettext as _l
import pygal
import emoji


@graph(_l('Reactions given to you'))
def reacived_reactions(data):
    reac = data['reactions']
    your_recived_reac = reac[reac.reciver == data['username']]
    your_recived_reac = your_recived_reac.groupby(your_recived_reac.reaction).count().giver.sort_values(ascending=False)

    graph1 = pygal.Bar(show_legend=False, style=emojistyle)
    graph1.add('', list(your_recived_reac))
    graph1.x_labels = list(your_recived_reac.index)
    graph1.x_title = 'Emoji'
    graph1.y_title = 'Occurrence count'
    return graph1
