from kivy.lang import Builder
from kivy.uix.image import Image


class SpinnerImage(Image):
    def __init__(self, **kwargs):
        kwargs['anim_delay'] = 0.03
        super(SpinnerImage, self).__init__(**kwargs)

Builder.load_file('uix/spinner_image.kv')
