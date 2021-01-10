from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd

@graph(_l('Number of comments by year'))
def device_usage(data):
    post_data = data['comments']
    posts_by_year = post_data.groupby(post_data.time.dt.year).count()
    year_values = list(posts_by_year.time)
    year_indexes = list(posts_by_year.index)

    if len(posts_by_year) == 1:
        year_values = [0] + year_values
        year_indexes = [year_indexes[0] - 1] + year_indexes

    chart = pygal.Line(style=style, show_legend=False)
    chart.x_labels = year_indexes
    chart.add('', year_values)

    return chart