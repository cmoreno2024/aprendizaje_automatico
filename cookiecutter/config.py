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
import platform

import yaml

from .exceptions import ConfigDoesNotExistException
from .utils import unicode_open, fix_path
from .exceptions import InvalidConfiguration

DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser(
        os.path.join('~', '.cookiecutters')
    ),
    'default_context': {}
}

def get_config(config_path):
    """
    Retrieve the config from the specified path, returning it as a config dict.
    """
    config_path = fix_path(config_path)

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    print("config_path is {0}".format(config_path))
    with unicode_open(config_path) as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle)
        except yaml.scanner.ScannerError:
            raise InvalidConfiguration(
                "%s is no a valid YAML file" % config_path)

    config_dict = copy.copy(DEFAULT_CONFIG)
    config_dict.update(yaml_dict)
    config_dict['cookiecutters_dir'] = os.path.expanduser(config_dict['cookiecutters_dir'])

    return config_dict


def get_user_config():
    """
    Retrieve config from the user's ~/.cookiecutterrc, if it exists.
    Otherwise, return None.
    """

    # TODO: test on windows...
    USER_CONFIG_PATH = os.path.expanduser(
        os.path.join('~', '.cookiecutterrc')
    )

    if os.path.exists(USER_CONFIG_PATH):
        return get_config(USER_CONFIG_PATH)
    return copy.copy(DEFAULT_CONFIG)
