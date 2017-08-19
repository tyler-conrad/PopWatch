from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

from uix.back_button import BackButton
from util import root
from util.query import get_by_kvid


class MenuBar(RelativeLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.back_button = None
        Clock.schedule_once(self.bind_back_button, -1)

    def bind_back_button(self, dt):
        get_by_kvid(root(), 'main_content_area').bind(history=self.on_history)

    def on_history(self, main_content_area, history):
        if len(history):
            if not self.back_button:
                self.back_button = BackButton()
                self.add_widget(self.back_button)
        else:
            self.remove_widget(self.back_button)
            self.back_button = None


Builder.load_file('uix/menu_bar.kv')
