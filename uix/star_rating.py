from kivy.lang import Builder
from kivy.metrics import dp
from kivy.graphics import PushMatrix
from kivy.graphics import PopMatrix
from kivy.graphics import Translate
from kivy.graphics.svg import Svg
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from util import AppLayout

file_path_from_type = {
    'full': 'assets/ic_star_24px.svg',
    'half': 'assets/ic_star_half_24px.svg',
    'empty': 'assets/ic_star_border_24px.svg'
}


class Star(Widget):
    def __init__(self, star_type, **kwargs):
        super(Star, self).__init__(**kwargs)
        self.star_type = star_type

    def on_pos(self, instance, pos):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Translate(self.x, self.y)
            Svg(file_path_from_type[self.star_type])
            PopMatrix()


class StarRating(GridLayout):
    def __init__(self, rating, **kwargs):
        super(StarRating, self).__init__(**kwargs)
        for i in range(5):
            step = i * 2.0
            if rating < step:
                self.add_widget(Star('empty'))
            elif rating < step + 1.0:
                self.add_widget(Star('half'))
            else:
                self.add_widget(Star('full'))


class ItemBlockStarRating(StarRating):
    def set_right(self, instance, width):
        self.right = width - dp(AppLayout.image_inset)

Builder.load_file('uix/star_rating.kv')
