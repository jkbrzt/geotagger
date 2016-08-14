import os


DEFAULT_CONFIG_PATH = os.path.expanduser('~/.geotagger.json')
DEFAULT_MOVES_TOKEN_PATH = os.path.expanduser('~/.geotagger-token.json')
EXIFTOOL_EXECUTABLE = '/usr/local/bin/exiftool'
WEBAPP_PORT = '7777'
WEBAPP_ROOT_URL = 'http://127.0.0.1:{}'.format(WEBAPP_PORT)
