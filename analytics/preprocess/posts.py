import json
import pandas as pd
from . import preprocessor


@preprocessor('posts')
def _get_posts_data(zip_file, folders):
    file_paths = [i[1] for i in folders['posts']['__files']]
    post_data = pd.DataFrame({'time': [], 'title': []})

    for path in file_paths:
        if path == 'posts/no-data.txt':
            break

        with zip_file.open(path) as f:
            jdata = json.loads(f.read())
            tdata = {'time': [], 'title': []}

            if isinstance(jdata, dict):
                jdata = [jdata]

            for i in jdata:
                if 'timestamp' not in i or 'title' not in i:
                    continue
                tdata['time'].append(i['timestamp'])
                tdata['title'].append(i.get('title'))
            temp_table = pd.DataFrame(tdata)
            temp_table.time = pd.to_datetime(temp_table.time, unit='s')
            post_data = pd.concat([post_data, temp_table])

    return post_data
