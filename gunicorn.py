# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

from server.configs import SERVER_IP, SERVER_PORT, DEBUG

bind = "{ip}:{port}".format(ip=SERVER_IP, port=SERVER_PORT)
backlog = 2048

workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 0
timeout = 30

daemon = False

if DEBUG:
    loglevel = 'debug'
else:
    loglevel = 'info'
