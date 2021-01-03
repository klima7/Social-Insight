from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Messages sent by year'))
def messages_sent_by_day_of_week(data):
    messages = data['messages']
    messages_for_year = messages.time.dt.year.value_counts().sort_index()
    percent_for_year = (messages_for_year / messages_for_year.sum() * 100).round(2)

    min_year = messages_for_year.index.min()-1
    max_year = messages_for_year.index.max()

    empty_series = pd.Series([0]*(max_year-min_year+1), list(range(min_year, max_year+1)))
    percent_for_year = percent_for_year.add(empty_series, fill_value=0)

    line_chart = pygal.Line(style=style, show_legend=False)
    line_chart.x_labels = percent_for_year.index
    line_chart.add('', percent_for_year)

    return line_chart
