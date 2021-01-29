import json
from . import preprocessor


@preprocessor('username')
def _get_username(zip_file, folders):
    name_file = folders['profile_information']['__files'][0][1]
    with zip_file.open(name_file) as f:
        data = json.loads(f.read())
        username = data['profile']['name']['full_name'].encode('latin1').decode('utf8')
    return username
