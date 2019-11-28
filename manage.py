# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from server.api import create_app, db


app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    '''create table'''
    db.create_all()


@manager.command
def drop_db():
    """drop all table
    """
    db.drop_all()


if __name__ == '__main__':
    manager.run()
