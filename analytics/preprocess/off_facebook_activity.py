import json
import pandas as pd
from . import preprocessor


@preprocessor('off_facebook_activity')
def _get_off_facebook_activity_table(zip_file, folders):
    json_filename = None
    for name in folders['ads_and_businesses']['__files']:
        if name[0] == 'your_off-facebook_activity.json':
            json_filename = name[1]
            break

    if json_filename:
        names = []
        types = []
        times = []
        with zip_file.open(json_filename) as f:
            json_data = json.loads(f.read())
            for act in json_data['off_facebook_activity']:
                name = act['name']
                for i in act['events']:
                    names.append(name)
                    types.append(i['type'])
                    times.append(i['timestamp'])
        table = pd.DataFrame({'name': names, 'type': types, 'time': times})
        table.time = pd.to_datetime(table.time, unit='s')
        return table
