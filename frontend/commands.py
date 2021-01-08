import pygal
import pandas

from flask import session
from flask_login import current_user
from config import config
from time import time_ns


def cache_suffix():
    if not config.CACHING_DISABLED:
        return ''
    return str(time_ns())


def get_current_user():
    return current_user


def is_pygal_chart(obj):
    return isinstance(obj, pygal.graph.graph.Graph)


def is_pandas_table(obj):
    return isinstance(obj, pandas.core.frame.DataFrame)


def translate_pandas_table(table):
    return table.rename(columns=str)


def is_dark_mode():
    return session.get('dark_mode', False)

