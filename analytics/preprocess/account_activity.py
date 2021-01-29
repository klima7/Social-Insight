import user_agents
import json
import pandas as pd
from . import preprocessor


def _aux_get_device_os_browser(t):
    t = user_agents.parse(t)
    dev = str(t.device.brand) + ' ' + str(t.device.model)
    if t.device.brand is None and t.device.model is None:
        if t.is_pc:
            dev = 'PC'
        else:
            dev = 'Other'
    return dev, str(t.os.family), t.browser.family


@preprocessor('account_activity')
def _get_acc_activity_table(zip_file, folders):
    acc_activity_path = None
    for i in folders['security_and_login_information']['__files']:
        if i[0] == 'account_activity.json':
            acc_activity_path = i[1]
            break

    with zip_file.open(acc_activity_path) as f:
        actions = []
        times = []
        devices = []
        oss = []
        browsers = []
        json_data = json.loads(f.read())
        for j in json_data['account_activity']:
            actions.append(j['action'])
            device, os, browser = _aux_get_device_os_browser(j['user_agent'])

            devices.append(device)
            oss.append(os)
            browsers.append(browser)
            times.append(j['timestamp'])

        acc_activity = pd.DataFrame({'time': times, 'device': devices, 'os': oss, 'browser': browsers, 'action': actions})
        acc_activity.time = pd.to_datetime(acc_activity.time, unit='s')
    return acc_activity
