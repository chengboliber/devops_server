# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
import uuid
import traceback

import salt.client

from datetime import date

from flask import jsonify as flask_jsonify
from flask import current_app, request
from flask.json import JSONEncoder

from server import __version__
from server.errors import ErrArgs, ErrTargetNoMatch
from server.hsbpythonlog import log_debug, log_info, log_error
from server.configs import FAKE_SALT


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def obj_to_dict(obj, filters=list()):
    out = dict()
    for k, v in obj.__dict__.items():
        if k not in filters and not k.startswith('_'):
            out[k] = v

    return out


def obj_to_dicts(obj):
    if isinstance(obj, list):
        rv = list()
        for _ in obj:
            rv.append(obj_to_dict(_, filters=['query', 'query_class']))
    else:
        raise Exception('%s is not supported' % type(obj))

    return rv


def validate_args(in_data):
    print(11111111, in_data)
    if current_app.debug:
        log_debug('<remote addr: %s> <%s> <%s>' % (request.remote_addr,
                                                   request.path, str(in_data)))

    if in_data is None:
        return dict()

    if not isinstance(in_data, dict):
        raise ErrArgs

    if in_data.get('_head') is None:
        raise ErrArgs

    if in_data['_head'].get('_version') is None:
        raise ErrArgs

    if __version__ != in_data['_head']['_version']:
        raise ErrArgs

    if in_data.get('_param') is None:
        raise ErrArgs

    return in_data['_param']


def fill_page_info(params, result):
    return {
        'page_info': {
            'page_size': params.get('page_size', 10),
            'page_index': params.get('page_index', 1),
            'total_number': result[0],
            'total_pages': result[1]
        },
        'list': result[2]
    }


def jsonify(has_error=False, data=None, output=True):
    out = {
        '_head': {
            '_version': __version__,
            '_msgType': 'response',
            '_interface': request.path,
            '_remark': '',
            '_timestamps': time.time()
        },
        '_data': {
            '_errCode': None,
            '_errStr': None,
            '_ret': None
        }
    }

    if has_error:
        out['_data']['_errCode'] = data.code
        out['_data']['_errStr'] = data.message
        out['_data']['_ret'] = -1
    else:
        out['_data']['_errCode'] = 0
        out['_data']['_errStr'] = 'ok'
        out['_data']['_ret'] = 0
        if data is not None:
            out['_data']['_retData'] = data

    if current_app.debug and output:
        log_debug('<%s> <%s>' % (request.path, str(out)))

    return flask_jsonify(out)


def _salt_cmd(target, cmd):
    log_info('salt "{0}" cmd.run "{1}"'.format(target, cmd))

    if FAKE_SALT:
        return 0, ''

    try:
        client = salt.client.LocalClient()

        ret = client.cmd(target, 'cmd.run', [cmd, 'shell="/bin/bash"',
                                             'runas="root"'])
        if ret[target] is False:
            return -1, 'fail to execute command'

        if len(ret[target]) > 0 and ret[target][-3:] == '\nok':
            return 0, ret[target].encode('utf-8')
    except KeyError:
        return -1, str(ErrTargetNoMatch)
    except Exception as e:
        log_error(traceback.format_exc())
        return -1, str(e)

    return -1, ret[target].encode('utf-8')


def get_app_status(target, search_key):
    cmd = 'ps aux | grep -v grep | grep -w {0}; md5sum {0} && echo "\nok"' \
        .format(search_key)

    return _salt_cmd(target, cmd)


def get_cur_branch(target, app_path):
    cmd = 'cd {} && git symbolic-ref -q HEAD && echo "\nok"'.format(
        app_path)

    return _salt_cmd(target, cmd)


def generate_uid(prefix=''):
    s = str(time.time())[1:6] + uuid.uuid4().hex[:6]
    if prefix:
        return prefix + '-' + s

    return s
