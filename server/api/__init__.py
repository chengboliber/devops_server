# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import pkgutil
import importlib
import traceback

from os.path import dirname, abspath
from functools import wraps

from flask import Flask, Blueprint
from voluptuous import MultipleInvalid
from werkzeug import exceptions as wkerr

from server import db
from server.utils import jsonify, CustomJSONEncoder
from server.errors import AppError, ErrArgs, ErrInternal
from server.hsbpythonlog import log_error


def register_blueprints(app, package_name, package_path):
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


def create_app(settings_override=None):
    app = Flask(__name__)
    app_name = dirname(dirname(abspath(__file__))).split(os.sep)[-1]
    app.config.from_object("%s.configs" % app_name)
    app.config.from_object(settings_override)
    app.json_encoder = CustomJSONEncoder

    register_blueprints(app, __name__, __path__)

    db.init_app(app)

    return app


def route(bp, *args, **kwargs):
    output = kwargs.pop('output') if 'output' in kwargs else True

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                rv = f(*args, **kwargs)
            except (wkerr.BadRequest, MultipleInvalid) as e:
                # 入参get_json解析错误会抛BadRequest
                print(traceback.format_exc())
                log_error(str(e))
                return jsonify(has_error=True, data=ErrArgs)
            except AppError as e:
                print(traceback.format_exc())
                return jsonify(has_error=True, data=e)
            except Exception:
                print(11111111, traceback.format_exc())
                log_error(traceback.format_exc())
                return jsonify(has_error=True, data=ErrInternal)

            return jsonify(data=rv, output=output)

        return f

    return decorator
