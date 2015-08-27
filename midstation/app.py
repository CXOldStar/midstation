#-*-coding:utf-8
__author__ = 'qitian'

from flask import Flask
from flask import render_template

from midstation.auth import auth


def create_app(config=None):
    """Creates the app."""

    # Initialize the app
    app = Flask(__name__)

    # Use the default config and override it afterwards
    app.config.from_object('configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("FLASK-TEST_SETTINGS", silent=True)


    configure_blueprint(app)

    return app



def configure_blueprint(app):
    app.register_blueprint(auth)



def configure_errorhandlers(app):
    """Configures the error handlers."""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500





if __name__ == '__main__':
    app = create_app()
    app.run()