from twisted.internet.defer import inlineCallbacks
from twisted.python.log import PythonLoggingObserver

import kivy
kivy.require('1.10.0')
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.loader import Loader
from kivy.app import App

from client.tmdb import client as tmdb_client
from util.query import get_by_kvid

PythonLoggingObserver(loggerName='twisted').stop()
PythonLoggingObserver(loggerName='kivy').start()

Loader.num_workers = 20


class PopWatchApp(App):
    @inlineCallbacks
    def on_start(self):
        yield tmdb_client.configuration()
        get_by_kvid(self.root, 'hamburger_button').nav_modal.open()

if __name__ == '__main__':
    PopWatchApp().run()
