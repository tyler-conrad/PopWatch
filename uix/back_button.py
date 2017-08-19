from kivy.lang import Builder

from uix.dark_button import DarkButton
from util import root
from util.query import get_by_kvid


class BackButton(DarkButton):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)

    def on_press(self):
        super(BackButton, self).on_press()
        get_by_kvid(root(), 'main_content_area').back()

Builder.load_file('uix/back_button.kv')
