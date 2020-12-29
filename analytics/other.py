import pandas as pd
import numpy as np
import emoji

import pygal
from flask_babel import lazy_gettext as _l

from . import style, emojistyle, graph

# wykres liczby znajomych 2
@graph('other', _l('Friends count'))
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

    chart = pygal.Line(x_label_rotation=-45, fill=True)
    time_index = list(map(lambda a: "{}/{}/{}".format(a.year, a.month, a.day), time_index))

    if len(b) > len(time_index):
        last_day = frens.date_added.max()
        time_index.append("{}/{}/{}".format(last_day.year, last_day.month, last_day.day))
        
    chart.x_labels = time_index
    chart.add('', b.to_list(), dots_size=0)

    return chart

@graph('other', _l('Device usage statistics'))
def device_usage(data):
    acc_act = data['account_activity']
    acc_act.agent.unique()
    device_usage = acc_act.groupby(acc_act.agent).action.count().sort_values(ascending=True)
    total_uses = device_usage.sum()

    chart = pygal.HorizontalBar(show_legend=False)
    chart.x_labels = list(device_usage.index)
    chart.add('', [ (i / total_uses) * 100 for i in list(device_usage)])
    # chart.y_title = 'device name'
    chart.x_title = '% of usage'

    return chart

@graph('other', _l('% of logins by hour'))
def logins_by_hour(data):
    acc_act = data['account_activity']
    hour_active = acc_act[(acc_act.action == 'Login') | (acc_act.action == 'Session updated')].groupby(acc_act.time.dt.hour)
    hour_active = hour_active.action.count()
    total_hours = hour_active.sum()
    
    hour_active = dict(hour_active)
    for i in range(24):
        if not i in hour_active:
            hour_active[i] = 0
    # sorted(hour_active.items(), key=lambda x: x[0])
    chart = pygal.Bar(show_legend=False)
    chart.x_labels = [i for i in range(24)]
    chart.add('', [(hour_active[i] / total_hours) * 100 for i in range(24)])
    chart.y_title = '% of activity'
    chart.x_title = 'hour'

    return chart
