import json
import pandas as pd
from . import preprocessor


@preprocessor('friends')
def _get_friends_table(zip_file, folders):
    friends_file_name = folders['friends']['__files'][0][1]

    friends_table = None

    paths = [i[1] for i in folders['friends']['__files']]

    for path in paths:
        try:
            with zip_file.open(path) as f:
                jdata = json.loads(f.read())

                names = []
                times = []
                types = []
                list_name = list(jdata.keys())[0]
                for i in jdata[list_name]:
                    names.append(i['name'].encode('latin1').decode('utf8'))
                    times.append(i['timestamp'])
                    types.append(list_name)

                temp_table = pd.DataFrame({'name': names, 'time': times, 'type': types})
                temp_table.time = pd.to_datetime(temp_table.time, unit='s')

                if friends_table is None:
                    friends_table = temp_table
                else:
                    friends_table = pd.concat([friends_table, temp_table])
        except:
            pass

    return friends_table
