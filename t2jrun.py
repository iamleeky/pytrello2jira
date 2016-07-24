#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements entry point of t2j.
"""

import os
import sys
import configparser
import log.mylogging as mylogging
import res.t2jstrings as strings
from t2j.trello2jira import Trello2Jira

# add project directory to build path
sys.path.insert(0, os.path.abspath('.'))

# logging configuration
mylogging.setup_logging(strings.logging_conf_path)

# get logger
logger = mylogging.get_logger(__name__)


def read_config():
    """
    read config
    """
    config = configparser.RawConfigParser()
    config.read(strings.conf_file, strings.conf_encoding)
    return config


def main():
    """
    main function.
    """
    try:
        Trello2Jira(read_config()).run()
    except Exception as err:
        logger.exception(err)

    
if __name__ == '__main__':
    main()
