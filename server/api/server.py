# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from flask import Blueprint, request

from server.api import route
from server.servers import forms
from server.servers import middles as m
from server.utils import validate_args, fill_page_info
from server import utils as ut
from server import errors as err
from server import constants as const
from server.hsbpythonlog import log_error

bp = Blueprint('server', __name__, url_prefix='/server')


@route(bp, '/get_server_list', methods=['POST'], output=False)
def get_server_list():
    params = forms.get_server_list_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_servers_with_paging(**params)

    return fill_page_info(params, rv)


@route(bp, '/get_server', methods=['POST'])
def get_server():
    params = forms.get_server_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_server(**params)
    if rv is None:
        raise err.ErrServerNotFound

    return rv


@route(bp, '/add_server', methods=['POST'])
def add_server():
    params = forms.add_server_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    m.add_server(**params)


@route(bp, '/update_server', methods=['POST'])
def update_server():
    params = forms.update_server_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.update_server(**params)
    if rv is None:
        raise err.ErrServerNotFound


@route(bp, '/get_app', methods=['POST'])
def get_app():
    params = forms.get_app_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app(**params)
    if rv is None:
        raise err.ErrAppNotFound

    rv['server_list'] = m.get_active_servers_by_app_id(**params)
    rv['user_list'] = m.get_active_users_by_app_id(**params)

    return rv


@route(bp, '/get_app_by_name', methods=['POST'])
def get_app_by_name():
    params = forms.get_app_by_name_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_by_name(**params)
    if rv is None:
        raise err.ErrAppNotFound
    out = []
    for app in rv:
        if app['status'] == const.StatusActive:
            out.append(app)
    return rv


@route(bp, '/get_app_list', methods=['POST'], output=False)
def get_app_list():
    params = forms.get_app_list_schema(
        validate_args(request.get_json(force=True, silent=False))
    )
    rv = m.get_apps_with_paging(**params)
    return fill_page_info(params, rv)


@route(bp, '/add_app', methods=['POST'])
def add_app():
    params = forms.add_app_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app(**{'app_name': params['app_name'],
                      'environment': params['environment']})
    if rv is not None:
        raise err.ErrAppRepeatedError

    m.add_app(**params)


@route(bp, '/update_app', methods=['POST'])
def update_app():
    params = forms.update_app_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    if params.get('app_name'):
        if m.have_repeated_app_name(**params):
            raise err.ErrAppRepeatedError

    # 如果是配置类型的应用, 需要检测目录是否冲突
    app_type = params.get('app_type')
    cfg_path = params.get('app_config_path')
    if app_type == const.TypeConfig or cfg_path:
        app = m.get_app(**{'app_uid': params['app_uid']})
        if app is None:
            raise err.ErrAppNotFound

        app_type = app_type or app['app_type']
        cfg_path = cfg_path or app['app_config_path']

        if app_type == const.TypeConfig:
            apps = m.get_app_list_by_config_path(params['app_uid'], cfg_path)
            if apps:
                srvs = m.get_active_servers_by_app_id(**{
                    'app_uid': params['app_uid']
                })
                for srv in srvs:
                    if m.check_config_conflicts(apps, srv['server_uid']):
                        raise err.ErrConfigConflicts

    rv = m.update_app(**params)
    if rv is None:
        raise err.ErrAppNotFound


@route(bp, '/get_app_type_list', methods=['POST'], output=False)
def get_app_type_list():
    rv = m.get_app_type_list()

    return rv


@route(bp, '/set_app_server', methods=['POST'])
def set_app_server():
    params = forms.set_app_server_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    app = m.get_app(**{'app_uid': params['app_uid'],
                       'status': const.StatusActive})
    if app is None:
        raise err.ErrAppNotFound

    srv = m.get_server(**{'server_uid': params['server_uid'],
                          'status': const.StatusActive})
    if srv is None:
        raise err.ErrServerNotFound

    if params['status'] == 0:
        m.merge_app_server(**params)

        return

    if app['environment'] != srv['environment']:
        raise err.ErrAppServerNotInSameEnv

    if app['app_type'] == const.TypeConfig:
        apps = m.get_app_list_by_config_path(app['app_uid'],
                                             app['app_config_path'])
        if apps and m.check_config_conflicts(apps, srv['server_uid']):
            raise err.ErrConfigConflicts

    m.merge_app_server(**params)


@route(bp, '/set_app_servers', methods=['POST'])
def set_app_servers():
    params = forms.set_app_servers_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    app = m.get_app(**{'app_uid': params['app_uid'],
                       'status': const.StatusActive})
    if app is None:
        raise err.ErrAppNotFound

    if app['app_type'] == const.TypeConfig:
        apps = m.get_app_list_by_config_path(app['app_uid'],
                                             app['app_config_path'])
    print(88888888, params )
    for srv_uid in params['server_uids']:
        srv = m.get_server(**{'server_uid': srv_uid,
                              'status': const.StatusActive})
        if srv is None:
            raise err.ErrServerNotFound

        if params['status'] == 0:
            m.merge_app_server(**params)

            continue

        if app['environment'] != srv['environment']:
            raise err.ErrAppServerNotInSameEnv

        if app['app_type'] == const.TypeConfig and apps and \
                m.check_config_conflicts(apps, srv['server_uid']):
            raise err.ErrConfigConflicts

        m.merge_app_server(**{'app_uid': app['app_uid'],
                              'server_uid': srv['server_uid'],
                              'status': const.StatusActive})


@route(bp, '/get_server_list_by_app_id', methods=['POST'], output=False)
def get_server_list_by_app_id():
    params = forms.get_server_list_by_app_id_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_active_servers_by_app_id(**params)

    out = list()
    for s in rv:
        out.append(m.get_server(**{'server_uid': s['server_uid']}))

    return out


@route(bp, '/get_app_server', methods=['POST'])
def get_app_server():
    params = forms.get_app_server_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_server(**params)
    if rv is None:
        raise err.ErrAppServerNotFound

    return rv


@route(bp, '/get_app_list_by_server_id', methods=['POST'], output=False)
def get_app_list_by_server_id():
    params = forms.get_app_list_by_server_id_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_list_by_server_id(**params)

    out = list()
    for s in rv:
        out.append(m.get_app(**{'app_uid': s['app_uid']}))

    return out


@route(bp, '/get_user_apps', methods=['POST'], output=False)
def get_user_apps():
    params = forms.get_user_apps_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_user_apps(**params)

    return rv


@route(bp, '/set_app_users', methods=['POST'])
def set_app_users():
    params = forms.set_app_users_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    app = m.get_app(**{'app_uid': params.get('app_uid'),
                       'status': const.StatusActive})
    if app is None:
        raise err.ErrAppNotFound

    for uid, uname in params['users']:
        m.merge_app_user(**{'app_uid': app['app_uid'], 'user_id': uid,
                            'user_name': uname, 'status': const.StatusActive})


@route(bp, '/set_app_user', methods=['POST'])
def set_app_user():
    params = forms.set_app_user_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    app = m.get_app(**{'app_uid': params.get('app_uid'),
                       'status': const.StatusActive})
    if app is None:
        raise err.ErrAppNotFound

    m.merge_app_user(**{
        'app_uid': app['app_uid'],
        'user_id': params['user_id'],
        'user_name': params['user_name'],
        'status': params['status']
    })


@route(bp, '/get_app_node_status', methods=['POST'])
def get_app_node_status():
    params = forms.get_app_node_status_schema(
        validate_args(request.get_json(force=True, silent=False))
    )
    tag = ''
    md5 = ''
    process_number = 0

    app = m.get_app(**{'app_uid': params['app_uid']})
    if app is None:
        raise err.ErrAppNotFound

    srv = m.get_server(**{'server_uid': params['server_uid']})
    if srv is None:
        raise err.ErrServerNotFound

    if const.TypeCPlus == app['app_type']:
        has_err, info = ut.get_app_status(srv['salt_id'],
                                          os.path.join(app['app_path'],
                                                       app['app_name']))
        if has_err:
            log_error('get app status error <%s>' % info)
        else:
            process_number = len(info.split('\n')) - 3
            md5 = info.split('\n')[-3][:32] \
                if len(info.split('\n')) > 1 else ''

    else:
        has_err, info = ut.get_cur_branch(srv['salt_id'], app['app_path'])
        if has_err:
            log_error('get current branch error <%s>' % info)
        else:
            tag = info.split('\n')[0].split('/')[-1]

    return {
        'app_uid': app['app_uid'],
        'server_uid': srv['server_uid'],
        'process_number': process_number,
        'tag': tag,
        'md5': md5
    }


@route(bp, '/get_app_balancer_info', methods=['POST'])
def get_app_balancer_info():
    params = forms.get_app_balancer_info_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_balancer_info(**params)
    if rv is None:
        raise err.ErrAppBalancerInfoNotFound

    app = m.get_app(**{'app_uid': rv['app_uid']})
    rv['app_name'] = app['app_name']

    return rv


@route(bp, '/get_app_balancer_info_by_app_id', methods=['POST'], output=False)
def get_app_balancer_info_by_app_id():
    params = forms.get_app_balancer_info_by_app_id_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_balancer_info_by_app_id(**params)

    return rv


@route(bp, '/add_app_balancer_info', methods=['POST'])
def add_app_balancer_info():
    params = forms.add_app_balancer_info_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    _id = m.add_app_balancer_info(**params)

    return {
        'id': _id
    }


@route(bp, '/update_app_balancer_info', methods=['POST'])
def update_app_balancer_info():
    params = forms.update_app_balancer_info_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    _id = m.update_app_balancer_info(**params)

    return {
        'id': _id
    }


@route(bp, '/get_app_balancer_info_list', methods=['POST'], output=False)
def get_app_balancer_info_list():
    params = forms.get_app_balancer_info_list_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    rv = m.get_app_balancer_info_with_paging(**params)
    foo = rv[2]

    # 增加app_name字段
    for bar in foo:
        app = m.get_app(**{'app_uid': bar['app_uid']})

        bar['environment'] = app['environment']
        bar['app_name'] = app['app_name']

    return fill_page_info(params, rv)


@route(bp, '/add_or_update_app_alert_info', methods=['POST'])
def add_app_alert_info():
    params = validate_args(request.get_json(force=True, silent=False))
    m.add_or_update_app_alert_info(**params)


@route(bp, '/get_app_alert_info', methods=['POST'])
def get_app_alert_info():
    params = validate_args(request.get_json(force=True, silent=False))

    rv = m.get_app_alert_info(**params)
    if rv is None:
        m.add_app_alert_info(**{'app_uid': params['app_uid'],
                                'log_module': '',
                                'ding_token': ''})
        rv = m.get_app_alert_info(**params)
    return rv


@route(bp, '/get_app_alert_info_list', methods=['POST'])
def get_app_alert_info_list():
    params = validate_args(request.get_json(force=True, silent=False))

    rv = m.get_app_alert_infos_with_paging(**params)
    return fill_page_info(params, rv)


@route(bp, '/get_server_list_by_app_name', methods=['POST'], output=False)
def get_server_list_by_app_name():
    params = forms.get_server_list_by_app_name_schema(
        validate_args(request.get_json(force=True, silent=False))
    )

    srv_app = {'app_name': params['app_name']}

    app_list = m.get_app_by_name(**params)
    for app in app_list:
        rv = m.get_active_servers_by_app_id(app_uid=app['app_uid'])
        out = list()
        for s in rv:
            out.append(m.get_server(**{'server_uid': s['server_uid']}))
        if app['environment'] == 'test':
            srv_app['test_server_uid_set'] = out
        else:
            srv_app['pro_server_uid_set'] = out
    return srv_app
