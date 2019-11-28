# -*- coding: utf-8 -*-

from __future__ import absolute_import

import traceback
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import asc, desc, or_, and_
from sqlalchemy_paginator import Paginator

from server import db
from server import errors as err
from server import utils as ut
from server import constants as const
from server.servers import models as m
from server.hsbpythonlog import log_error


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    try:
        yield db.session
        db.session.commit()
    except err.AppError:
        raise
    except Exception as e:
        db.session.rollback()
        print(traceback.format_exc())
        log_error(traceback.format_exc())
        raise err.ErrOperation
    finally:
        db.session.close()


def _filter_model(model, session, page=False, order_key=None,
                  order_desc=True, **kwargs):
    q = session.query(model)

    if order_key and order_desc:
        q = q.order_by(desc(order_key))
    elif order_key:
        q = q.order_by(asc(order_key))

    for key, value in kwargs.items():
        if hasattr(model, key):
            q = q.filter(model.__dict__[key] == value)
    if page:
        page_size = int(kwargs.get('page_size', 10))
        page_index = int(kwargs.get('page_index', 1))
        paginator = Paginator(q, page_size)
        paginator.npage = paginator.page(page_index)
        return paginator

    return q


def filter_server(session, page=False, order_key=None,
                  order_desc=True, **kwargs):
    q = session.query(m.TServer).filter_by(status=const.StatusActive)

    q = q.order_by(desc(m.TServer.status))

    if order_key and order_desc:
        q = q.order_by(desc(order_key))
    elif order_key:
        q = q.order_by(asc(order_key))

    key_word = kwargs.get('key_word')
    if key_word:
        key_word = key_word.encode('utf8')
        q = q.filter(or_(
            m.TServer.server_name.like('%{}%'.format(key_word)),
            m.TServer.server_uid.like('%{}%'.format(key_word)),
            m.TServer.salt_id.like('%{}%'.format(key_word)),
            m.TServer.inner_ip.like('%{}%'.format(key_word)),
            m.TServer.external_ip.like('%{}%'.format(key_word)),
            m.TServer.qcloud_ins_id.like('%{}%'.format(key_word))
        ))

    for key, value in kwargs.items():
        if hasattr(m.TServer, key):
            q = q.filter(m.TServer.__dict__[key] == value)
    if page:
        page_size = int(kwargs.get('page_size', 10))
        page_index = int(kwargs.get('page_index', 1))
        paginator = Paginator(q, page_size)
        paginator.npage = paginator.page(page_index)
        return paginator

    return q


def insert_server(session, **kwargs):
    now = datetime.now()
    kwargs['create_time'] = now
    kwargs['update_time'] = now
    kwargs['server_uid'] = ut.generate_uid('server')
    t = m.TServer(**kwargs)
    session.add(t)
    session.flush()

    return t.server_uid


def filter_app(session, page=False, order_key=None, order_desc=True, **kwargs):
    return _filter_model(m.TApplication, session, page, order_key,
                         order_desc, **kwargs)


def insert_app(session, **kwargs):
    now = datetime.now()
    kwargs['create_time'] = now
    kwargs['update_time'] = now
    kwargs['app_uid'] = ut.generate_uid('app')
    t = m.TApplication(**kwargs)
    session.add(t)
    session.flush()

    return t.app_uid


def filter_app_type(session, page=False, order_key=None,
                    order_desc=True, **kwargs):
    return _filter_model(m.TApplicationType, session, page, order_key,
                         order_desc, **kwargs)


def filter_app_server(session, page=False, order_key=None,
                      order_desc=True, **kwargs):
    return _filter_model(m.TApplicationServer, session, page, order_key,
                         order_desc, **kwargs)


def insert_app_server(session, **kwargs):
    now = datetime.now()
    kwargs['create_time'] = now
    kwargs['update_time'] = now
    kwargs['status'] = 1  # 初始状态为有效
    t = m.TApplicationServer(**kwargs)
    session.add(t)
    session.flush()

    return t.app_uid, t.server_uid


def filter_app_and_app_type(session, page=False, **kwargs):
    q = session.query(m.TApplication, m.TApplicationType)\
        .filter(m.TApplication.status == const.StatusActive) \
        .join(m.TApplicationType,
              m.TApplication.app_type == m.TApplicationType.app_type_id) \
        .order_by(desc(m.TApplication.status)) \
        .order_by(desc(m.TApplication.id))\

    if 'user_id' in kwargs:
        q = q.join(m.TUserApplication,
                   m.TUserApplication.app_uid == m.TApplication.app_uid) \
            .filter(or_(m.TUserApplication.user_id == kwargs['user_id'],
                        and_(m.TApplication.environment == const.EnvTest,
                             kwargs['user_position'] == const.ConstTEPosition)))

    key_word = kwargs.get('key_word')
    if key_word:
        key_word = key_word.encode('utf8')
        q = q.filter(or_(
            m.TApplication.app_uid.like('%{}%'.format(key_word)),
            m.TApplication.app_name.like('%{}%'.format(key_word)),
            m.TApplication.app_path.like('%{}%'.format(key_word)),
            m.TApplication.repo.like('%{}%'.format(key_word)),
            m.TApplication.service_name.like('%{}%'.format(key_word)),
            m.TApplication.log_module.like('%{}%'.format(key_word))
        ))

    for key, value in kwargs.items():
        if hasattr(m.TApplication, key):
            q = q.filter(m.TApplication.__dict__[key] == value)
    if page:
        page_size = int(kwargs.get('page_size', 10))
        page_index = int(kwargs.get('page_index', 1))
        paginator = Paginator(q, page_size)
        paginator.npage = paginator.page(page_index)
        return paginator

    return q


def filter_user_application(session, page=False, order_key=None,
                            order_desc=True, **kwargs):
    return _filter_model(m.TUserApplication, session, page, order_key,
                         order_desc, **kwargs)


def insert_user_app(session, **kwargs):
    now = datetime.now()
    kwargs['create_time'] = now
    kwargs['update_time'] = now
    kwargs['status'] = 1  # 初始状态为有效
    t = m.TUserApplication(**kwargs)
    session.add(t)
    session.flush()

    return t.app_uid, t.user_id


def filter_app_balancer_info(session, page=False, order_key=None,
                             order_desc=True, **kwargs):
    return _filter_model(m.TApplicationBalancerInfo, session, page, order_key,
                         order_desc, **kwargs)


def insert_app_balancer_info(session, **kwargs):
    t = m.TApplicationBalancerInfo(**kwargs)
    session.add(t)
    session.flush()

    return t.id


def insert_app_alert_info(session, **kwargs):
    t = m.TApplicationAlertInfo(**kwargs)
    session.add(t)
    session.flush()
    return t.id


def filter_app_alert_info(session, page=False, order_key=None, order_desc=True,  **kwargs):
    return _filter_model(m.TApplicationAlertInfo, session, page, order_key,
                         order_desc, **kwargs)
