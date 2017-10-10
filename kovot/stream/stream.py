#! /usr/bin/env python
# coding:utf-8


import abc


class Stream(metaclass=abc.ABCMeta):
    def __init__(
        self,
        logger
    ):
        self.logger = logger

    @abc.abstractmethod
    def __iter__(self):
        """
        対話ストリーム
        """
        pass

    @abc.abstractmethod
    def post(self, post_status) -> bool:
        pass

    def say(self, status, answers: [(float, str, str)]) -> bool:

        while answers:
            prob, text, source, info = answers[0]
            post_status = {}
            post_status["status"] = text
            if "in_reply_to_status_id" in info:
                post_status["in_reply_to_status_id"] = \
                    info["in_reply_to_status_id"]
            success_flag = self.post(post_status)
            if success_flag:
                return True
            else:
                answers = answers[1:]
        else:
            return False
