import json
import pandas as pd
from . import preprocessor
from ..util import fb_decode


@preprocessor('search_history')
def _get_search_history(zip_file, folders):
    try:
        with zip_file.open('search_history/your_search_history.json') as f:
            jdata = json.loads(f.read())
            messages = []
            types = []
            for search in list(jdata['searches']):
                if 'data' in search:
                    messages.append(fb_decode(search['data'][0]['text']))
                    types.append(fb_decode(search['title']))
        history = pd.DataFrame({'message': messages, 'type': types})
        return history
    except:
        return None
