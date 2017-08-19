from functools import partial

from twisted.internet.defer import Deferred, inlineCallbacks

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label

from uix.star_rating import ItemBlockStarRating
from client.tmdb import client


class GenreLabel(Label):
    pass


class GenreLayout(GridLayout):
    pass


class BackdropImage(AsyncImage):
    pass


class BackdropBanner(RelativeLayout):
    def __init__(self, details, **kwargs):
        self.details = details.data
        self.title = self.details.get('original_name') \
            or self.details.get('original_title')

        super(BackdropBanner, self).__init__(**kwargs)
        self.backdrop = None

        self.genre_layout = GenreLayout()
        for genre in self.details['genres']:
            self.genre_layout.add_widget(GenreLabel(text=genre['name']))
        self.add_widget(self.genre_layout)

        star_rating = ItemBlockStarRating(self.details['vote_average'])
        self.bind(width=star_rating.set_right)
        self.add_widget(star_rating)

        self.bind(width=self.layout_backdrop)
        self.init()

    @inlineCallbacks
    def init(self):
        self.backdrop = yield BackdropBanner.fetch_image(
            client.build_backdrop_url(self.details['backdrop_path']))
        self.add_widget(self.backdrop, 3)
        self.layout_backdrop()
        self.parent.parent.parent.active = False

    def layout_backdrop(self, instance=None, width=None):
        if not self.backdrop:
            return

        width = self.backdrop.texture.width * 1.0
        height = self.backdrop.texture.height * 1.0
        aspect = width / height
        self.height = self.width / aspect

    @staticmethod
    def resolve_image_deferred(d, image, dt):
        d.callback(image)

    @staticmethod
    def on_load_image(d, image, proxy_image):
        Clock.create_trigger(
            partial(BackdropBanner.resolve_image_deferred, d, image), -1)()

    @staticmethod
    def fetch_image(image_url):
        d = Deferred()
        image = BackdropImage(source=image_url)

        def on_source_error(instance, error):
            d.errback(Exception(
                'Failed to load image {}'.format(image.source)))
        image._coreimage.bind(on_error=on_source_error)

        if image._coreimage.loaded:
            BackdropBanner.on_load_image(d, image, image._coreimage)
        else:
            image._coreimage.bind(
                on_load=partial(BackdropBanner.on_load_image, d, image))
        return d

Builder.load_file('uix/backdrop_banner.kv')
