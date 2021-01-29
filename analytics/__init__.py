from pygal.style import Style
from db import *
import analytics.preprocess as preprocess
import zipfile as zp
from collections import namedtuple
import traceback
import os
import pkgutil

style = Style(
  background='white',
  plot_background='white',
  transition='400ms ease-in',
  legend_font_size=20)

emojistyle = Style(
  background='white',
  plot_background='white',
  transition='400ms ease-in',
  legend_font_size=20,
  label_font_size=30,
  major_label_font_size=30,
  label_font_family='Segoe UI Emoji',
  major_label_font_family='Segoe UI Emoji'
)


_graphs = []


# Dekorator do oznaczania funkcji generujących wykresy
def graph(name):
    def decorator(fun):
        category = fun.__module__.split('.')[-2]
        graphTuple = namedtuple('graph', 'fun, category, name')
        graph = graphTuple(fun, category, str(name))
        _graphs.append(graph)
    return decorator


def import_graphs():
    packages = ['messages', 'posts', 'administration', 'other']

    for package in packages:
        modules = [name for _, name, _ in pkgutil.iter_modules([f'analytics/{package}'])]
        for module in modules:
            __import__(f'analytics.{package}.{module}', fromlist=[f'analytics.{package}'])


def analyse(pack_id, file_path, delete=True):

    with zp.ZipFile(file_path) as zip:
        pdata = preprocess.preprocess(zip)
        for fun, category, name in _graphs:

            try:
                data = fun(pdata)
                if data is None:
                    continue
                graph_entry = Graph(name=name, category=category, packid=pack_id, data=data)
                db_session.add(graph_entry)
            except Exception:
                traceback.print_exc()
                graph_entry = Graph(name=name, category=category, packid=pack_id, data=None)
                db_session.add(graph_entry)

    # Usunięcie pliku
    if delete:
        os.remove(file_path)

    # Zmiana flagi mówiąca o zakończeniu analizy
    pack = db_session.query(Pack).filter_by(id=pack_id).one()
    pack.status = Pack.STATUS_SUCCESS
    db_session.add(pack)

    # Zatwierdzenie zmian
    db_session.commit()


import_graphs()

