from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout

from util import Palette


class DarkButton(ButtonBehavior, RelativeLayout):
    def __init__(self, **kwargs):
        self.color = Color(*Palette.gray)
        self.rect = Rectangle()
        super(DarkButton, self).__init__(**kwargs)

        with self.canvas:
            self.color
            self.rect

    def on_size(self, instance, size):
        self.rect.size = size

    def on_press(self):
        self.color.rgba = Palette.dark_gray_4

    def on_release(self):
        self.color.rgba = Palette.gray
