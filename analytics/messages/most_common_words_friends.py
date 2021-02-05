from .. import graph, using
from ..util import shorten_strings
from flask_babel import gettext as _l
from collections import Counter
import re
import pandas as pd


@graph(_l('Most common words your friends use (above 5 letters)'))
@using('messages', 'username')
def words_count_in_message(data):
    all_messages = data['messages']
    messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender != data['username'])].dropna()

    users_list = []
    words_list = []

    for conv, msgs in messages.groupby(messages.conversation):

        counter = Counter()

        if msgs.content is not None and len(msgs.content) >= 1:
            for msg in msgs.content:
                words = [word.lower() for word in re.split(r'[\s,.]', re.sub(r'[^\w ]+', '', msg)) if 5 < len(word) < 20]
                counter.update(words)

        if len(counter) == 0:
            continue

        common_words = counter.most_common(3)
        text = ''
        for word, count in common_words:
            text += '%s(%d), ' % (word, count)
        text = text[0:-2]

        users_list.append(conv)
        words_list.append(text)

    table = pd.DataFrame({'User': users_list, 'Most common words': words_list})
    table['User'] = shorten_strings(table['User'])

    return table.head(10), table
