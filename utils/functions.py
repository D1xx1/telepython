import re


def namechanger(youtube ,ext:str) -> str:
    name = youtube.streams[0].title
    name = re.sub('\W -+', '', name)
    name = re.sub(r'[/]', '', name) + f'{ext}'
    return name