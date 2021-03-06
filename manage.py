# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
from threading import Thread

from flask_script import (Manager, Shell, Server, prompt, prompt_pass,
                          prompt_bool)
from flask_migrate import MigrateCommand, upgrade

from midstation.app import create_app
from midstation.extensions import db, plugin_manager
from midstation.utils.scrape_backend import detect_button_events

# Use the development configuration if available
from midstation.configs.default import DefaultConfig as Config

app = create_app()
manager = Manager(app)


# Run local server
manager.add_command("runserver", Server('localhost', port=8080))


@manager.command
def initdb():
    """Creates the database."""

    upgrade()


@manager.command
def dropdb():
    """Deletes the database."""

    db.drop_all()


if __name__ == "__main__":
    manager.run()
