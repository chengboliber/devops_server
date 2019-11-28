# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint

from server import db


class TServer(db.Model):
    """
    服务器配置表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_server'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(64), nullable=False)
    server_uid = db.Column(db.String(128), nullable=False)
    salt_id = db.Column(db.String(128), nullable=False)
    external_ip = db.Column(db.String(64), nullable=False)
    inner_ip = db.Column(db.String(64), nullable=False)
    server_name = db.Column(db.String(64), nullable=False)
    server_desc = db.Column(db.String(255), nullable=False)
    qcloud_ins_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class TApplication(db.Model):
    """
    应用配置表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_application'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(64), nullable=False)
    ftid = db.Column(db.String(64))
    app_layer = db.Column(db.Integer)
    app_uid = db.Column(db.String(128), nullable=False)
    app_type = db.Column(db.Integer)
    app_name = db.Column(db.String(255), nullable=False)
    app_desc = db.Column(db.String(255), nullable=False)
    app_path = db.Column(db.String(255), nullable=False)
    app_config_path = db.Column(db.String(255), nullable=False)
    process_number = db.Column(db.Integer, nullable=False)
    repo = db.Column(db.String(255), nullable=False)
    hook_command = db.Column(db.Text)
    start_command = db.Column(db.Text)
    restart_command = db.Column(db.Text)
    stop_command = db.Column(db.Text)
    build_path = db.Column(db.String(255), nullable=False)
    build_command = db.Column(db.Text)
    build_outputs = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    service_url = db.Column(db.String(255), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    cdn_bucket = db.Column(db.String(255), nullable=False)
    cdn_region = db.Column(db.String(255), nullable=False)
    cdn_uri = db.Column(db.String(512), nullable=False)
    log_module = db.Column(db.String(255), nullable=False, default='')
    monitor_flag = db.Column(db.Integer, nullable=False)
    ding_token = db.Column(db.Text, nullable=False, default='')
    caller_name = db.Column(db.Text)
    caller_id = db.Column(db.Integer)
    port = db.Column(db.Integer)
    max_load = db.Column(db.Integer)
    reference_load = db.Column(db.Integer)


class TApplicationAlertInfo(db.Model):
    """
    应用告警配置表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_application_alert_info'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True)
    app_uid = db.Column(db.String(128), unique=True, nullable=False)
    log_module = db.Column(db.String(255), nullable=False, default='')
    enable_email = db.Column(db.Boolean, nullable=False, default=True)
    ding_token = db.Column(db.Text, nullable=False, default='')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.now, onupdate=datetime.now)


class TApplicationType(db.Model):
    """
    应用类型配置表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_application_type'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    app_type_id = db.Column(db.Integer, primary_key=True)
    app_type_name = db.Column(db.String(64), nullable=False)
    app_type_desc = db.Column(db.String(255), nullable=False)


class TApplicationServer(db.Model):
    """
    应用-服务关联表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_application_server'
    __table_args__ = (PrimaryKeyConstraint('app_uid', 'server_uid'),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'})

    app_uid = db.Column(db.String(128), nullable=False)
    server_uid = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    port = db.Column(db.Integer, default=None)
    weight = db.Column(db.SmallInteger, default=None)


class TUserApplication(db.Model):
    """
    用户应用关系表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_user_application'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    app_uid = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False,
                            onupdate=datetime.now,
                            default=datetime.now)


class TApplicationBalancerInfo(db.Model):
    """
    应用腾讯负载均衡信息表
    """
    __bind_key__ = 'devops'
    __tablename__ = 't_application_balancer_info'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    app_uid = db.Column(db.String(128), nullable=False)
    lb_id = db.Column(db.String(255), nullable=False)
    lbl_id = db.Column(db.String(255), nullable=False)
    loc_id = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.now, onupdate=datetime.now)
