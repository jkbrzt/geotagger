import logging


__author__ = 'Jakub Roztocil'
__version__ = '0.0.2-beta'
__licence__ = 'BSD'


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
