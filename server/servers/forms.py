# -*- coding: utf-8 -*-

from __future__ import absolute_import

from voluptuous import Schema, Required, Optional, All, Coerce, Any


get_server_list_schema = Schema({
    Required('key_word'): All(Coerce(unicode)),
    Optional('page_index', default=1): All(Coerce(int)),
    Optional('page_size', default=10): All(Coerce(int)),
    Optional('status'): All(Coerce(int), Any(0, 1))
})

get_server_schema = Schema({
    Optional('server_uid'): All(Coerce(unicode)),
    Optional('status'): All(Coerce(int), Any(0, 1)),
    Optional('inner_ip'): All(Coerce(unicode))
})

get_app_list_by_server_id_schema = Schema({
    Required('server_uid'): All(Coerce(unicode)),
    Optional('status'): All(Coerce(int), Any(0, 1))
})

add_server_schema = Schema({
    Required('environment'): All(Coerce(unicode)),
    Required('salt_id'): All(Coerce(unicode)),
    Required('server_name'): All(Coerce(unicode)),
    Optional('external_ip', default=''): All(Coerce(unicode)),
    Optional('inner_ip', default=''): All(Coerce(unicode)),
    Optional('server_desc', default=''): All(Coerce(unicode)),
    Optional('qcloud_ins_id', default=''): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

update_server_schema = Schema({
    Required('server_uid'): All(Coerce(unicode)),
    Optional('environment'): All(Coerce(unicode)),
    Optional('salt_id'): All(Coerce(unicode)),
    Optional('external_ip'): All(Coerce(unicode)),
    Optional('inner_ip'): All(Coerce(unicode)),
    Optional('server_name'): All(Coerce(unicode)),
    Optional('server_desc'): All(Coerce(unicode)),
    Optional('qcloud_ins_id'): All(Coerce(unicode)),
    Optional('status'): All(Coerce(int), Any(0, 1))
})

get_app_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Optional('status'): All(Coerce(int), Any(0, 1))
})

get_app_by_name_schema = Schema({
    Required('app_name'): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

get_server_list_by_app_id_schema = Schema({
    Required('app_uid'): All(Coerce(unicode))
})

get_app_list_schema = Schema({
    Required('key_word'): All(Coerce(unicode)),
    Optional('user_id'): All(Coerce(unicode)),
    Optional('ftid'): All(Coerce(unicode)),
    Optional('user_position'):All(Coerce(unicode)),
    Optional('page_index', default=1): All(Coerce(int)),
    Optional('page_size', default=10): All(Coerce(int)),
    Optional('status'): All(Coerce(int), Any(0, 1)),
    Optional('environment'): All(Coerce(unicode)),
    Optional('app_type'): All(Coerce(int), Any(1, 2, 3, 4, 5, 7, 8, 9, 10)),
    Optional('log_module'): All(Coerce(unicode)),
    Optional('ding_token'): All(Coerce(unicode))
})

add_app_schema = Schema({
    Required('app_type'): All(Coerce(int), Any(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
    Required('app_name'): All(Coerce(unicode)),
    Required('environment'): All(Coerce(unicode)),
    Optional('ftid'): All(Coerce(unicode)),
    Optional('app_layer'): All(Coerce(int), Any(0, 1)),
    Optional('app_path', default=''): All(Coerce(unicode)),
    Optional('app_config_path', default=''): All(Coerce(unicode)),
    Optional('build_outputs', default=''): All(Coerce(unicode)),
    Optional('repo', default=''): All(Coerce(unicode)),
    Optional('app_desc', default=''): All(Coerce(unicode)),
    Optional('process_number', default=1): All(Coerce(int)),
    Optional('hook_command', default=''): All(Coerce(unicode)),
    Optional('start_command', default=''): All(Coerce(unicode)),
    Optional('restart_command', default=''): All(Coerce(unicode)),
    Optional('stop_command', default=''): All(Coerce(unicode)),
    Optional('build_path', default=''): All(Coerce(unicode)),
    Optional('build_command', default=''): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1)),
    Optional('service_url', default=''): All(Coerce(unicode)),
    Optional('service_name', default=''): All(Coerce(unicode)),
    Optional('cdn_bucket', default=''): All(Coerce(unicode)),
    Optional('cdn_region', default=''): All(Coerce(unicode)),
    Optional('cdn_uri', default=''): All(Coerce(unicode)),
    Optional('log_module', default=''): All(Coerce(unicode)),
    Optional('monitor_flag', default=0): All(Coerce(int), Any(0, 1)),
    Optional('ding_token'): All(Coerce(unicode)),
    Optional('caller_name'): All(Coerce(unicode)),
    Optional('caller_id', default=0): All(Coerce(int)),
    Optional('port',  default=0): All(Coerce(int)),
    Optional('max_load',  default=0): All(Coerce(int)),
    Optional('reference_load',  default=0): All(Coerce(int))
})

update_app_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Optional('ftid'): All(Coerce(unicode)),
    Optional('environment'): All(Coerce(unicode)),
    Optional('app_layer'): All(Coerce(int)),
    Optional('app_type'): All(Coerce(int), Any(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
    Optional('app_name'): All(Coerce(unicode)),
    Optional('app_desc'): All(Coerce(unicode)),
    Optional('app_path'): All(Coerce(unicode)),
    Optional('app_config_path'): All(Coerce(unicode)),
    Optional('build_outputs'): All(Coerce(unicode)),
    Optional('process_number'): All(Coerce(int)),
    Optional('repo'): All(Coerce(unicode)),
    Optional('hook_command'): All(Coerce(unicode)),
    Optional('start_command'): All(Coerce(unicode)),
    Optional('restart_command'): All(Coerce(unicode)),
    Optional('stop_command'): All(Coerce(unicode)),
    Optional('build_path'): All(Coerce(unicode)),
    Optional('build_command'): All(Coerce(unicode)),
    Optional('status'): All(Coerce(int), Any(0, 1)),
    Optional('service_url'): All(Coerce(unicode)),
    Optional('service_name'): All(Coerce(unicode)),
    Optional('cdn_bucket'): All(Coerce(unicode)),
    Optional('cdn_region'): All(Coerce(unicode)),
    Optional('cdn_uri'): All(Coerce(unicode)),
    Optional('log_module'): All(Coerce(unicode)),
    Optional('monitor_flag'): All(Coerce(int), Any(0, 1)),
    Optional('ding_token'): All(Coerce(unicode)),
    Optional('caller_name'): All(Coerce(unicode)),
    Optional('caller_id', default=0): All(Coerce(int)),
    Optional('port', default=0): All(Coerce(int)),
    Optional('max_load', default=0): All(Coerce(int)),
    Optional('reference_load', default=0): All(Coerce(int))
})

set_app_server_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('server_uid'): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

set_app_servers_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('server_uids'): All(list),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

get_app_server_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('server_uid'): All(Coerce(unicode))
})

get_app_node_status_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('server_uid'): All(Coerce(unicode))
})

get_app_balancer_info_schema = Schema({
    Required('id'): All(Coerce(unicode))
})

get_app_balancer_info_by_app_id_schema = Schema({
    Required('app_uid'): All(Coerce(unicode))
})

get_user_apps_schema = Schema({
    Required('user_id'): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

set_app_users_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('users'): All(list)
})

set_app_user_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('user_id'): All(Coerce(unicode)),
    Required('user_name'): All(Coerce(unicode)),
    Optional('status', default=1): All(Coerce(int), Any(0, 1))
})

add_app_balancer_info_schema = Schema({
    Required('app_uid'): All(Coerce(unicode)),
    Required('lb_id'): All(Coerce(unicode)),
    Required('lbl_id'): All(Coerce(unicode)),
    Required('loc_id'): All(Coerce(unicode)),
    Required('weight'): All(Coerce(int))
})

update_app_balancer_info_schema = Schema({
    Required('id'): All(Coerce(unicode)),
    Optional('app_uid'): All(Coerce(unicode)),
    Optional('lb_id'): All(Coerce(unicode)),
    Optional('lbl_id'): All(Coerce(unicode)),
    Optional('loc_id'): All(Coerce(unicode)),
    Optional('weight'): All(Coerce(int))
})

get_app_balancer_info_list_schema = Schema({
    Required('key_word'): All(Coerce(unicode)),
    Optional('page_index', default=1): All(Coerce(int)),
    Optional('page_size', default=10): All(Coerce(int))
})

get_server_list_by_app_name_schema = Schema({
    Required('app_name'): All(Coerce(unicode)),
})




