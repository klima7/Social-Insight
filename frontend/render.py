import os
import tempfile
import base64
import pygal
import pandas as pd
import zipfile
import frontend.common as common

import flask
import imgkit
import pdfkit

from config import config


def render_graph_png_inline(graph):
    factor = 1
    scale_graph(graph, factor)

    path = os.path.join(tempfile.mkdtemp(), 'graph.png')
    graph.render_to_png(path)
    encoded = base64.b64encode(open(path, "rb").read())

    scale_graph(graph, 1/factor)
    return "data:image/png;base64," + encoded.decode()


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


def render_container_pdf(container, path, style):
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


def render_graph_png(graph, path, scale=1):
    scale_graph(graph, scale)
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


def render_chart_png(chart, path):
    if isinstance(chart.data, pygal.graph.graph.Graph):
        render_graph_png(chart.data, path, scale=1)
    elif isinstance(chart.data, pd.core.frame.DataFrame):
        render_table_png(chart.data, path)


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

        graph.render_png(png_path)

    common.zipdir(directory, path)


