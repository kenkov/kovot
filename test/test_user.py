#! /usr/bin/env python
# coding:utf-8


import unittest
from kovot.user import User


class UserTest(unittest.TestCase):
    def test_user(self):
        name = "hoge"
        message = User(name=name)
        self.assertEqual(message.name, name)
