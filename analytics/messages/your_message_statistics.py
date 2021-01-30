from .. import graph, using
from .sentences_with_cap_letters import get_sentences_percent_with_cap_letter
from .sentences_with_punctuation import get_percent_of_messages_with_punctuation
from .words_count_in_message import get_avg_message_length
from flask_babel import gettext as _l
import pandas as pd


@graph(_l('Your messages analysis'))
@using('messages')
def your_message_stats(data):
    all_messages = data['messages']
    your_messages = all_messages[(all_messages.thread_type == 'Regular') & (all_messages.sender == data['username'])].dropna().content
    words_count = get_avg_message_length(your_messages)
    punctuation_percent = get_percent_of_messages_with_punctuation(your_messages)
    capital_percent = get_sentences_percent_with_cap_letter(your_messages)
    frame = pd.DataFrame(
        {
            'Attribute': ['Percent of sentences with punctuation', 'Percent of sentences starting with capital letter', 'Average words count in sentence'],
            'Value': [punctuation_percent, capital_percent, words_count]
        })

    return frame
