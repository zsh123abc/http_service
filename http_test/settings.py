#!/usr/bin/env python
# encoding: utf-8

from os import path

# the application settings
settings = {
    'debug': True,
    'cookie_secret': 'test',    # TODO: get the real secret
    'login_url': '/admin/login',
    'xsrf_cookies': False,
    'static_path': path.join(path.dirname(__file__), 'static'),
    'template_path': path.join(path.dirname(__file__), 'templates'),
    #'ui_modules': '' # TODO: the ui modules file
}


import logging
import logging.config

logging.config.fileConfig("logging.conf")
# 初始化
logger = logging.getLogger("weblogger")