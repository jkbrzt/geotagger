import logging


__author__ = 'Jakub Roztocil'
__version__ = '0.0.1-alpha'
__licence__ = 'BSD'


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
