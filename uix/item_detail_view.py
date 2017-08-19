from twisted.internet.defer import inlineCallbacks

from kivy.uix.scrollview import ScrollView

from uix.item_detail_layout import ItemDetailLayout
from uix.backdrop_banner import BackdropBanner
from client.tmdb import client


class ItemDetailView(ScrollView):
    def __init__(self, item, **kwargs):
        super(ItemDetailView, self).__init__(**kwargs)
        self.item = item
        self.layout = ItemDetailLayout()
        self.add_widget(self.layout)
        self.init()

    @inlineCallbacks
    def init(self):
        details = yield self.fetch_details(self.item)
        self.layout.add_widget(BackdropBanner(details))


class MovieDetailView(ItemDetailView):
    def fetch_details(self, item):
        return client.movie(item['id'], params={
            'append_to_response': 'recommendations,similar,reviews,images',
            'include_image_language': 'en,null'})


class TVDetailView(ItemDetailView):
    def fetch_details(self, item):
        return client.tv(item['id'], params={
            'append_to_response': 'recommendations,similar,images'})
