# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ctypes
import sys
from server import configs as cfg

if not cfg.DEBUG:
    loglib = ctypes.cdll.LoadLibrary("/huishoubao/loglib/lib/libhsbpythonlog.so")


def log_initialize(name, debug=False):
    initialize = loglib.log_initialize_py
    initialize.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    initialize.restype = ctypes.c_bool
    return initialize(name, debug)


def log_debug(text):
    if cfg.DEBUG:
        print(text)
    else:
        f = sys._getframe(1)
        debug = loglib.log_debug_py
        debug.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                          ctypes.c_int]
        debug(text, f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def log_info(text):
    if cfg.DEBUG:
        print(text)
    else:
        f = sys._getframe(1)
        info = loglib.log_info_py
        info.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                         ctypes.c_int]
        info(text, f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def log_warn(text):
    if cfg.DEBUG:
        print(text)
    else:
        f = sys._getframe(1)
        warn = loglib.log_warn_py
        warn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                         ctypes.c_int]
        warn(text, f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def log_error(text):
    if cfg.DEBUG:
        print(text)
    else:
        f = sys._getframe(1)
        error = loglib.log_error_py
        error.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                          ctypes.c_int]
        error(text, f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def log_fatal(text):
    if cfg.DEBUG:
        print(text)
    else:
        f = sys._getframe(1)
        fatal = loglib.log_fatal_py
        fatal.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                          ctypes.c_int]
        fatal(text, f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def log_report(text):
    report = loglib.log_report_py
    report.argtypes = [ctypes.c_char_p]
    report(text)


def log_set_ndc(message):
    set_ndc = loglib.log_set_ndc_py
    set_ndc.argtypes = [ctypes.c_char_p]
    set_ndc(message)


def log_clr_ndc():
    clr_ndc = loglib.log_clr_ndc_py
    clr_ndc()


def log_get_ndc():
    get_ndc = loglib.log_get_ndc_py
    get_ndc.restype = ctypes.c_char_p
    return get_ndc()


def log_get_errinfo():
    get_errinfo = loglib.log_get_errinfo_py
    get_errinfo.restype = ctypes.c_char_p
    return get_errinfo()
