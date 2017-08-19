from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label

from uix.dynamic_carousel import DynamicCarousel
from uix.loader_wrapper import loader_wrapper_factory
from util import root
from util.query import get_by_kvid


class NavModalButton(ToggleButtonBehavior, Label):
    content_class = ObjectProperty()

    def on_state(self, instance, state):
        if state != 'down':
            return

        get_by_kvid(
            root(), 'main_content_area'
        ).swap_content_clear_history(
            DynamicCarousel(
                self.content_class,
                loader_wrapper_factory(self.content_class)))

        get_by_kvid(root(), 'hamburger_button').nav_modal.dismiss()

Builder.load_file('uix/nav_modal_button.kv')
