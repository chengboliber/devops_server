#!/usr/bin/env bash

if [ "$1" = 'prod' ]; then
    cp -f configs_prod.py gateway/configs.py
    s='devops_gateway'
elif [ "$1" = 'test' ]; then
    cp -f configs_test.py gateway/configs.py
    s='devops_gateway_test'
else
    cp -f configs.py gateway/configs.py
    s='devops_gateway_dev'
fi

sed -i -e "s/app_name/$s/g" /huishoubao/loglib/lib/hsblog.xml

gunicorn -c gunicorn.py wsgi:app