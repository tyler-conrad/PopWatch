from functools import partial

from twisted.internet.defer import \
    Deferred, inlineCallbacks, DeferredList, returnValue

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

from uix.item_block_layout import ItemBlockLayout
from uix.item_block_line import ItemBlockLine
from uix.item_block_image import ItemBlockImage
from uix.item_block import ItemBlock
from uix.item_detail_view import MovieDetailView, TVDetailView
from client.tmdb import client as tmdb_client
from util import root
from util import chunks
from util.query import get_by_kvid


class BlankObject(object):
    pass


class NullItemBlock(object):
    def __init__(self):
        self.image = BlankObject()
        self.image.texture = BlankObject()
        self.image.texture.width = 0.0
        self.image.texture.height = 1.0


class ContentScrollView(ScrollView):
    def __init__(self, page, **kwargs):
        super(ContentScrollView, self).__init__(**kwargs)
        self.page = page
        self.line_data_list = []
        self.item_block_layout = ItemBlockLayout()
        self.add_widget(self.item_block_layout)
        self.bind(width=self.layout_images)
        self.init()

    @inlineCallbacks
    def init(self):
        data = yield self.request_data()
        self.set_max_pages(data['total_pages'])
        lines = [DeferredList(
            [self.build_item_block_deferred(item) for item in chunk])
            for chunk in chunks(
                filter(ContentScrollView.filter_results, data['results']), 2)]

        for line in lines:
            line_data = yield line
            self.parent.active = False
            self.line_data_list.append(line_data)
            left = line_data[0][1]
            try:
                right = line_data[1][1]
            except IndexError:
                right = NullItemBlock()

            item_block_line = ItemBlockLine()
            item_block_line.add_widget(left)
            if not isinstance(right, NullItemBlock):
                item_block_line.add_widget(right)
            self.item_block_layout.add_widget(item_block_line)
            self.layout_images()

    def layout_images(self, instance=None, prop=None):
        for line_data in self.line_data_list:
            left = line_data[0][1]
            try:
                right = line_data[1][1]
            except IndexError:
                right = NullItemBlock()

            right_is_null_item_block = isinstance(right, NullItemBlock)

            left_width = left.image.texture.width * 1.0
            left_height = left.image.texture.height * 1.0

            right_width = right.image.texture.width * 1.0
            right_height = right.image.texture.height * 1.0

            max_height = max(left_height, right_height)

            left_aspect = left_width / left_height
            if right_is_null_item_block:
                right_aspect = 1.0
            else:
                right_aspect = right_width / right_height

            pre_left_width = left_aspect * max_height
            if right_is_null_item_block:
                pre_right_width = 0.0
            else:
                pre_right_width = right_aspect * max_height

            line_width = pre_left_width + pre_right_width
            line_width_scale_factor = self.width / line_width

            left.width = pre_left_width * line_width_scale_factor
            right.width = pre_right_width * line_width_scale_factor

            left.height = left.width / left_aspect
            right.height = right.width / right_aspect

            left.pos = (0.0, 0.0)
            right.pos = (left.width, 0.0)

            left.parent.height = left.height

    @staticmethod
    def filter_results(item):
        return (not item.get('adult', False)) \
               and item['poster_path'] and item['backdrop_path']

    @staticmethod
    def resolve_deferred(d, item_block, dt):
        d.callback(item_block)

    @staticmethod
    def on_load(d, item_block, proxy_image):
        Clock.create_trigger(
            partial(ContentScrollView.resolve_deferred, d, item_block), -1)()

    @staticmethod
    def get_image_url(item):
        url = ''
        poster_path = item['poster_path']
        if poster_path:
            url = tmdb_client.build_poster_url(poster_path)
        else:
            backdrop_path = item['backdrop_path']
            if backdrop_path:
                url = tmdb_client.build_backdrop_url(backdrop_path)
        return url

    def build_item_block_deferred(self, item):
        d = Deferred()

        image = ItemBlockImage(source=ContentScrollView.get_image_url(item))
        item_block = ItemBlock(item, image, self.detail_view_class)

        def on_source_error(instance, error):
            d.errback(Exception('Failed to load image {}'.format(image.source)))
        image._coreimage.bind(on_error=on_source_error)

        if image._coreimage.loaded:
            ContentScrollView.on_load(d, item_block, image._coreimage)
        else:
            image._coreimage.bind(
                on_load=partial(ContentScrollView.on_load, d, item_block))
        return d


class MovieScrollView(ContentScrollView):
    def __init__(self, *args, **kwargs):
        self.detail_view_class = MovieDetailView
        super(MovieScrollView, self).__init__(*args, **kwargs)


class TVScrollView(ContentScrollView):
    def __init__(self, *args,  **kwargs):
        self.detail_view_class = TVDetailView
        super(TVScrollView, self).__init__(*args, **kwargs)


class NowPlayingMovieScrollView(MovieScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.movie_.now_playing(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), NowPlayingMovieScrollView)
        view.max_pages = max_pages


class UpcomingMovieScrollView(MovieScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.movie_.upcoming(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), UpcomingMovieScrollView)
        view.max_pages = max_pages


class PopularMovieScrollView(MovieScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.movie_.popular(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), PopularMovieScrollView)
        view.max_pages = max_pages


class TopRatedMovieScrollView(MovieScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.movie_.top_rated(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), TopRatedMovieScrollView)
        view.max_pages = max_pages


class PopularTVScrollView(TVScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.tv_.popular(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), PopularTVScrollView)
        view.max_pages = max_pages


class TopRatedTVScrollView(TVScrollView):
    @inlineCallbacks
    def request_data(self):
        popular = yield tmdb_client.tv_.top_rated(self.page)
        returnValue(popular.data)

    def set_max_pages(self, max_pages):
        view = get_by_kvid(root(), TopRatedTVScrollView)
        view.max_pages = max_pages



