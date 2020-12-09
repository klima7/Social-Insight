from pygal.style import Style
from db import *
import zipfile as zp
from collections import namedtuple
import traceback
import os

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
  label_font_size=30)


_graphs = []


# Dekorator do oznaczania funkcji generujących wykresy
def graph(category, name):
    def decorator(fun):
        graphTuple = namedtuple('graph', 'fun, category, name, translated_name')
        graph = graphTuple(fun, category, str(name), name)
        _graphs.append(graph)
    return decorator


def get_translated_graph_name(english_name):
    for graph in _graphs:
        if graph.name == english_name:
            return graph.translated_name
    return None


def analyse(pack_id, file_path, delete=True):
    # Pobranie ścieżki do pliku

    with zp.ZipFile(file_path) as zip:
        pdata = gen_pandas_table(zip)
        for fun, category, name, tran_name in _graphs:

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


from .messages import *
from .other import *
from .posts import *
