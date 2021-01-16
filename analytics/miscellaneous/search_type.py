from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


MAX_COUNT = 10


@graph(_l('Types of most frequently searched elements'))
def time_to_post(data):
    history = data['search_history']
    if history is None:
        return None
        
    types = history.type.value_counts()
    table = pd.DataFrame({'Search type': types.index, 'Count': types})
    table = table.head(MAX_COUNT)

    return table

