# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import datetime

from server import servers as db
from server import constants as const
from server import utils as ut
from server.servers import models as m


def get_server(**kwargs):
    with db.get_session() as session:
        q = db.filter_server(session, **kwargs)
        out = q.first()
        if out is None:
            return

        return ut.obj_to_dict(out)


def add_server(**kwargs):
    with db.get_session() as session:
        return db.insert_server(session, **kwargs)


def get_servers_with_paging(**kwargs):
    with db.get_session() as session:
        p = db.filter_server(session, page=True,
                             order_key='create_time', **kwargs)
        return p.count, p.total_pages, ut.obj_to_dicts(p.npage.object_list)


def update_server(**kwargs):
    with db.get_session() as session:
        s = db.filter_server(session, server_uid=kwargs['server_uid']) \
            .with_lockmode('update') \
            .first()
        if s is None:
            return

        for k, v in kwargs.items():
            setattr(s, k, v)

        setattr(s, 'update_time', datetime.now())

        return s.id


def add_app(**kwargs):
    with db.get_session() as session:
        return db.insert_app(session, **kwargs)


def get_app(**kwargs):
    with db.get_session() as session:
        q = db.filter_app(session, **kwargs)
        out = q.first()
        if out is None:
            return

        return ut.obj_to_dict(out)


def get_app_by_name(**kwargs):
    with db.get_session() as session:
        q = db.filter_app(session, **kwargs)
        out = q.all()

        return ut.obj_to_dicts(out)


def have_repeated_app_name(**kwargs):
    with db.get_session() as session:
        q = db.filter_app(session, **{'app_name': kwargs['app_name'],
                                      'environment': kwargs['environment']})
        q = q.filter(m.TApplication.app_uid != kwargs['app_uid'])
        out = q.first()
        if out:
            return True

        return False


def get_apps_with_paging(**kwargs):
    with db.get_session() as session:
        p = db.filter_app_and_app_type(session, page=True, **kwargs)
        for app, app_type in p.npage.object_list:
            app.app_type_name = app_type.app_type_name

        p.npage.object_list = \
            list(map(lambda args: args[0], p.npage.object_list))

        return p.count, p.total_pages, ut.obj_to_dicts(p.npage.object_list)


def update_app(**kwargs):
    with db.get_session() as session:
        a = db.filter_app(session, app_uid=kwargs['app_uid']) \
            .with_lockmode('update') \
            .first()
        if a is None:
            return

        for k, v in kwargs.items():
            setattr(a, k, v)

        setattr(a, 'update_time', datetime.now())

        return a.app_uid


def get_app_type_list(**kwargs):
    with db.get_session() as session:
        out = db.filter_app_type(session, **kwargs).all()
        return ut.obj_to_dicts(out)


def merge_app_server(**kwargs):
    with db.get_session() as session:
        a = db.filter_app_server(session, **{
            'app_uid': kwargs['app_uid'],
            'server_uid': kwargs['server_uid']
        }).with_lockmode('update') \
            .first()
        if a is None:
            return db.insert_app_server(session, **kwargs)

        for k, v in kwargs.items():
            setattr(a, k, v)

        setattr(a, 'update_time', datetime.now())

        return a.app_uid, a.server_uid


def get_active_servers_by_app_id(**kwargs):
    with db.get_session() as session:
        q = db.filter_server(session, **{'status': const.StatusActive})

        q = q.join(m.TApplicationServer,
                   m.TApplicationServer.server_uid == m.TServer.server_uid)\
            .filter(m.TApplicationServer.app_uid == kwargs['app_uid'],
                    m.TApplicationServer.status == const.StatusActive)

        out = q.all()

        return ut.obj_to_dicts(out)


def get_app_server(**kwargs):
    with db.get_session() as session:
        out = db.filter_app_server(session, **kwargs) \
            .first()
        if out is None:
            return

        return ut.obj_to_dict(out)


def get_app_list_by_server_id(**kwargs):
    with db.get_session() as session:
        q = db.filter_app_server(session, **kwargs)

        out = q.all()

        return ut.obj_to_dicts(out)


def get_user_apps(**kwargs):
    with db.get_session() as session:
        q = db.filter_user_application(session, **kwargs)

        out = q.all()

        return ut.obj_to_dicts(out)


def merge_app_user(**kwargs):
    with db.get_session() as session:
        a = db.filter_user_application(session, **{
            'app_uid': kwargs['app_uid'],
            'user_id': kwargs['user_id']
        }).with_lockmode('update') \
            .first()
        if a is None:
            return db.insert_user_app(session, **kwargs)

        for k, v in kwargs.items():
            setattr(a, k, v)

        setattr(a, 'update_time', datetime.now())

        return a.app_uid, a.user_id


def get_active_users_by_app_id(**kwargs):
    with db.get_session() as session:
        q = db.filter_user_application(session,
                                       **{'app_uid': kwargs['app_uid'],
                                          'status': const.StatusActive})

        out = q.all()

        return ut.obj_to_dicts(out)


def get_app_balancer_info(**kwargs):
    with db.get_session() as session:
        q = db.filter_app_balancer_info(session, **kwargs)
        out = q.one_or_none()
        if out is None:
            return

        return ut.obj_to_dict(out)


def get_app_balancer_info_by_app_id(**kwargs):
    with db.get_session() as session:
        q = db.filter_app_balancer_info(session, **kwargs)
        out = q.all()

        return ut.obj_to_dicts(out)


def add_app_balancer_info(**kwargs):
    with db.get_session() as session:
        return db.insert_app_balancer_info(session, **kwargs)


def update_app_balancer_info(**kwargs):
    with db.get_session() as session:
        s = db.filter_app_balancer_info(session, id=kwargs['id']) \
            .with_lockmode('update') \
            .first()
        if s is None:
            return

        for k, v in kwargs.items():
            setattr(s, k, v)

        setattr(s, 'update_time', datetime.now())

        return s.id


def get_app_balancer_info_with_paging(**kwargs):
    with db.get_session() as session:
        p = db.filter_app_balancer_info(session, page=True,
                                        order_key='create_time', **kwargs)
        return p.count, p.total_pages, ut.obj_to_dicts(p.npage.object_list)


def get_app_list_by_config_path(app_uid, cfg_path):
    with db.get_session() as session:
        q = db.filter_app(session, **{'app_type': const.TypeConfig,
                                      'app_config_path': cfg_path})

        q = q.filter(m.TApplication.app_uid != app_uid)

        out = q.all()

        return ut.obj_to_dicts(out)


def check_config_conflicts(apps, srv_uid):
    for app in apps:
        srvs = get_active_servers_by_app_id(**app)
        for srv in srvs:
            if srv['server_uid'] == srv_uid:
                return True

    return False


def add_app_alert_info(**kwargs):
    with db.get_session() as session:
        return db.insert_app_alert_info(session, **kwargs)


def get_app_alert_info(**kwargs):
    with db.get_session() as session:
        q = db.filter_app_alert_info(session, **kwargs)
        out = q.first()
        if out is None:
            return

        return ut.obj_to_dict(out)


def add_or_update_app_alert_info(**kwargs):
    with db.get_session() as session:
        a = db.filter_app_alert_info(session, app_uid=kwargs['app_uid']) \
            .with_lockmode('update') \
            .first()
        if a is None:
            a = db.insert_app_alert_info(session, **kwargs)

        for k, v in kwargs.items():
            setattr(a, k, v)

        return a.id


def get_app_alert_infos_with_paging(**kwargs):
    with db.get_session() as session:
        p = db.filter_app_alert_info(session, page=True, **kwargs)
        return p.count, p.total_pages, ut.obj_to_dicts(p.npage.object_list)
