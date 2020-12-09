import os
import glob
from config import config


def get_path_for_pack(pack_id):
    return config.UPLOADS_LOCATION + '/' + str(pack_id) + ".zip"


def remove_all_packs():
    files = glob.glob(config.UPLOADS_LOCATION + "/*")
    for f in files:
        if f.endswith(".zip"):
            os.remove(f)
