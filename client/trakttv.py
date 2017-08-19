from twisted.internet.defer import inlineCallbacks, returnValue
from common.cache import cached_request

from common.response import Response

api_endpoint = 'https://api.trakt.tv/'
client_id = '76e4786d6fd3aa6c741a242391d3093084798b7f2317fa8d24e8bca6bad9f252'


def request(method, path, look_in_cache, **kwargs):
    headers = kwargs.get('headers', {})
    headers.update({
        'Content-type': 'application/json',
        'trakt-api-key': client_id,
        'trakt-api-version': '2'
    })
    kwargs['headers'] = headers

    url_parts = [api_endpoint]
    url_parts.extend(path)

    return cached_request(method, ''.join(url_parts), look_in_cache, **kwargs)


def get(path, look_in_cache, **kwargs):
    return request('GET', path, look_in_cache, **kwargs)


def post(path, look_in_cache, **kwargs):
    return request('POST', path, look_in_cache, **kwargs)


def put(path, look_in_cache, **kwargs):
    return request('PUT', path, look_in_cache, **kwargs)


def delete(path, look_in_cache, **kwargs):
    return request('DELETE', path, look_in_cache, **kwargs)


class Movies(object):
    @inlineCallbacks
    def trending(self, page, limit=10, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        params['limit'] = str(limit)
        kwargs['params'] = params
        trending = yield get(['movies/trending'], look_in_cache, **kwargs)
        data = yield trending.json()
        headers = dict(trending.headers.getAllRawHeaders())
        returnValue(Response(
            item_count=int(headers['X-Pagination-Item-Count'][0]),
            limit=int(headers['X-Pagination-Limit'][0]),
            page=int(headers['X-Pagination-Page'][0]),
            page_count=int(headers['X-Pagination-Page-Count'][0]),
            user_count=int(headers['X-Trending-User-Count'][0]),
            data=data
        ))


class Shows(object):
    @inlineCallbacks
    def trending(self, page, limit=10, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        params['limit'] = str(limit)
        kwargs['params'] = params
        trending = yield get(['shows/trending'], look_in_cache, **kwargs)
        data = yield trending.json()
        headers = dict(trending.headers.getAllRawHeaders())
        returnValue(Response(
            item_count=int(headers['X-Pagination-Item-Count'][0]),
            limit=int(headers['X-Pagination-Limit'][0]),
            page=int(headers['X-Pagination-Page'][0]),
            page_count=int(headers['X-Pagination-Page-Count'][0]),
            user_count=int(headers['X-Trending-User-Count'][0]),
            data=data
        ))




class Client(object):
    def __init__(self):
        self.movies = Movies()
        self.shows = Shows()

client = Client()
