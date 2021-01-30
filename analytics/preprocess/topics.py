import json
import pandas as pd
from . import preprocessor, fb_decode


@preprocessor('topics')
def _get_your_topics(zip_file, folders):
    with zip_file.open('your_topics/your_topics.json') as f:
        jdata = json.loads(f.read())
        topics = []
        for topic in list(jdata['inferred_topics']):
            topics.append(fb_decode(topic))
    topics = pd.DataFrame({'topic': topics})
    return topics
