from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.python.log import PythonLoggingObserver
from twisted.internet.defer import inlineCallbacks
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from client import trakttv
from client import tmdb
from util.log import Loggable

PythonLoggingObserver(loggerName='twisted').stop()
PythonLoggingObserver(loggerName='kivy').start()

trakttv_client = trakttv.client
tmdb_client = tmdb.client


class TMDBNowPlayingMovieButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        now_playing = yield tmdb_client.movie_.now_playing(1)
        print now_playing


class TMDBPopularMovieButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        popular = yield tmdb_client.movie_.popular(1)
        print popular


class TMDBTopRatedMovieButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        top_rated = yield tmdb_client.movie_.top_rated(1)
        print top_rated


class TMDBUpcomingMovieButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        upcoming = yield tmdb_client.movie_.upcoming(1)
        print upcoming


class TMDBPopularTVButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        popular = yield tmdb_client.tv_.popular(1)
        print popular


class TMDBTopRatedTVButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        top_rated = yield tmdb_client.tv_.top_rated(1)
        print top_rated


class TMDBConfigButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        config = yield tmdb_client.configuration()
        print config


class TMDBTVButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        show = yield tmdb_client.tv(1396, params={
            'append_to_response': 'recommendations,similar,images'
        })
        print show


class TMDBMovieButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        movie = yield tmdb_client.movie(293167, params={
            'append_to_response': 'recommendations,similar,reviews,images',
            'include_image_language': 'en,null'
        })
        print movie


class TraktTVMoviesTrendingButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        trending = yield trakttv_client.movies.trending(1)
        print trending


class TraktTVShowsTrendingButton(Button, Loggable):
    @inlineCallbacks
    def on_press(self):
        trending = yield trakttv_client.shows.trending(1)
        print trending


class PopWatchApp(App):
    def build(self):
        return Builder.load_file('tester.kv')

if __name__ == '__main__':
    PopWatchApp().run()
