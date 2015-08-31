#-*-coding:utf-8
__author__ = 'qitian'

from flask import Flask
from midstation.auth.views import auth
from midstation.station.views import station
from midstation.user.views import user
from threading import Thread
from midstation.wechat.views import wechat

def create_app(config=None):
    """Creates the app."""

    # Initialize the app
    app = Flask(__name__)

    # Use the default config and override it afterwards
    app.config.from_object('midstation.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_blueprint(app)

    # configure_extensions(app)
    app.debug = app.config['DEBUG']
    return app


def configure_blueprint(app):
    app.register_blueprint(auth)
    app.register_blueprint(station, url_prefix=app.config['STATION_URL_PREFIX'])
    app.register_blueprint(user, url_prefix=app.config['USER_URL_PREFIX'])
    app.register_blueprint(wechat, url_prefix=app.config['WECHAT_URL_PREFIX'])


def configure_extensions(app):

    # Flask-Themes
    # themes.init_themes(app, app_identifier="midstation")
    pass


def run_app():
    app = create_app()
    app.run

def get_signal():
    pass

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run()