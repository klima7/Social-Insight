from .. import graph, using, style
from flask_babel import gettext as _l
from collections import Counter
import re
import pandas as pd


def get_most_common_words(data, min_word_width):
    all_messages = data['messages']
    messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender == data['username'])].dropna()

    counter = Counter()

    for conv, msgs in messages.groupby(messages.conversation):
        if msgs.content is not None and len(msgs.content) >= 1:
            for msg in msgs.content:
                words = [word.lower() for word in re.split(r'[\s,.]', re.sub(r'[^\w ]+', '', msg)) if min_word_width < len(word) < 20]
                counter.update(words)

    common_words = counter.most_common(50)
    text = ''
    for word, count in common_words:
        text += '%s(%d), ' % (word, count)
    text = text[0:-2]

    table = pd.DataFrame({'': [text]})
    return table


@graph(_l('Most common words you use'))
@using('messages')
def words_count_in_message(data):
    return get_most_common_words(data, 1)


@graph(_l('Most common words you use (above 5 letters)'))
@using('messages')
def words_count_in_message(data):
    return get_most_common_words(data, 5)
