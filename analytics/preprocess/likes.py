import json
import pandas as pd
from . import preprocessor


@preprocessor('likes')
def _get_likes_data(zip_file, folders):
    like_table = pd.DataFrame({'time': [], 'reaction': []})

    paths = ['likes_and_reactions/posts_and_comments.json', 'likes_and_reactions/pages.json']
    for path in paths:
        # Likes on posts
        with zip_file.open('likes_and_reactions/posts_and_comments.json') as f:
            jdata = json.loads(f.read())

            likes = []
            times = []

            for i in jdata['reactions']:
                times.append(i['timestamp'])
                likes.append(i['data'][0]['reaction']['reaction'])

            temp_table = pd.DataFrame({'time': times, 'type': likes})
            temp_table.time = pd.to_datetime(temp_table.time, unit='s')
            like_table = pd.concat([like_table, temp_table])

    return like_table
