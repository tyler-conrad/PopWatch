from kivy.lang import Builder
from kivy.uix.image import AsyncImage


class ItemBlockImage(AsyncImage):
    pass

Builder.load_file('uix/item_block_image.kv')