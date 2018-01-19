#! /usr/bin/env python
# coding:utf-8


from collections import namedtuple


Message = namedtuple("Message", ["id_", "text", "user"])
User = namedtuple("User", ["name"])
