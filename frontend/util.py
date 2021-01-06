import pygal
import pandas

from flask import flash, session
from flask_login import current_user
from config import config
from time import time_ns
import os
import tempfile
import base64


def cache_suffix():
    if not config.CACHING_DISABLED:
        return ''
    return str(time_ns())


def display_errors_with_flash(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            flash(err, 'error')


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


def scale_graph(graph, factor):
    graph.config.width *= factor
    graph.config.height *= factor
    graph.config.style.label_font_size *= factor
    graph.config.style.major_label_font_size *= factor
    graph.config.style.value_font_size *= factor
    graph.config.style.value_label_font_size *= factor
    graph.config.style.tooltip_font_size *= factor
    graph.config.style.title_font_size *= factor
    graph.config.style.legend_font_size *= factor
    graph.config.style.no_data_font_size *= factor


def render_graph_png_inline(graph):
    factor = 1
    scale_graph(graph, factor)

    path = os.path.join(tempfile.mkdtemp(), 'graph.png')
    graph.render_to_png(path)
    encoded = base64.b64encode(open(path, "rb").read())

    scale_graph(graph, 1/factor)
    return "data:image/png;base64," + encoded.decode()
