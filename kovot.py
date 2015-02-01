#! /usr/bin/env python
# coding:utf-8


import abc
from logging import getLogger


class Module(metaclass=abc.ABCMeta):
    """
    message の形式
    message:
        "id"
        "text"
        "user":
            "name"
            "screen_name"
    """
    def is_fire(self):
        return True

    @abc.abstractmethod
    def reses(self, message, master):
        pass


class Kovot:

    def __init__(
        self,
        target,
        stream,
        master,
        logger=None
    ):
        self.target = target
        self.stream = stream
        self.master = master
        self.logger = logger if logger else getLogger(__file__)
        self.modules = []

    def is_message(self, message):
        """
        Check essage format:
            "id"
            "text"
            "user":
                "name"
                "screen_name"
        """
        return (
            "text" in message and
            "user" in message and
            "id" in message and
            "name" in message["user"] and
            "screen_name" in message["user"]
        )

    def add_module(self, module):
        self.modules.append(module)

    def reses(self, message):
        modules = [module for module in self.modules if module.is_fire()]
        reses = []
        for module in modules:
            reses.extend(module.reses(message, self.master))
        return reses

    def run(self):
        for message in self.stream:
            if not self.is_message(message):
                continue
            elif self.stream.is_tweet_needed(message):
                reses = self.reses(message)

                self.stream.say(
                    message,
                    sorted(reses, reverse=True),
                    num=5
                )
