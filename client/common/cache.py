from sys import getsizeof
from json import dumps
from twisted.internet.defer import succeed
from treq.client import _combine_query_params
from treq import request
from cachetools import LRUCache
from cookielib import CookieJar

cache = LRUCache(maxsize=246 * 1024 * 1024, getsizeof=getsizeof)


def add_to_cache(response, key):
    cache[key] = response
    return response


def build_cache_key(method, url, **kwargs):
    key = {
        'method': method.upper(),
        'url': _combine_query_params(url, kwargs.get('params') or {}).lower(),
    }

    if 'headers' in kwargs:
        key['headers'] = frozenset(kwargs['headers'].items())

    if 'data' in kwargs:
        data = kwargs['data']
        if not isinstance(data, str):
            raise TypeError('"data" parameter must be a str.')
        key['data'] = data

    if 'json' in kwargs:
        key['json'] = dumps(kwargs['json'], allow_nan=False, sort_keys=True)

    if 'allow_redirects' in kwargs:
        key['allow_redirects'] = kwargs['allow_redirects']

    if 'auth' in kwargs:
        key['auth'] = kwargs['auth']

    if 'cookies' in kwargs:
        cookies = kwargs['cookies']
        if isinstance(cookies, CookieJar):
            cookie_dict = {}
            for cookie in cookies:
                cookie_dict[cookie.name] = cookie.value
            key['cookies'] = frozenset(cookie_dict.items())
        key['cookies'] = frozenset(cookies.items())

    if 'browser_like_redirects' in kwargs:
        key['browser_like_redirects'] = kwargs['browser_like_redirects']

    return frozenset(key.items())


def cached_request(method, url, look_in_cache, **kwargs):
    key = build_cache_key(method, url, **kwargs)

    if look_in_cache:
        try:
            out = cache[key]
        except KeyError:
            out = request(method, url, **kwargs)
            out.addCallback(add_to_cache, key)
            return out
        return succeed(out)

    out = request(method, url, **kwargs)
    out.addCallback(add_to_cache, key)
    return out



