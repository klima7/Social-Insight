from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


@graph(_l('Things you are interested in according to Facebook'))
def time_to_post(data):
    topics = data['topics']
    return topics

