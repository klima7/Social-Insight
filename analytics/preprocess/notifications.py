import re
import json
import pandas as pd
from . import preprocessor


@preprocessor('notifications')
def _get_notifications(zip_file, folders):
    notify_table = None
    try:
        with zip_file.open('about_you/notifications.json') as f:
            jdata = json.loads(f.read())

            type_reg = re.compile(r'(https://www.facebook.com/)(.+?)([/.])(.*)')

            times = []
            types = []

            for i in jdata['notifications']:
                times.append(i['timestamp'])
                try:
                    types.append(re.findall(type_reg, i['href'])[0][1])
                except:
                    types.append(None)
            notify_table = pd.DataFrame({'time': times, 'url_type': types})
            notify_table.time = pd.to_datetime(notify_table.time, unit='s')
    except Exception as e:
        pass

    return notify_table
