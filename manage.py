#!/usr/bin/env python

"""
    flaskbb.manage
    ~~~~~~~~~~~~~~~~~~~~

    This script provides some easy to use commands for
    creating the database with or without some sample content.
    You can also run the development server with it.
    Just type `python manage.py` to see the full list of commands.

    TODO: When Flask 1.0 is released, get rid of Flask-Script and use click.
          Then it's also possible to split the commands in "command groups"
          which would make the commands better seperated from each other
          and less confusing.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function
import sys
import os
import subprocess

from werkzeug.utils import import_string
from sqlalchemy.exc import IntegrityError, OperationalError
from flask_script import (Manager, Shell, Server, prompt, prompt_pass,
                          prompt_bool)
from flask_migrate import MigrateCommand, upgrade

from midstation.app import create_app
from midstation.extensions import db, plugin_manager

# Use the development configuration if available
from midstation.configs.default import DefaultConfig as Config

app = create_app()
manager = Manager(app)


# Run local server
manager.add_command("runserver", Server("localhost", port=8080))





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
