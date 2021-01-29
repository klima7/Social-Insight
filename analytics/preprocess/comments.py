import json
import pandas as pd
from . import preprocessor


@preprocessor('comments')
def _get_comments_data(zip_file, folders):
    file_paths = [i[1] for i in folders['comments']['__files']]
    comment_data = pd.DataFrame({'time': [], 'content': [], 'group': []})

    for path in file_paths:
        if path == 'posts/no-data.txt':
            break

        with zip_file.open(path) as f:
            jdata = json.loads(f.read())
            tdata = {'time': [], 'content': [], 'group': []}

            for i in jdata['comments']:
                tdata['time'].append(i['timestamp'])
                if ('data' in i) and len(i['data']) > 0 and 'comment' in i['data'][0]:
                    com = i['data'][0]['comment']

                    content = com.get('comment')
                    if content:
                        content = content.encode('latin1').decode('utf8')
                    group = com.get('group')
                    if group:
                        group = group.encode('latin1').decode('utf8')

                    tdata['content'].append(content)
                    tdata['group'].append(group)
                else:
                    tdata['content'].append(None)
                    tdata['group'].append(None)
            temp_table = pd.DataFrame(tdata)
            temp_table.time = pd.to_datetime(temp_table.time, unit='s')
            comment_data = pd.concat([comment_data, temp_table])

    return comment_data
