#! /usr/bin/env python
# coding:utf-8

from operator import itemgetter


class Selector:
    def select(self, answers, num=10):
        """
        answer format:
            (prob: float, text: str, source: str)
        """
        return sorted(
            answers,
            key=itemgetter(0),
            reverse=True
        )[:num]
