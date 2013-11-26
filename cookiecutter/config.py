#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

from __future__ import unicode_literals
import copy
import os

import yaml

from .exceptions import ConfigDoesNotExistException
from .utils import unicode_open
from .exceptions import InvalidConfiguration


DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser('~/.cookiecutters/'),
    'default_context': {}
}


def get_default_config():
    return copy.copy(DEFAULT_CONFIG)


def get_config(config_path):
    """
    Retrieve the config from the specified path, returning it as a config dict.
    """

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    print("config_path is {0}".format(config_path))
    with unicode_open(config_path) as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle)
        except yaml.scanner.ScannerError:
            raise InvalidConfiguration(
                "%s is no a valid YAML file" % config_path)

    config_dict = get_default_config()
    config_dict.update(yaml_dict)

    return config_dict


def get_user_config():
    """
    Retrieve config from the user's ~/.cookiecutterrc, if it exists.
    Otherwise, return None.
    """

    # TODO: test on windows...
    USER_CONFIG_PATH = os.path.expanduser('~/.cookiecutterrc')

    if os.path.exists(USER_CONFIG_PATH):
        return get_config(USER_CONFIG_PATH)
    return get_default_config()
