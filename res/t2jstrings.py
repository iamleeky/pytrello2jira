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
exc_jira_issue_creation_error = 'failed to create jira issue'
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
info_jobs_are_done = 'The jobs are all done.'
info_jobs_count = 'Total'
info_success_count = 'Success'
info_failure_count = 'Failure'
info_failure_count_help = 'See, %s.' % dir_error
info_retry_for_failure = 'Now retry for failed items ...'
info_progress = 'Progress'
# -------------------------------------------

# jira
# -------------------------------------------
order = 'order'
jira_field_basic = 'basic'
jira_field_project = 'project'
jira_field_project_key = 'key'
jira_field_summary = 'summary'
jira_field_description = 'description'
jira_field_issuetype = 'issuetype'
jira_field_issuetype_name = 'name'
jira_field_issuetype_bug = 'Bug'
jira_field_issuetype_task = 'Task'
jira_field_labels = 'labels'
jira_field_attachs = 'attachments'
jira_field_checklists = 'checklists'
jira_field_comments = 'comments'
# -------------------------------------------

# trello
# -------------------------------------------
trel_field_boardname = 'name'
trel_field_boardurl = 'url'
trel_field_boardcards = 'cards'
trel_field_boardlists = 'lists'
trel_field_boardchecklists = 'checklists'
trel_field_boardchecklists_id = 'id'
trel_field_boardchecklists_name = 'name'
trel_field_boardchecklists_checkitems = 'checkItems'
trel_field_boardchecklists_checkitems_state = 'state'
trel_field_boardchecklists_checkitems_statecomplete = 'complete'
trel_field_boardchecklists_checkitems_stateincomplete = 'incomplete'
trel_field_boardchecklists_checkitems_name = 'name'
trel_field_boardactions = 'actions'
trel_field_boardactions_type = 'type'
trel_field_boardactions_typecommentcard = 'commentCard'
trel_field_boardactions_membercreator = 'memberCreator'
trel_field_boardactions_membercreator_fullname = 'fullName'
trel_field_boardactions_data = 'data'
trel_field_boardactions_data_card = 'card'
trel_field_boardactions_data_card_id = 'id'
trel_field_boardactions_data_text = 'text'
trel_field_listid = 'id'
trel_field_listname = 'name'
trel_field_cardname = 'name'
trel_field_carddesc = 'desc'
trel_field_cardurl = 'url'
trel_field_cardid = 'id'
trel_field_cardclosed = 'closed'
trel_field_cardidlist = 'idList'
trel_field_cardattachs = 'attachments'
trel_field_cardidchecklists = 'idChecklists'
trel_field_attachurl = 'url'
# -------------------------------------------
