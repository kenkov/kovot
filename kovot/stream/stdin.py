#! /usr/bin/env python
# coding:utf-8


from kovot.stream.stream import Stream
import sys


class Stdin(Stream):
    def __init__(
        self,
        name,
        screen_name,
        logger
    ):
        Stream.__init__(self, logger)
        self.name = name
        self.screen_name = screen_name
        self.logger = logger

    def __iter__(self):
        return self

    def __next__(self):
        ipt = sys.stdin.readline().strip()
        return {
            "id": 0,
            "text": ipt,
            "user": {
                "name": self.name,
                "screen_name": self.screen_name
            },
        }

    def post(self, post_status) -> bool:
        print("{}".format(post_status["status"]))
        return True
