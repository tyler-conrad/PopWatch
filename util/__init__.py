from kivy.app import App


def root():
    return App.get_running_app().root


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class Palette(object):
    white = (1.0, 1.0, 1.0, 1.0)
    dark_red = (0.7, 0.0, 0.0, 1.0)
    gray = (0.5, 0.5, 0.5, 1.0)
    light_gray_0 = (0.9, 0.9, 0.9, 1.0)
    dark_gray_4 = (0.33, 0.33, 0.33, 1.0)
    dark_gray_3 = (0.25, 0.25, 0.25, 1.0)
    dark_gray_2 = (0.2, 0.2, 0.2, 1.0)
    dark_gray_1 = (0.17, 0.17, 0.17, 1.0)
    dark_gray_0 = (0.13, 0.13, 0.13, 1.0)
    black = (0.0, 0.0, 0.0, 1.0)
    image_overlay_background_color = (0.3, 0.3, 0.3, 0.7)


class AppLayout(object):
    menu_bar_size = 60.0
    menu_bar_icon_size = 48.0
    nav_modal_button_spacing = 10.0
    nav_modal_title_font_size = 48.0
    nav_modal_button_font_size = 36.0
    star_size = 24.0
    image_inset = 20.0
    backdrop_banner_title_font_size = 64.0
    backdrop_banner_title_outline_size = 2.0
    genre_layout_height = 30.0
    genre_layout_spacing = 10.0
    genre_label_font_size = 24.0
    genre_label_horiz_padding = 10.0
