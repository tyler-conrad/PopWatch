from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout

from uix.star_rating import ItemBlockStarRating
from uix.loader_wrapper import loader_wrapper_factory
from util import root
from util.query import get_by_kvid


class ItemBlock(ButtonBehavior, RelativeLayout):
    def __init__(self, item, image, detail_view_class, **kwargs):
        super(ItemBlock, self).__init__(**kwargs)
        self.item = item
        self.image = image
        self.detail_view_class = detail_view_class
        self.add_widget(self.image)
        star_rating = ItemBlockStarRating(self.item['vote_average'])
        self.bind(width=star_rating.set_right)
        self.add_widget(star_rating)

    def on_press(self):
        get_by_kvid(
            root(),
            'main_content_area'
        ).swap_content_with_history(
            loader_wrapper_factory(self.detail_view_class)(self.item))

Builder.load_file('uix/item_block.kv')
