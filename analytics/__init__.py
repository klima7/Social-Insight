import pygal
from pygal.style import Style
from db import *
import uploads

custom_style = Style(
  background='white',
  plot_background='white',
  transition='400ms ease-in',
  legend_font_size=20)


def analyse(pack_id):
    # Pobranie ścieżki do pliku
    file_path = uploads.get_path_for_pack(pack_id)

    # Zrobienie jakiegoś wykresu bez sensu
    bar_chart = pygal.Bar(legend_at_bottom=True, style=custom_style)
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 34, 21, 13, 8, 5, 3, 2, 1, 1, 0])
    data = bar_chart.render_data_uri()

    # Usunięcie pliku
    uploads.remove_pack(pack_id)

    # Dodanie wykresu do bazy danych
    print(pack_id)
    graph1 = Graph(name='graph1', packid=pack_id, data=data)
    db_session.add(graph1)

    # Zmiana flagi mówiąca o zakończeniu analizy
    pack = db_session.query(Pack).filter_by(id=pack_id).one()
    pack.status = PackStatus.SUCCESS
    db_session.add(pack)

    # Zatwierdzenie zmian
    db_session.commit()
