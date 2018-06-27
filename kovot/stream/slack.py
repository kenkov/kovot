#! /usr/bin/env python
# coding:utf-8


import os
import time
import logging
import traceback
from collections import deque
from kovot.message import Message
from kovot.speaker import Speaker
from slackclient import SlackClient


class Slack:
    def __init__(self, realname):
        self.realname = realname
        slack_token = os.environ["SLACK_API_TOKEN"]
        self.sc = SlackClient(slack_token)
        self.id2realname = self._get_id2realname()
        self.messages = deque([])

    def _get_id2realname(self):
        return {item["id"]: item["real_name"]
                for item
                in self.sc.api_call("users.list", limit=100)["members"]
                if "real_name" in item}

    def __iter__(self):
        con = self.sc.rtm_connect()
        if not con:
            raise Exception()
        return self

    def __next__(self):
        while True:
            try:
                reses = self.sc.rtm_read()
            except:
                traceback.print_exc()
                self.sc.rtm_connect()

            logging.debug(f"slack: {reses}")
            if reses:
                for item in reses:
                    realname = self.id2realname.get(item.get("user", None),
                                                    None)
                    if (item["type"] == "message" and
                            realname != self.realname):
                        self.messages.append(item)
            if self.messages:
                break
            time.sleep(1)
        mess = self.messages.popleft()
        return Message(id_=0,
                       text=self._get_text(mess),
                       speaker=Speaker(name=""))

    def _get_text(self, message):
        if "text" in message:
            return message["text"]
        if "attachments" in message:
            return message["attachments"][0]["pretext"]

        raise Exception("No text found in message")

    def post(self, response) -> bool:
        self.sc.api_call("chat.postMessage",
                         channel="#bot_test",
                         text=response.text.text,
                         as_user=True  # bot user のアイコン、名前を設定してツイートする
                         )
        return True
