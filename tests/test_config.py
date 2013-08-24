#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
-----------

Tests for `cookiecutter.config` module.
"""

import os
import sys
import unittest

from cookiecutter import config

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    from mock import patch
    input_str = '__builtin__.raw_input'

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


test_config_file = 'tests/config/test-config.json'
test_config_obj = {
	'template_dirs': [
		'/home/raphi/dev'
	],
	'default_context': {
		"full_name": "Raphi Gaziano",
		"email": "r.gaziano@gmail.com",
		"github_username": "raphigaziano"
	}
}

class TestConfig(unittest.TestCase):

	def test_create_config(self):
		""" Create a new config file with passed values """
		fname = "tests/config/dynamic-config.json"
		conf = config.create_config({
			'template_dirs': [
				'foo',
				'bar'
			],
			'full_name': 'bob',
			'email': 'bob@bob.com',
			'github_username': 'bobo'
		}, path=fname)

		self.assertEqual(conf['template_dirs'], ['foo', 'bar'])
		self.assertEqual(conf['default_context']['full_name'], 'bob')
		self.assertEqual(conf['default_context']['email'], 'bob@bob.com')
		self.assertEqual(conf['default_context']['github_username'], 'bobo')

		os.remove(fname)

	def test_get_config(self):
		""" Opening and reading config file """
		conf = config.get_config(test_config_file)
		self.assertEqual(conf, test_config_obj)

	def test_auto_gen_config_if_does_not_exist(self):
		""" Auto generation of a default config file if none can be found """
		fname = "tests/config/autogen.json"
		config.get_config(fname)
		self.assertTrue(os.path.exists(fname))
		if os.path.exists(fname):
			os.remove(fname)


if __name__ == '__main__':
    unittest.main()