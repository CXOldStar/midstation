#-*-coding:utf-8
__author__ = 'qitian'

from flask import Flask
from midstation.auth.views import auth
from midstation.station.views import station
from midstation.user.views import user
from threading import Thread
from midstation.wechat.views import wechat
import time
from midstation.utils.scrape_backend import detect_button_events
from extensions import login_manager
from midstation.user.models import User
from midstation.service.views import service

def create_app(config=None):
    """Creates the app."""

    # 探测按钮消息后台线程
    t = Thread(target=detect_button_events)
    t.setDaemon(True)
    t.start()

    # Initialize the app
    app = Flask(__name__)

    # Use the default config and override it afterwards
    app.config.from_object('midstation.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)

    configure_blueprint(app)
    configure_extensions(app)
    # configure_extensions(app)
    app.debug = app.config['DEBUG']
    return app





def configure_blueprint(app):
    app.register_blueprint(auth)
    app.register_blueprint(station, url_prefix=app.config['STATION_URL_PREFIX'])
    app.register_blueprint(user, url_prefix=app.config['USER_URL_PREFIX'])
    app.register_blueprint(service, url_prefix=app.config['SERVICE_URL_PREFIX'])
    # app.register_blueprint(wechat, url_prefix=app.config['WECHAT_URL_PREFIX'])


def configure_extensions(app):
    login_configure(app)


def login_configure(app):
    login_manager.init_app(app)
    login_manager.login_view = app.config['LOGIN_VIEW']
    @login_manager.user_loader
    def load_user(user_id):
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            return user_instance
        else:
            return None


def run_app():
    app = create_app()
    app.run

def get_signal():
    pass

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run()