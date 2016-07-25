#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements string collection.
"""

# configuration
# -------------------------------------------
conf_file = 'conf/t2j.ini'
conf_encoding = 'utf8'

section_jira = 'jira'
key_jira_url = 'url'
key_jira_project = 'project'
key_jira_username = 'username'
key_jira_password = 'password'
# -------------------------------------------

# arguments
# -------------------------------------------
arg_desc = 'Creates JIRA issues from the given JSON file'
arg_key = 'filePath'
arg_help = 'JSON file path or directory'
# -------------------------------------------

# debugging
# -------------------------------------------
dbg_src_files_info = '* Source Files:'
dbg_user_info = '* User:'
# -------------------------------------------

# logging
# -------------------------------------------
logging_conf_path = 'log/t2jlogging.json'
# -------------------------------------------

# exceptions
# -------------------------------------------
exc_config_read_error = 'error occurs while reading configuration'
# -------------------------------------------

# path
# -------------------------------------------
dir_temp = './temp'
dir_error = dir_temp + '/' + 'error'
dir_extract = dir_temp + '/' + 'extract'
file_extract = 'extract.json'
# -------------------------------------------

# information
# -------------------------------------------
info_create_issue_error = 'There is a failed item. Saved to %s.' % dir_error
info_extract_done = 'All fields has been extracted. Saved to %s.' % dir_extract
# -------------------------------------------

# jira
# -------------------------------------------
order = 'order'
jira_field_project = 'project'
jira_field_project_id = 'id'
jira_field_summary = 'summary'
jira_field_description = 'description'
jira_field_issuetype = 'issuetype'
jira_field_issuetype_name = 'name'
jira_field_issuetype_bug = 'Bug'
jira_field_issuetype_task = 'Task'
jira_field_labels = 'labels'
jira_field_attachs = 'attachments'
# -------------------------------------------

# trello
# -------------------------------------------
trel_field_boardname = 'name'
trel_field_boardurl = 'url'
trel_field_boardcards = 'cards'
trel_field_boardlists = 'lists'
trel_field_listid = 'id'
trel_field_listname = 'name'
trel_field_cardname = 'name'
trel_field_carddesc = 'desc'
trel_field_cardurl = 'url'
trel_field_cardclosed = 'closed'
trel_field_cardidlist = 'idList'
trel_field_cardattachs = 'attachments'
trel_field_attachurl = 'url'
# -------------------------------------------
