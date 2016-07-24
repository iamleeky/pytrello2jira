#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements logging configuration.
It referred to http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python.
"""

import os
import json
import logging
import logging.config


def setup_logging(default_path='mylogging.json',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_logger(name):
    return logging.getLogger(name)
