from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.relativelayout import RelativeLayout


class MainContentArea(RelativeLayout):
    history = ListProperty()

    def swap_content(self, widget):
        self.clear_widgets()
        self.add_widget(widget)

    def swap_content_clear_history(self, widget):
        self.history = []
        self.swap_content(widget)

    def swap_content_with_history(self, widget):
        self.history.append(self.children[0])
        self.swap_content(widget)

    def back(self):
        self.swap_content(self.history.pop())

Builder.load_file('uix/main_content_area.kv')
