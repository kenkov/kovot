#! /usr/bin/env python
# coding:utf-8


from kovot.message import Message
from kovot.message import User
import sys


class Stdin:
    def __iter__(self):
        return self

    def __next__(self):
        ipt = sys.stdin.readline().strip("\n")
        return Message(text=ipt,
                       user=User(name="あなた"))

    def post(self, response) -> bool:
        print("{}".format(response.text))
        return True
