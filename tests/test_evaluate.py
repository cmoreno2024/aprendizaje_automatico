#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_evaluate.py
--------------

Tests the evaluation based on a given config.
"""


import sys
import os
import unittest

from cookiecutter.generate import resolve_context

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

class TestPrompt(unittest.TestCase):

    def setUp(self):
        os.environ["COOKIECUTTER_CONTEXT_FILE"] = "tests/test-evaluate/cookiecutter.json"

    def test_evaluation(self):
        self.assertEquals(resolve_context("yo_mama"), "fat")
