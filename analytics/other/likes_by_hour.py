from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd

@graph(_l('Percent of likes by hour'))
def time_to_post(data):
    post_data = data['likes']
    total_posts_n = len(post_data)

    posts_in_hour = post_data.groupby(post_data.time.dt.hour)
    posts_in_hour = dict(posts_in_hour.count().time)
    index = range(24)
    values = [(posts_in_hour[i] / total_posts_n) * 100 if i in posts_in_hour else 0 for i in index]

    radar_chart = pygal.Radar(style=style, show_legend=False, fill=True, height=800)
    radar_chart.x_labels = index
    radar_chart.add('', values)

    return radar_chart

