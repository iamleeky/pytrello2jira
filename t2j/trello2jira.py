#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements Trello to JIRA importer.
"""

import os
import argparse
import json
# from io import StringIO
from io import BytesIO
from jira import JIRA
from urllib import request
import res.t2jstrings as strings
import log.mylogging as mylogging
import exc.myexceptions as exceptions

now_testing = False
now_testing_field_file = False


class Trello2Jira(object):
    _jira = None  # jira connection object
    _logger = None  # logger
    _args = {}  # command line arguments
    _config = None  # user configuration
    _username = ''  # jira user name
    _password = ''  # jira user password
    _url = ''  # jira project url
    _project = ''  # jira project key
    _file_list = []  # json files exported from trello
    _field_list = []  # fields to be used to create jira issues
    _failed_field_list = []  # failed fields while creating jira issues

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

    def _remove_field(self, in_field_list, in_target_field):
        """
        remove the target field from the given list
        :param in_field_list:
        :param in_target_field:
        :return: none
        """
        for index, field in enumerate(in_field_list):
            if field[strings.order] == in_target_field[strings.order]:
                in_field_list.pop(index)

    def _add_field_if_not_exist(self, in_field_list, in_target_field):
        """
        add the target field into the given list if the field does not exist
        :param in_field_list:
        :param in_target_field:
        :return: none
        """
        for index, field in enumerate(in_field_list):
            if field[strings.order] == in_target_field[strings.order]:
                return

        in_field_list.append(in_target_field.copy())

    def _create_issues_test(self, in_field_list):

        in_field_len = len(in_field_list)

        if not self._jira:
            self._jira = JIRA(server=self._url, basic_auth=(self._username, self._password))

        self._logger.info(strings.info_progress + ':  0 / ' + str(in_field_len))

        for index, field in enumerate(in_field_list):
            try:
                self._logger.info('### _create_issues_test ###')

                # # create issue
                # issue = self._jira.create_issue(fields=field[strings.jira_field_basic])
                #
                # if issue:
                #     # add label
                #     issue.update(labels=field[strings.jira_field_labels])
                #
                #     # add attachment
                #     for src_url in field[strings.jira_field_attachs]:
                #         attachment = BytesIO()
                #         attachment.write(request.urlopen(src_url).read())
                #         self._jira.add_attachment(issue=issue, attachment=attachment,
                #                             filename=src_url[src_url.rindex('/'):])
                #
                #     # add comment
                #     for comment in field[strings.jira_field_comments]:
                #         self._jira.add_comment(issue, comment)
                # else:
                #     raise exceptions.JiraIssueCreationException(strings.exc_jira_issue_creation_error)
                #
                # self._remove_field(self._failed_field_list, field)
            except Exception as err:
                self._add_field_if_not_exist(self._failed_field_list, field)
                self._logger.error(strings.info_create_issue_error)
                self._logger.error(err)

                if not os.path.exists(strings.dir_error):
                    os.makedirs(strings.dir_error)
                fp = open('%s/%d.json' % (strings.dir_error, field[strings.order]), 'w')
                json.dump(field, fp, indent=2)

            self._logger.info(strings.info_progress + ':  ' + str(index + 1) + ' / ' + str(in_field_len))

        self._logger.info('=' * 30)
        self._logger.info(strings.info_jobs_are_done)
        self._logger.info(' * ' + strings.info_jobs_count + ': ' + str(len(self._field_list)))
        self._logger.info(' * ' + strings.info_success_count + ': '
                          + str(len(self._field_list) - len(self._failed_field_list)))
        self._logger.info(' * ' + strings.info_failure_count + ': '
                          + str(len(self._failed_field_list)) + ' (' + strings.info_failure_count_help + ')')
        self._logger.info('=' * 30)

    def _create_issues(self, in_field_list):
        """
        create jira issues with extracted fields

        issue = jira.create_issue(fields=issue_dict) or issue = jira.issue('JIRA-9')
        issue.update(labels=[{'add': 'AAA'}, {'add': 'BBB'}])
        jira.add_attachment(issue=issue, attachment=attachment, filename='content.txt')
        """
        in_field_len = len(in_field_list)

        if not self._jira:
            self._jira = JIRA(server=self._url, basic_auth=(self._username, self._password))

        self._logger.info(strings.info_progress + ':  0 / ' + str(in_field_len))

        for index, field in enumerate(in_field_list):
            try:
                # create issue
                issue = self._jira.create_issue(fields=field[strings.jira_field_basic])

                if issue:
                    # add label
                    issue.update(labels=field[strings.jira_field_labels])

                    # add attachment
                    for src_url in field[strings.jira_field_attachs]:
                        attachment = BytesIO()
                        attachment.write(request.urlopen(src_url).read())
                        self._jira.add_attachment(issue=issue, attachment=attachment, filename=src_url[src_url.rindex('/'):])

                    # add comment
                    for comment in field[strings.jira_field_comments]:
                        self._jira.add_comment(issue, comment)
                else:
                    raise exceptions.JiraIssueCreationException(strings.exc_jira_issue_creation_error)

                self._remove_field(self._failed_field_list, field)
            except Exception as err:
                self._add_field_if_not_exist(self._failed_field_list, field)
                self._logger.error(strings.info_create_issue_error)
                self._logger.error(err)

                if not os.path.exists(strings.dir_error):
                    os.makedirs(strings.dir_error)
                fp = open('%s/%d.json' % (strings.dir_error, field[strings.order]), 'w')
                json.dump(field, fp, indent=2)

            self._logger.info(strings.info_progress + ':  ' + str(index + 1) + ' / ' + str(in_field_len))

        self._logger.info('=' * 30)
        self._logger.info(strings.info_jobs_are_done)
        self._logger.info(' * ' + strings.info_jobs_count + ': ' + str(len(self._field_list)))
        self._logger.info(' * ' + strings.info_success_count + ': '
                          + str(len(self._field_list) - len(self._failed_field_list)))
        self._logger.info(' * ' + strings.info_failure_count + ': '
                          + str(len(self._failed_field_list)) + ' (' + strings.info_failure_count_help + ')')
        self._logger.info('=' * 30)

    def _extract_fields(self):
        """
        extract issue fields from exported trello json files

        <input - trello.json>
        {
            "name": "name of the board",
            "url": "http://...",
            "lists": [...],
            "checklists": [...],
            "cards": [
                {
                    "name": "name of one of cards",
                    "desc": "description of one of cards",
                    "idList": "1234567890",
                    "idChecklists": ["abcdefgh", "...", ...],
                    "url": "http://...",
                    "attachments": [...]
                },
                {...}, ...
            ],
            "actions": [{...}, ...]
        }

        <output - filed lists to be sent to JIRA>
        [
            {
                'order': 0,
                'basic': {
                    'project': {'id': 'ABC'},
                    'summary': 'New issue from jira-python',
                    'description': 'Look into this one',
                    'issuetype': {'name': 'Bug'},
                },
                'labels': [{'add':'AAA'}, {'add':'BBB'}],
                'attachments': ['http://aaa.jpg', 'http://bbb.jpg'],
                'checklists': ['...', ...],
                'comments': ['...', ...]
            },
            {...}, ...
        ]
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

                # organize basic field
                field[strings.jira_field_basic] = dict()
                field[strings.jira_field_basic][strings.jira_field_project] = \
                    {strings.jira_field_project_key: self._project}
                field[strings.jira_field_basic][strings.jira_field_summary] = \
                    '[' + board[strings.trel_field_boardname] + ']' \
                    + '[' + boardlists[card[strings.trel_field_cardidlist]] + ']' \
                    + ' ' + card[strings.trel_field_cardname]
                field[strings.jira_field_basic][strings.jira_field_description] = \
                    card[strings.trel_field_carddesc] \
                    + '\n\n' + '*Board Link* - ' + board[strings.trel_field_boardurl] \
                    + '\n' + '*Card Link* - ' + card[strings.trel_field_cardurl]
                field[strings.jira_field_basic][strings.jira_field_issuetype] = \
                    {strings.jira_field_issuetype_name: strings.jira_field_issuetype_task}

                # organize labels field
                field[strings.jira_field_labels] = []
                field[strings.jira_field_labels].append(
                    {'add': board[strings.trel_field_boardname].replace(' ', '_')})
                field[strings.jira_field_labels].append(
                    {'add': board[strings.trel_field_boardurl].replace(' ', '_')})
                field[strings.jira_field_labels].append(
                    {'add': card[strings.trel_field_cardurl].replace(' ', '_')})
                field[strings.jira_field_labels].append(
                    {'add': boardlists[card[strings.trel_field_cardidlist]].replace(' ', '_')})

                # organize attachments filed
                field[strings.jira_field_attachs] = \
                    [attach[strings.trel_field_attachurl] for attach in card[strings.trel_field_cardattachs]]

                # organize checklists filed
                field[strings.jira_field_checklists] = []
                for chlist_id in card[strings.trel_field_cardidchecklists]:
                    for chlist_trel in board[strings.trel_field_boardchecklists]:
                        if chlist_id == chlist_trel[strings.trel_field_boardchecklists_id]:
                            # make checklist title
                            chlist_jira = '\n' + 'h4. ' + chlist_trel[strings.trel_field_boardchecklists_name]

                            # make checklist items
                            for chlist_trel_item in chlist_trel[strings.trel_field_boardchecklists_checkitems]:
                                # if complete
                                if strings.trel_field_boardchecklists_checkitems_statecomplete \
                                        == chlist_trel_item[strings.trel_field_boardchecklists_checkitems_state]:
                                    chlist_jira += '\n' + '(/)'
                                # or incomplete
                                else:
                                    chlist_jira += '\n' + '(?)'

                                # item name
                                chlist_jira += \
                                    ' ' + chlist_trel_item[strings.trel_field_boardchecklists_checkitems_name]

                            # add checklist
                            field[strings.jira_field_checklists].append(chlist_jira)

                # organize comments
                field[strings.jira_field_comments] = []
                for action in reversed(board[strings.trel_field_boardactions]):
                    if action[strings.trel_field_boardactions_type] == strings.trel_field_boardactions_typecommentcard:
                        action_data = action[strings.trel_field_boardactions_data]
                        action_data_card = action_data[strings.trel_field_boardactions_data_card]
                        action_data_card_id = action_data_card[strings.trel_field_boardactions_data_card_id]
                        action_membercreator = action[strings.trel_field_boardactions_membercreator]
                        if action_data_card_id == card[strings.trel_field_cardid]:
                            # make comment
                            cmnt_author = action_membercreator[strings.trel_field_boardactions_membercreator_fullname]
                            cmnt_content = action_data[strings.trel_field_boardactions_data_text]
                            cmnt_item = 'h4. ' + cmnt_author + '\'s Comment:'
                            cmnt_item += '\n' + cmnt_content

                            # add new comment
                            field[strings.jira_field_comments].append(cmnt_item)

                # manipulate issue description with checklists
                field[strings.jira_field_basic][strings.jira_field_description] += \
                    '\n' + '\n'.join(field[strings.jira_field_checklists])

                # remove new line character from issue summary
                field[strings.jira_field_basic][strings.jira_field_summary].replace('\n', ' ')

                # finally add new filed
                self._field_list.append(field)

        # save it to file
        self._logger.info(strings.info_extract_done)
        if not os.path.exists(strings.dir_extract):
            os.makedirs(strings.dir_extract)
        fp = open('%s/%s' % (strings.dir_extract, strings.file_extract), 'w')
        json.dump(self._field_list, fp, indent=2)

    def _extract_fields_from_file(self):
        """
        extract fields from files which contains already converted fields
        :return: none

        <input>
        {
            'order': 0,
            'basic': {
                'project': {'id': 'ABC'},
                'summary': 'New issue from jira-python',
                'description': 'Look into this one',
                'issuetype': {'name': 'Bug'},
            },
            'labels': [{'add':'AAA'}, {'add':'BBB'}],
            'attachments': ['http://aaa.jpg', 'http://bbb.jpg'],
            'checklists': ['...', ...],
            'comments': ['...', ...]
        }
        """
        for file in self._file_list:
            fp = open(file, 'r', encoding='utf-8')
            field = json.load(fp)
            fp.close()

            # remove new line character from issue summary
            field[strings.jira_field_basic][strings.jira_field_summary] = \
                field[strings.jira_field_basic][strings.jira_field_summary].replace('\n', ' ')

            self._field_list.append(field)

        # save it to file
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

        if now_testing_field_file:
            self._extract_fields_from_file()
        else:
            self._extract_fields()

        # create issues
        if now_testing:
            self._create_issues_test(self._field_list)
        else:
            self._create_issues(self._field_list)

        # retry if any failed job exists
        if len(self._failed_field_list) > 0:
            self._logger.info(strings.info_retry_for_failure)
            if now_testing:
                self._create_issues_test(self._failed_field_list)
            else:
                self._create_issues(self._failed_field_list)
