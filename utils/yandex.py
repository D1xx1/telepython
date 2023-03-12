import yadisk
import yadisk.exceptions

from cfg.token import yadisk_token

from utils.functions import *

# yadisk_token = 'y0_AgAAAAAMStddAAlBhAAAAADeOVVZWZW4PkXfT8qZv4y_OPKHIVuQ_iU'

session = yadisk.YaDisk(token = yadisk_token)

def uploadToDisk(name:str) -> str:
    try:
    # yadisk_path = f'pythonAPI/{name[:-4]}'
        yadisk_path = f'pythonAPI/{name}'
        with open(f'{name}', 'rb') as file:
            session.upload(file,yadisk_path)
            # session.rename(yadisk_path, name)
            session.publish(yadisk_path)
    except yadisk.exceptions.PathExistsError:
        pass
    finally:
        return session.get_download_link(yadisk_path)