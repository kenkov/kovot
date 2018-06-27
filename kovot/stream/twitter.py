#! /usr/bin/env python
# coding:utf-8


from datetime import datetime
import TwitterAPI
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


class Twitter(Stream):
    def __init__(
        self,
        logger,
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret
    ):
        # initialize superclass
        Stream.__init__(self, logger)

        self.basetime = datetime.now()
        self.limit = 140

        self.api = TwitterAPI.TwitterAPI(
            consumer_key,
            consumer_secret,
            oauth_token,
            oauth_secret
        )

    def __iter__(self):
        return self.api.request("user").get_iterator()

    def __next__(self):
        pass

    def post(self, post_status) -> bool:
        text = post_status["status"]
        self.logger.info("trying to tweet {}".format(text))
        if len(text) > self.limit:
            self.logger.info(
                "over the length {} > {}".format(len(text), self.limit)
            )
            return False
        else:
            # Update status
            self.logger.info('statuses/update: {}'.format(post_status))
            r = self.api.request('statuses/update', post_status)
            status_code = r.status_code
            self.logger.info("status code: {}".format(status_code))
            if status_code == 200:
                return True
