import json
import pandas as pd
from . import preprocessor

@preprocessor('following')
def _get_following_data(zip_file, folders):
    follows = None

    try:
        with zip_file.open('following_and_followers/following.json') as f:
            jdata = json.loads(f.read())

            times = []

            for i in list(jdata['following']):
                times.append(i['timestamp'])

            follows = pd.DataFrame({'time': times, 'type': ['person'] * len(times)})
    except Exception as e:
        pass

    try:
        with zip_file.open('following_and_followers/followed_pages.json') as f:
            jdata = json.loads(f.read())

            times = []

            for i in list(jdata['pages_followed']):
                times.append(i['timestamp'])

            temp_follows = pd.DataFrame({'time': times, 'type': ['page'] * len(times)})
            if follows is None:
                follows = temp_follows
            else:
                follows = pd.concat([follows, temp_follows])
    except Exception as e:
        pass

    if follows is not None:
        follows.time = pd.to_datetime(follows.time, unit='s')

    return follows
