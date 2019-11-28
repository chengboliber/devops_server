# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from server.configs import SERVER_IP, SERVER_PORT, DEBUG
from server import api

app = DispatcherMiddleware(api.create_app())

if __name__ == "__main__":
    run_simple(SERVER_IP, SERVER_PORT, app, use_reloader=DEBUG,
               use_debugger=DEBUG)
