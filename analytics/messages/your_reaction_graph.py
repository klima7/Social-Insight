from .. import graph, emojistyle
from flask_babel import gettext as _l
import pygal
import emoji

@graph(_l('Your reactions'))
def your_reactions(data):
    reac = data['reactions']
    your_reac = reac[reac.giver == data['username']]
    your_reac = your_reac.groupby(your_reac.reaction).count().giver.sort_values(ascending=False)

    graph1 = pygal.Bar(showlegend=False, style=emojistyle)
    graph1.add('', list(your_reac))
    graph1.x_labels = list(your_reac.index)
    return graph1
