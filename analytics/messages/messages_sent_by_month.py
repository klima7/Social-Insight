from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Messages sent by month'))
def messages_sent_by_day_of_week(data): #
    messages = data['messages']
    messages_for_month = messages.time.dt.month.value_counts().sort_index()
    percent_for_month = messages_for_month / messages_for_month.sum() * 100

    empty_series = pd.Series([0]*12, list(range(1, 13)))
    percent_for_month = percent_for_month.add(empty_series, fill_value=0).round(1)

    bar_chart = pygal.Bar(style=style, show_legend=False)
    bar_chart.add('', percent_for_month)
    bar_chart.x_labels = percent_for_month.index
    bar_chart.y_title = 'Month number'
    bar_chart.x_title = 'Percent of sent messages'

    return bar_chart