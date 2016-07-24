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
