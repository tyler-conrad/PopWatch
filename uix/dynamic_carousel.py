from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView


class DynamicCarousel(Carousel):
    index = NumericProperty(0, force_dispatch=True)

    def __init__(self, kvid, content_class, **kwargs):
        super(DynamicCarousel, self).__init__(**kwargs)
        self.kvid = kvid
        self.content_class = content_class
        self.page = 0
        self.max_pages = 2
        self.called = False
        self.update_slides_trigger = \
            Clock.create_trigger(self.update_slides, -1)

        self.left_slide = None

        self.center_slide = self.content_class(self.page + 1)
        self.add_widget(self.center_slide)

        self.right_slide = self.content_class(self.page + 2)
        self.right_slide.text = str(self.page + 1)
        self.add_widget(self.right_slide)

    def on_index(self, instance, index):
        if not self.called:
            self.update_slides_trigger()
        self.called = True

    def update_slides(self, dt):
        if len(self.slides) < 2:
            return

        if self._offset <= -self.width:
            if self.page < self.max_pages - 1:
                if self.left_slide:
                    self.remove_widget(self.left_slide)
                self.left_slide = self.center_slide
                self.center_slide = self.right_slide
                self.right_slide = self.content_class(self.page + 2)
                self.add_widget(self.right_slide)
            else:
                if self.page == self.max_pages - 1:
                    self.remove_widget(self.left_slide)
                    self.left_slide = self.center_slide
                    self.center_slide = self.right_slide
                    self.right_slide = None
                if self.page > self.max_pages - 1:
                    self.page = self.max_pages - 1

        elif self._offset >= self.width:
            if self.page > 0:
                if self.right_slide:
                    self.remove_widget(self.right_slide)
                self.right_slide = self.center_slide
                self.center_slide = self.left_slide
                self.left_slide = self.content_class(self.page)
                self.add_widget(self.left_slide, 0)
            else:
                if self.page == 0:
                    self.remove_widget(self.right_slide)
                    self.right_slide = self.center_slide
                    self.center_slide = self.left_slide
                    self.left_slide = None
                if self.page < 0:
                    self.page = 0

        super(DynamicCarousel, self).on_index(self, self.index)
        self.called = False

    def on__offset(self, *args):
        self._trigger_position_visible_slides()
        # if reached full offset, switch index to next or prev
        direction = self.direction
        _offset = self._offset
        width = self.width
        height = self.height
        index = self.index
        set_index = False
        move_right = False
        if self._skip_slide is not None or index is None:
            return

        if direction[0] == 'r':
            if _offset <= -width:
                set_index = True
                move_right = True
            if _offset >= width:
                set_index = True
                move_right = False
        if direction[0] == 'l':
            if _offset <= -width:
                set_index = True
                move_right = True
            if _offset >= width:
                set_index = True
                move_right = False
        if direction[0] == 't':
            if _offset <= - height:
                set_index = True
                move_right = True
            if _offset >= height:
                set_index = True
                move_right = False
        if direction[0] == 'b':
            if _offset <= -height:
                set_index = True
                move_right = True
            if _offset >= height:
                set_index = True
                move_right = False

        if set_index:
            if move_right:
                self.page += 1
            else:
                self.page -= 1

            if self.page > 0:
                self.index = 1
            else:
                self.index = 0

    def on_slides(self, *args):
        if len(self.slides) == 3:
            self.index = 1

        self._insert_visible_slides()
        self._trigger_position_visible_slides()

    def add_widget(self, widget, index=None):
        slide = RelativeLayout(size=self.size, x=self.x - self.width, y=self.y)
        slide.add_widget(widget)
        super(StencilView, self).add_widget(slide, index or 0)
        if index is None:
            self.slides.append(widget)
        else:
            self.slides.insert(index - len(self.slides), widget)

Builder.load_file('uix/dynamic_carousel.kv')
