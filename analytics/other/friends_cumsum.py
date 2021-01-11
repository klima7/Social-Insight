from .. import graph, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


# wykres liczby znajomych 2
@graph(_l('Friends count'))
def friends_cumsum(data):
    frens = data['friends']
    a = frens.groupby([frens.date_added.dt.year, frens.date_added.dt.dayofyear])
    t = pd.date_range(frens.date_added.min(), frens.date_added.max())

    t = pd.Series(t.date)
    days_with_frens = t.isin(frens.date_added.dt.date)
    days_with_frens = ~days_with_frens
    # Dodawanie '-1', jako nazwy użytkownika, ponieważ pandas nie grupuje wartości None/np.nan
    frens2 = pd.concat([frens, pd.DataFrame({'date_added': t[days_with_frens], 'name': ['-1'] * len(t[days_with_frens])})])
    frens2 = frens2.sort_values(['date_added']).reset_index(drop=True)
    frens2['date_added'] = pd.to_datetime(frens2['date_added'])

    grouped = None

    timespan = frens.date_added.max() - frens.date_added.min()
    time_index = []

    # Grupowanie przedziałów zliczania liczby znajomych, w zależności od tego jak stare jest konto
    if timespan.days > 360 * 10:
        distance = 'Y'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.year])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='Y')
    elif timespan.days > 360 * 2:
        distance = 'QS'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.quarter])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='QS')
    elif timespan.days > 40:
        distance = 'W'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.isocalendar().week])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='W')
    elif timespan.days > 90:
        distance = 'M'
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.month])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='M')
    else:
        grouped = frens2.groupby([frens2.date_added.dt.year, frens2.date_added.dt.day])
        time_index = pd.date_range(frens.date_added.min().date(), frens.date_added.max(), freq='D')

    # zliczanie elementów które nie są '-1'
    b = grouped['name'].agg(lambda x: len(x[x != '-1']))

    # cum sumowanie
    b = b.cumsum()

    chart = pygal.Line(style=style, x_label_rotation=-45, fill=True, show_legend=False)
    time_index = list(map(lambda a: "{}/{}/{}".format(a.year, a.month, a.day), time_index))

    if len(b) > len(time_index):
        last_day = frens.date_added.max()
        time_index.append("{}/{}/{}".format(last_day.year, last_day.month, last_day.day))

    chart.x_labels = time_index
    chart.add('', b.to_list(), dots_size=0)
    chart.y_title = 'Friends count'
    chart.x_title = 'Date'

    return chart
