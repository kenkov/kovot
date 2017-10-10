#! /usr/bin/env python
# coding:utf-8


import os
import time
import logging
from collections import deque
from kovot.stream.stream import Stream
from slackclient import SlackClient


class Slack(Stream):
    def __init__(
        self,
        name,
        logger
    ):
        Stream.__init__(self, logger)
        self.name = name
        self.logger = logger

        slack_token = os.environ["SLACK_API_TOKEN"]
        self.sc = SlackClient(slack_token)
        self.messages = deque([])

    def __iter__(self):
        con = self.sc.rtm_connect()
        if not con:
            raise Exception()
        return self

    def __next__(self):
        while True:
            reses = self.sc.rtm_read()
            logging.info(f"slack: {reses}")
            if reses:
                for item in reses:
                    if (item["type"] == "message" and
                            item.get("username", None) != self.name):
                        self.messages.append(item)
            if self.messages:
                break
            time.sleep(1)
        res = self.messages.popleft()
        return {
            "id": 0,
            "text": res["text"],
            "user": {
                "name": "",
                "screen_name": "",
            },
        }

    def post(self, post_status) -> bool:
        text = post_status["status"]
        self.sc.api_call(
              "chat.postMessage",
              channel="#general",
              username=self.name,
              text=text
        )
        return True
