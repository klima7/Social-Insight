import os
import tempfile
import base64
import pygal
import pandas as pd
import shutil
import frontend.common as common

import flask
import imgkit
import pdfkit
import demoji

from config import config


SCALE = 2


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


def demojify_graph(graph):
    if not isinstance(graph, pygal.Bar):
        return

    if hasattr(graph, 'x_labels'):
        graph.x_labels = map(demoji.replace, graph.x_labels)

    if hasattr(graph, 'y_labels'):
        graph.y_labels = map(demoji.replace, graph.y_labels)


def render_graph_png(graph, path, scale=1):
    scale_graph(graph, scale)
    demojify_graph(graph)
    graph.render_to_png(path)
    scale_graph(graph, 1/scale)


def render_table_png(df, path):
    html = flask.render_template('helper/table.html', table=df)
    css = 'frontend/static/css/pdf/print.css'
    configuration = imgkit.config(wkhtmltoimage=config.WKHTMLTOIMAGE_PATH)
    options = {
        'format': 'png',
        'width': 600,
        'encoding': "UTF-8",
        'quiet': ''
    }
    imgkit.from_string(html, path, options=options, css=[css], config=configuration)


def render_chart_png(data, path):
    try:
        if isinstance(data, pygal.graph.graph.Graph):
            render_graph_png(data, path, scale=SCALE)
        elif isinstance(data, pd.core.frame.DataFrame):
            render_table_png(data, path)
        else:
            raise MemoryError()
    except MemoryError:
        shutil.copyfile('frontend/static/images/emoji_error.png', path)


def render_chart_png_inline(data):
    path = os.path.join(tempfile.mkdtemp(), 'graph.png')
    render_chart_png(data, path)
    encoded = base64.b64encode(open(path, "rb").read())
    return "data:image/png;base64," + encoded.decode()


def render_pdf(container, path, style):
    html = flask.render_template('pdf.html', container=container)
    css = f'frontend/static/css/pdf/{style}.css'
    configuration = pdfkit.configuration(wkhtmltopdf=config.WKHTMLTOPDF_PATH)
    options = {
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'no-outline': None,
        'quiet': ''
    }

    pdf_data = pdfkit.from_string(html, False, options=options, css=[css], configuration=configuration)

    file = open(path, 'wb')
    file.write(pdf_data)
    file.close()


def render_zip(container, path, categories=False):
    directory = tempfile.mkdtemp()

    for graph in container.graphs:
        png_name = str(graph.get_name()) + ".png"
        if categories:
            category_dir = os.path.join(directory, graph.category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            png_path = os.path.join(category_dir, png_name)
        else:
            png_path = os.path.join(directory, png_name)

        render_chart_png(graph.data, png_path)

    common.zipdir(directory, path)


