import json
import pandas as pd
from . import preprocessor
from ..util import fb_decode


@preprocessor('mobile_devices')
def _get_your_topics(zip_file, folders):
    with zip_file.open('security_and_login_information/mobile_devices.json') as f:
        jdata = json.loads(f.read())
        types = []
        oss = []
        locales = []
        for entry in list(jdata['devices']):
            types.append(entry['type'])
            oss.append(entry['os'])
            locales.append(entry['device_locale'].split('_')[0])
    topics = pd.DataFrame({'name': types, 'os': oss, 'language': locales})
    return topics
