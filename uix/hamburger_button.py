from kivy.lang import Builder

from uix.dark_button import DarkButton
from uix.nav_modal import NavModal


class HamburgerButton(DarkButton):
    def __init__(self, **kwargs):
        super(HamburgerButton, self).__init__(**kwargs)
        self.nav_modal = NavModal()

    def on_press(self):
        super(HamburgerButton, self).on_press()
        self.nav_modal.open()


Builder.load_file('uix/hamburger_button.kv')
