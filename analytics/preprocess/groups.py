import re
import json
import pandas as pd
from . import preprocessor


@preprocessor('groups_join')
def _get_group_join(zip_file, folders):
    group_join = None
    try:
        with zip_file.open('groups/your_group_membership_activity.json') as f:
            jdata = json.loads(f.read())

            times = []

            for i in jdata['groups_joined']:
                times.append(i['timestamp'])

            temp_table = pd.DataFrame({'time': times})
            temp_table.time = pd.to_datetime(temp_table.time, unit='s')
            group_join = temp_table
    except:
        pass

    return group_join


@preprocessor('group_interactions')
def _get_group_interactions(zip_file, folders):
    group_interactions = None
    try:
        with zip_file.open('interactions/groups.json') as f:
            jdata = json.loads(f.read())

            names = []
            values = []

            regx = re.compile(r'^(\d+)')
            for huh in jdata['group_interactions']:
                for i in huh['entries']:
                    value = re.findall(regx, i['data']['value'])
                    if len(value) == 0:
                        continue

                    values.append(int(value[0]))
                    names.append(i['data']['name'].encode('latin1').decode('utf8'))
            group_interactions = pd.DataFrame({'name': names, 'value': values})
    except:
        pass

    return group_interactions
