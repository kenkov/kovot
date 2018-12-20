#! /usr/bin/env python
# coding:utf-8


import unittest
from test.test_mod import ModTestMixin
from kovot.remote_mod import RemoteCallerMod


class RemoteCallerModTest(unittest.TestCase, ModTestMixin):
    def setUp(self):
        self.mod = RemoteCallerMod("example.com", "5000", "api")