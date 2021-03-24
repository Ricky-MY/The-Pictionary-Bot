from yaml import load, SafeLoader

with open("config.yml", 'r') as file:
    _CONFIGURATION = load(file, Loader=SafeLoader)


def get_values(major: str) -> dict:
    return _CONFIGURATION[major]


style = get_values('style')
bot = get_values('bot')
dir = get_values('directory')


class Colour:
    EXCEPTION = style['exception']
    LIGHT_BLUE = style['light_blue']
    SUN_YELLOW = style['sun_yellow']
    BRIGHT_GREEN = style['bright_green']
    BABY_PINK = style['baby_pink']
    COLORS = style['light_blue']
    EXCEPTION = style['exception']


class Directory:
    PACKAGE = dir['package']
    MODULES = dir['modules']
    COGS = dir['cogs']


PREFIX = bot['prefix']
ADMINS = bot['admins']
