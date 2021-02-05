import json
import pandas as pd
from . import preprocessor
from ..util import fb_decode


@preprocessor('ips')
def get_ips(zip_file, folders):
    with zip_file.open('security_and_login_information/used_ip_addresses.json') as f:
        jdata = json.loads(f.read())
        ips = []
        actions = []
        timestamps = []
        for entry in list(jdata['used_ip_address']):
            ips.append(entry['ip'])
            actions.append(entry['action'])
            timestamps.append(entry['timestamp'])
    topics = pd.DataFrame({'IP': ips, 'action': actions, 'timestamp': timestamps})
    return topics
