from .. import graph
from .message_stats import get_messages_stats
from flask_babel import gettext as _l
import pandas as pd


@graph('messages', _l('Your message statistics'))
def your_message_stats(data):
    mess = data['messages']
    friends_avg = data['friends_stats_mean']

    your_stats = get_messages_stats(mess[(mess.thread_type == 'Regular') & (mess.sender == data['username'])].dropna().content)
    # '% Zdań ze znakami interpunkcyjnymi', df['% zn_int'])
    # chart.add('% Zdań zaczętych wielką literą', df['% zd_wl'])
    # chart.add('Średnia liczba słów w wiadomości
    xdpd = pd.DataFrame(
        {
            '': ['Średnia znajomych', 'Twoje statystyki'],
            '% Zdań ze znakami interpunkcyjnymi': [friends_avg['% zn_int'], your_stats[1]],
            '% Zdań zaczętych wielką literą': [friends_avg['% zd_wl'], your_stats[3]],
            'Średnia długość zdania': [friends_avg['avg_word'], your_stats[4]],
        })

    # xdpd = xdpd.set_index('*')
    xdpd = xdpd.round({'% Zdań ze znakami interpunkcyjnymi': 2, '% Zdań zaczętych wielką literą': 2, 'Średnia długość zdania': 1})
    return xdpd
