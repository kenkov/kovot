#! /usr/bin/env python
# coding:utf-8


class Selector:
    def select(self, answers, num=10):
        """
        answer format:
            (prob: float, text: str, source: str)
        """
        return sorted(answers, reverse=True)[:num]
