import pygal
from pygal.style import Style
from db import *
import uploads
import zipfile as zp

style = Style(
  background='white',
  plot_background='white',
  transition='400ms ease-in',
  legend_font_size=20)


_analysers = {}


def analyser(graph):
    def decorator(fun):
        _analysers[graph] = fun
    return decorator


def analyse(pack_id):
    # Pobranie ścieżki do pliku
    file_path = uploads.get_path_for_pack(pack_id)

    with zp.ZipFile(file_path) as zip:
        for graphName, analyser in _analysers.items():
            data_uri = analyser(zip).render_data_uri()
            graph = Graph(name=graphName.nr, packid=pack_id, data=data_uri)
            db_session.add(graph)

    # Usunięcie pliku
    uploads.remove_pack(pack_id)

    # Zmiana flagi mówiąca o zakończeniu analizy
    pack = db_session.query(Pack).filter_by(id=pack_id).one()
    pack.status = Pack.STATUS_SUCCESS
    db_session.add(pack)

    # Zatwierdzenie zmian
    db_session.commit()


from .messages import *
from .other import *
from .posts import *
