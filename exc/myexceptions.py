#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements exceptions.
"""


class MyException(Exception):
    """
    General Exception
    """
    def __init__(self, extra_msg=None):
        self._extra_msg = extra_msg

    def __str__(self, *args, **kwargs):
        msg = self.get_name() if self.get_name() else __name__
        if self._extra_msg:
            msg += ': ' + self._extra_msg

        return msg

    def get_name(self):
        return self.__class__.__name__


class ConfigException(MyException):
    """
    Configuration Error
    """
