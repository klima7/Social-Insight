from .. import graph, using
from flask_babel import gettext as _l
import pandas as pd


def create_chart(df, limit=None):
    if limit is not None:
        df = df.tail(limit)
    return df


@graph(_l('Most frequently searched phrases'))
@using('search_history')
def time_to_post(data):
    history = data['search_history']
    if history is None:
        return None
       
    history.message.value_counts()
    counts = history.message.value_counts()
    table = pd.DataFrame({'searched phrase': counts.index, 'count': counts})
    return create_chart(table, 10), create_chart(table)

