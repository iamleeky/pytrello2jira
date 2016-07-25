#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements Trello to JIRA importer.
"""

import os
import argparse
import json
from jira import JIRA
import res.t2jstrings as strings
import log.mylogging as mylogging
import exc.myexceptions as exceptions


class Trello2Jira(object):
    _logger = None  # logger
    _args = {}  # command line arguments
    _config = None  # user configuration
    _username = ''  # jira user name
    _password = ''  # jira user password
    _url = ''  # jira project url
    _project = ''  # jira project key
    _file_list = []  # json files exported from trello
    _field_list = []  # fields to be used to create jira issues
    _issue_list = []  # finally created jira issues

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
        self._url = self._config.get(strings.section_jira, strings.key_jira_url)

    def _read_project(self):
        """
        get jira project key
        """
        self._project = self._config.get(strings.section_jira, strings.key_jira_project)

    def _create_issues(self):
        """
        create jira issues with extracted fields

        issue = jira.create_issue(fields=issue_dict)
        issue.update(labels=['AAA', 'BBB'])
        jira.add_attachment(issue=issue, attachment=attachment, filename='content.txt')
        """
        jira = JIRA(server=self._url, basic_auth=(self._username, self._password))

        for field in self._field_list:
            try:
                # issue = jira.create_issue(fields=field)
                issue = jira.create_issue(fields={'summary': 'test summary'})
                self._issue_list.append(issue)
            except Exception as err:
                self._logger.error(strings.info_create_issue_error)
                if not os.path.exists(strings.dir_error):
                    os.makedirs(strings.dir_error)
                fp = open('%s/%d.json' % (strings.dir_error, field[strings.order]), 'w')
                json.dump(field, fp, indent=2)

    def _extract_fields(self):
        """
        extract issue fields from exported trello json files

        issue_dict = {
            'project': {'id': 123},
            'summary': 'New issue from jira-python',
            'description': 'Look into this one',
            'issuetype': {'name': 'Bug'},
        }
        """
        for file in self._file_list:
            fp = open(file, 'r', encoding='utf-8')
            board = json.load(fp)
            fp.close()

            boardlists = dict()
            for lst in board[strings.trel_field_boardlists]:
                boardlists[lst[strings.trel_field_listid]] = lst[strings.trel_field_listname]

            for order, card in enumerate(board[strings.trel_field_boardcards]):
                if card[strings.trel_field_cardclosed]:
                    continue

                field = dict()
                field[strings.order] = order
                field[strings.jira_field_project] = {strings.jira_field_project_id: self._project}
                field[strings.jira_field_summary] = card[strings.trel_field_cardname]
                field[strings.jira_field_description] = card[strings.trel_field_carddesc]
                field[strings.jira_field_issuetype] = \
                    {strings.jira_field_issuetype_name: strings.jira_field_issuetype_task}
                field[strings.jira_field_labels] = [board[strings.trel_field_boardname],
                                                    board[strings.trel_field_boardurl],
                                                    card[strings.trel_field_cardurl],
                                                    boardlists[card[strings.trel_field_cardidlist]]]
                field[strings.jira_field_attachs] = \
                    [attach[strings.trel_field_attachurl] for attach in card[strings.trel_field_cardattachs]]

                self._field_list.append(field)

        # save to file
        self._logger.info(strings.info_extract_done)
        if not os.path.exists(strings.dir_extract):
            os.makedirs(strings.dir_extract)
        fp = open('%s/%s' % (strings.dir_extract, strings.file_extract), 'w')
        json.dump(self._field_list, fp, indent=2)

    def run(self):
        """
        run trello2jira
        """
        self._parse_args()
        self._parse_file_list()
        self._read_auth()
        self._read_url()
        self._read_project()

        self._logger.debug(strings.dbg_src_files_info + ' '.join(self._file_list))
        self._logger.debug(strings.dbg_user_info + self._username)

        self._extract_fields()
        self._create_issues()
