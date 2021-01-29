import json
from . import preprocessor


@preprocessor('event_responses')
def _get_event_responses(zip_file, folders):
    events = None
    try:
        with zip_file.open('events/your_event_responses.json') as f:
            jdata = json.loads(f.read())
            events = {}
            for ev_type in list(jdata['event_responses'].keys()):
                events[ev_type] = len(jdata['event_responses'][ev_type])

    except Exception as e:
        pass

    return events
