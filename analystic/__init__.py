import pygal
from db import *
import uploads


def analyse(pack_id):

    # Pobranie obiektu paczki z bazy
    pack = db_session.query(Pack).filter_by(id=pack_id).one()

    # Pobranie ścieżki do pliku
    file_path = uploads.get_path_for_pack(pack_id)

    # Zrobienie jakiegoś wykresu bez sensu
    bar_chart = pygal.Bar()
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    data = bar_chart.render_data_uri()

    # Usunięcie pliku
    uploads.remove_pack(pack_id)

    # Dodanie wykresu do bazy danych
    pack.chart1 = data

    # Zmiana flagi mówiąza o zakończeniu analizy
    pack.done = True

    # Dodanie obiektu do transakcji i zatwierdzenie transakcji
    db_session.add(pack)
    db_session.commit()
