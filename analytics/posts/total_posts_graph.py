from .. import graph, using, style
from flask_babel import gettext as _l
import pygal
import pandas as pd


# Funkcja tworząca wykres skumulowany, wypełniając brakujące dni zerami.
def get_cum_graph(time_events):
    a = time_events.groupby([time_events.dt.year, time_events.dt.dayofyear])
    t = pd.Series(pd.date_range(time_events.dt.date.min(), time_events.dt.date.max()))
    t = pd.date_range(time_events.min(), time_events.max())
    t = pd.Series(t.date)
    days_not_present = t.isin(time_events.dt.date)
    days_not_present = ~days_not_present
    days_not_present

    temp = pd.DataFrame(
        {
            'time': time_events,
            'value': [1] * len(time_events)# + [-1] * len(days_not_present == False)
        }
    )

    temp = pd.concat([
        temp, 
        pd.DataFrame(
            {
                'time': t[days_not_present],
                'value': [-1] * len(t[days_not_present])
            }
        )    
    ])
    temp = temp.sort_values(['time']).reset_index(drop=True)
    temp

    timespan = temp.time.max() - temp.time.min()
    time_index = []

    temp.time = pd.to_datetime(temp.time)

    # Grupowanie przedziałów zliczania liczby znajomych, w zależności od tego jak stare jest konto
    if timespan.days > 360 * 10:
        distance = 'Y'
        grouped = temp.groupby([temp.time.dt.year, temp.time.dt.year])
        time_index = pd.date_range(temp.time.min().date(), temp.time.max(), freq='Y')
    elif timespan.days > 360 * 2:
        distance = 'QS'
        grouped = temp.groupby([temp.time.dt.year, temp.time.dt.quarter])
        time_index = pd.date_range(temp.time.min().date(), temp.time.max(), freq='QS')
    elif timespan.days > 40:
        distance = 'W'
        grouped = temp.groupby([temp.time.dt.year, temp.time.dt.isocalendar().week])
        time_index = pd.date_range(temp.time.min().date(), temp.time.max(), freq='W')
    elif timespan.days > 90:
        distance = 'M'
        grouped = temp.groupby([temp.time.dt.year, temp.time.dt.month])
        time_index = pd.date_range(temp.time.min().date(), temp.time.max(), freq='M')
    else:
        grouped = temp.groupby([temp.time.dt.year, temp.time.dt.day])
        time_index = pd.date_range(temp.time.min().date(), temp.time.max(), freq='D')

    # zliczanie elementów które nie są '-1'
    b = grouped['value'].agg(lambda x: len(x[x != -1]))

    # cum sumowanie
    b = b.cumsum()

    return b, time_index


@graph(_l('Cumulated number of posts'))
@using('posts')
def device_usage(data):
    post_data = data['posts']
    vals, index = get_cum_graph(post_data['time'])
    char = pygal.Line(style=style, fill=True, x_label_rotation=-45, show_legend=False)
    char.x_labels = index.date
    char.add('', list(vals))

    return char
