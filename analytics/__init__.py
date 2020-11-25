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

    # Usunięcie pliku
    uploads.remove_pack(pack_id)

    # Wykres 1
    bar_chart = pygal.Bar(legend_at_bottom=True, style=custom_style)
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 34, 21, 13, 8, 5, 3, 2, 1, 1, 0])
    graph = Graph(name=GraphName.EXAMPLE_BAR_CHART, packid=pack_id, data=bar_chart.render_data_uri())
    db_session.add(graph)

    # Wykres 2
    pie_chart = pygal.Pie(legend_at_bottom=True, style=custom_style)
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    graph = Graph(name=GraphName.EXAMPLE_PIE_CHART, packid=pack_id, data=pie_chart.render_data_uri())
    db_session.add(graph)

    # Wykres 3
    line_chart = pygal.Line(legend_at_bottom=True, style=custom_style)
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    graph = Graph(name=GraphName.EXAMPLE_LINE_CHART, packid=pack_id, data=line_chart.render_data_uri())
    db_session.add(graph)

    # Wykres 4
    radar_chart = pygal.Radar(legend_at_bottom=True, style=custom_style)
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
    radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    graph = Graph(name=GraphName.EXAMPLE_RADAR_CHART, packid=pack_id, data=radar_chart.render_data_uri())
    db_session.add(graph)

    # Zmiana flagi mówiąca o zakończeniu analizy
    pack = db_session.query(Pack).filter_by(id=pack_id).one()
    pack.status = PackStatus.SUCCESS
    db_session.add(pack)

    # Zatwierdzenie zmian
    db_session.commit()
