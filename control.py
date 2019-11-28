# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

sys.path.append('/huishoubao/config/')

import time
import signal

try:
    import devops_server_config as cfg
except ImportError:
    raise Exception('Couldn\'t find config in /huishoubao/config/')


def start():
    try:
        os.remove('./control.log')
    except Exception:
        pass

    print('create venv ...')
    if not os.path.exists('./venv'):
        os.system('virtualenv --clear -p python2.7 ./venv >> ./control.log')

    print('install required packages ...')
    os.system('./venv/bin/pip install -q -r ./requirements.txt >> '
              './control.log')

    print('start app ...')
    os.system('nohup ./venv/bin/gunicorn -c gunicorn.py wsgi:app >> '
              './control.log 2>&1 & echo $! > %s.pid' % cfg.APP_NAME)


def restart():
    stop()

    sleep_time = 0

    while True:
        sleep_time += 1
        if sleep_time > 300:
            raise Exception('wait too long')

        if os.path.exists('%s.pid' % cfg.APP_NAME):
            time.sleep(1)

        break

    start()


def stop():
    if os.path.exists('%s.pid' % cfg.APP_NAME):
        with open('%s.pid' % cfg.APP_NAME, 'r') as f:
            try:
                pid = int(f.read())
                print('pid is %d' % pid)
                os.kill(pid, signal.SIGTERM)
            except OSError as e:
                if e.errno == 3:
                    print('no such process')

                print(e)

        try:
            os.remove('%s.pid' % cfg.APP_NAME)
        except Exception:
            pass
    else:
        print('pid file not exist')


if len(sys.argv) != 2:
    print('only accept start/restart/stop as argument')
    exit()

flag = sys.argv[1]

if 'start' == flag:
    start()
elif 'restart' == flag:
    restart()
elif 'stop' == flag:
    stop()
else:
    print('only accept start/restart/stop as argument')
