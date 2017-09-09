"""
https://dev.moves-app.com/docs

"""
import logging
import datetime
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from geotagger.utils import parse_date


log = logging.getLogger(__name__)


class MovesClient:
    AUTH_ROOT = 'https://api.moves-app.com/oauth/v1'
    API_ROOT = 'https://api.moves-app.com/api/1.1'

    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def get(self, url, params=None, auth=True):
        return self.request(url=url, params=params, method='GET', auth=auth)

    def post(self, url, params=None, auth=True):
        return self.request(url=url, params=params, method='POST', auth=auth)

    def request(self, url, params=None, method='GET', auth=True):
        if not url.startswith('https://'):
            url = self.API_ROOT + url
        headers = {}
        if auth:
            assert self.access_token
            headers['Authorization'] = 'Bearer {}'.format(self.access_token)
        log.info('> %s %s params=%s', method, url, params)
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers
        )
        log.info('< HTTP %s', response.status_code)
        log.debug('< %s', response.text)
        response.raise_for_status()
        return response.json()

    def build_url(self, root, path, params):
        return root + path + '?' + urlencode(params)

    def build_authorize_url(self, scope='activity location'):
        return self.build_url(self.AUTH_ROOT, '/authorize', {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': scope,
        })

    def get_token(self, code, ):
        return self.post(self.AUTH_ROOT + '/access_token', auth=False, params={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

    def get_token_info(self, access_token):
        return self.get('/tokeninfo', auth=False, params={
            'access_token': access_token
        })

    def get_places(self, date):
        """
        https://dev.moves-app.com/docs/api_places

        """
        if isinstance(date, datetime.date):
            date = date.isoformat().replace('-', '')
        return self.get('/user/places/daily/{}'.format(date))

    def get_storyline(self, date):
        """
        https://dev.moves-app.com/docs/api_places

        """
        if isinstance(date, datetime.date):
            date = date.isoformat().replace('-', '')
        return self.get('/user/storyline/daily/{}'.format(date), params={
            'trackPoints': 'true'
        })


def parse_response(resp):
    datetime_keys = ['time', 'lastUpdate']

    if isinstance(resp, list):
        return [parse_response(obj) for obj in resp]

    if hasattr(resp, 'encode'):
        return resp

    for key, value in resp.items():
        if isinstance(value, (dict, list)):
            value = parse_response(value)
        elif any(token.lower() in key.lower() for token in datetime_keys):
            value = parse_date(value)
        resp[key] = value
    return resp


class MovesModel:

    def __init__(self, client):
        self.client = client

    def get_places(self, date):
        return parse_response(self.client.get_places(date)[0]['segments'])

    def get_storyline(self, date):
        return parse_response(self.client.get_storyline(date)[0])


