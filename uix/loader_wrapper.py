from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout

from uix.spinner_image import SpinnerImage
from util import Palette


class FaderBackground(Widget):
    def __init__(self, **kwargs):
        super(FaderBackground, self).__init__(**kwargs)
        with self.canvas:
            self.color = Color(*Palette.black)
            self.rect = Rectangle()

    def on_size(self, instance, size):
        self.rect.size = size


def loader_wrapper_factory(base_class):
    class LoaderWrapper(RelativeLayout):
        active = BooleanProperty(True)
        alpha = NumericProperty(1.0)

        def __init__(self, *args, **kwargs):
            super(LoaderWrapper, self).__init__(**kwargs)
            self.fader_background = FaderBackground()
            self.spinner_image = SpinnerImage()
            self.add_widget(self.spinner_image, 0)
            self.add_widget(self.fader_background, 1)
            self.add_widget(base_class(*args), 2)

        def on_active(self, instance, active):
            Animation(alpha=0.0, duration=0.2).start(self)

        def on_alpha(self, instance, alpha):
            self.fader_background.color.a = alpha
            self.spinner_image.color[-1] = alpha

    return LoaderWrapper