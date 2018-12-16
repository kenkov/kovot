#! /usr/bin/env python
# coding:utf-8


class Speaker:
    def __init__(self, name):
        self.name = name

    def dict(self):
        return {"name": self.name}
