#-*-coding:utf-8
__author__ = 'qitian'

from flask import Flask
from midstation.auth.views import auth
from midstation.extensions import themes


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

    return app


def configure_blueprint(app):
    app.register_blueprint(auth)


def configure_extensions(app):

    # Flask-Themes
    # themes.init_themes(app, app_identifier="midstation")
    pass

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run()