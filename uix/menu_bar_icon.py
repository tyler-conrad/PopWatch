from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.graphics import PushMatrix, PopMatrix, Translate
from kivy.graphics.svg import Svg
from kivy.uix.widget import Widget

from util import AppLayout


class MenuBarIcon(Widget):
    svg_file_path = StringProperty()

    def __init__(self, **kwargs):
        super(MenuBarIcon, self).__init__(**kwargs)
        self.translation = \
            dp((AppLayout.menu_bar_size - AppLayout.menu_bar_icon_size) / 2.0)

        self.bind(
            pos=self.update,
            size=self.update,
            svg_file_path=self.update)

    def update(self, instance, prop):
        with self.canvas:
            PushMatrix()
            Translate(self.translation, self.translation)
            Svg(self.svg_file_path)
            PopMatrix()
