from .. import graph, using
from flask_babel import gettext as _l
import pandas as pd


MAX_COUNT = 10


@graph(_l('Most frequently searched phrases'))
@using('search_history')
def time_to_post(data):
    history = data['search_history']
    if history is None:
        return None
       
    history.message.value_counts()
    counts = history.message.value_counts()
    table = pd.DataFrame({'searched phrase': counts.index, 'count': counts})
    table = table.head(MAX_COUNT)

    return table

