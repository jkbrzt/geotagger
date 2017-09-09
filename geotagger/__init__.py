import logging


__author__ = 'Jakub Roztocil'
__version__ = '0.0.3'
__licence__ = 'MIT'


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
