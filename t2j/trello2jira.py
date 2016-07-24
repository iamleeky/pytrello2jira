#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements Trello to JIRA importer.
"""

import argparse
import res.t2jstrings as strings
import log.mylogging as mylogging
import exc.myexceptions as exceptions


class Trello2Jira(object):
    _logger = None
    _args = {}
    _config = None
    _username = ''
    _password = ''
    _url = ''
    _file_list = []

    def __init__(self, config):
        if not config:
            raise exceptions.ConfigException(strings.exc_config_read_error)
        else:
            self._config = config

        self._logger = mylogging.get_logger(self.__class__.__name__)

    def _parse_args(self):
        """
        parse arguments
        """
        parser = argparse.ArgumentParser(description=strings.arg_desc)
        parser.add_argument(strings.arg_key, type=str, nargs='+', help=strings.arg_help)
        self._args = vars(parser.parse_args())

    def _parse_file_list(self):
        """
        parse file list from command line arguments
        """
        self._file_list = self._args[strings.arg_key]

    def _read_auth(self):
        """
        get user id and pwd
        """
        self._username = self._config.get(strings.section_jira, strings.key_jira_username)
        self._password = self._config.get(strings.section_jira, strings.key_jira_password)

    def _read_url(self):
        """
        get jira project url
        """
        self._username = self._config.get(strings.section_jira, strings.key_jira_url)

    def run(self):
        """
        run trello2jira
        """
        self._parse_args()
        self._parse_file_list()
        self._read_auth()
        self._read_url()

        self._logger.debug(strings.dbg_src_files_info + ' '.join(self._file_list))
        self._logger.debug(strings.dbg_user_info + self._username)
