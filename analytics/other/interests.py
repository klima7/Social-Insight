from .. import graph, using
from flask_babel import gettext as _l


@graph(_l('Things you are interested in according to Facebook'))
@using('topics')
def time_to_post(data):
    topics = data['topics']
    return topics

