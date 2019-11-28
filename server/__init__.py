# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask_sqlalchemy import SQLAlchemy


from server import configs as cfg

__version__ = '2.0.0'

db = SQLAlchemy(session_options={'autoflush': False})

if not cfg.DEBUG:
    from server.hsbpythonlog import log_initialize
    log_initialize(cfg.APP_NAME, False)
