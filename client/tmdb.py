from collections import deque
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
from common.cache import cached_request

from common.response import Response

RATE_LIMIT = 0.26
api_endpoint = 'https://api.themoviedb.org/3/'
api_key = 'e1e974a7f89b46e3fd6b569c404f5517'

request_deque = deque()


def process_queue():
    if not len(request_deque):
        return

    d, kwargs = request_deque.pop()
    cached_request(**kwargs).chainDeferred(d)
LoopingCall(process_queue).start(RATE_LIMIT, now=False)


def queue_request(method, url, look_in_cache, **kwargs):
    kwargs.update({
        'method': method,
        'url': url,
        'look_in_cache': look_in_cache
    })
    d = Deferred()
    request_deque.appendleft((d, kwargs))
    return d


def request(method, path, look_in_cache, use_rate_limit, **kwargs):
    params = kwargs.get('params', {})
    params['api_key'] = api_key
    kwargs['params'] = params

    url_parts = [api_endpoint]
    url_parts.extend(path)
    url = ''.join(url_parts)

    if use_rate_limit:
        return queue_request(method, url, look_in_cache, **kwargs)
    return cached_request(method, url, look_in_cache, **kwargs)


def get(path, look_in_cache, use_rate_limit=True, **kwargs):
    return request('GET', path, look_in_cache, use_rate_limit, **kwargs)


def post(path, look_in_cache, use_rate_limit=True,  **kwargs):
    return request('POST', path, look_in_cache, use_rate_limit, **kwargs)


def put(path, look_in_cache, use_rate_limit=True,  **kwargs):
    return request('PUT', path, look_in_cache, use_rate_limit, **kwargs)


def delete(path, look_in_cache, use_rate_limit=True,  **kwargs):
    return request('DELETE', path, look_in_cache, use_rate_limit, **kwargs)


class Movie(object):
    @inlineCallbacks
    def now_playing(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        now_playing = yield get(['movie/now_playing'], look_in_cache, **kwargs)
        data = yield now_playing.json()
        returnValue(Response(data=data))

    @inlineCallbacks
    def popular(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        popular = yield get(['movie/popular'], look_in_cache, **kwargs)
        data = yield popular.json()
        returnValue(Response(data=data))

    @inlineCallbacks
    def top_rated(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        top_rated = yield get(['movie/top_rated'], look_in_cache, **kwargs)
        data = yield top_rated.json()
        returnValue(Response(data=data))

    @inlineCallbacks
    def upcoming(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        upcoming = yield get(['movie/upcoming'], look_in_cache, **kwargs)
        data = yield upcoming.json()
        returnValue(Response(data=data))

    # @inlineCallbacks
    # def images(self, movie_id, look_in_cache=True, **kwargs):
    #     images = yield get(
    #         ['movie/', str(movie_id), '/images'], look_in_cache, **kwargs)
    #     data = yield images.json()
    #     returnValue(Response(data=data))


class TV(object):
    @inlineCallbacks
    def popular(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        popular = yield get(['tv/popular'], look_in_cache, **kwargs)
        data = yield popular.json()
        returnValue(Response(data=data))

    @inlineCallbacks
    def top_rated(self, page, look_in_cache=True, **kwargs):
        params = kwargs.get('params', {})
        params['page'] = str(page)
        kwargs['params'] = params
        top_rated = yield get(['tv/top_rated'], look_in_cache, **kwargs)
        data = yield top_rated.json()
        returnValue(Response(data=data))


class Client(object):
    def __init__(self):
        self.movie_ = Movie()
        self.tv_ = TV()

        self.image_base_url = ''
        self.backdrop_size = ''
        self.poster_size = ''

    def build_backdrop_url(self, backdrop_path):
        return self.image_base_url + self.backdrop_size + backdrop_path

    def build_poster_url(self, poster_path):
        return self.image_base_url + self.poster_size + poster_path

    @inlineCallbacks
    def configuration(self, look_in_cache=True, **kwargs):
        config = yield get(['configuration'], look_in_cache, **kwargs)
        data = yield config.json()

        self.image_base_url = data['images']['secure_base_url']

        backdrop_sizes = data['images']['backdrop_sizes']
        if 'w780' not in backdrop_sizes:
            self.backdrop_size = backdrop_sizes[1]
        else:
            self.backdrop_size = 'w780'

        poster_sizes = data['images']['poster_sizes']
        if 'w780' not in poster_sizes:
            self.poster_size = poster_sizes[-2]
        else:
            self.poster_size = 'w780'

        returnValue(Response(data=data))

    @inlineCallbacks
    def movie(self, movie_id, look_in_cache=True, **kwargs):
        movie = yield get(['movie/', str(movie_id)], look_in_cache, **kwargs)
        data = yield movie.json()
        returnValue(Response(data=data))

    @inlineCallbacks
    def tv(self, tv_id, look_in_cache=True, **kwargs):
        show = yield get(['tv/', str(tv_id)], look_in_cache, **kwargs)
        data = yield show.json()
        returnValue(Response(data=data))

client = Client()
