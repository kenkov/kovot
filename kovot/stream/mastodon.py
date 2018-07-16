#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
from mastodon import StreamListener, MastodonError, Mastodon as MastodonAPI
from queue import Queue
from kovot.response import Response
from logging import Logger
from typing import Iterator, Optional
__all__ = ['MastodonResponse', 'Mastodon']

_TOOT_LIMIT = 500


class MastodonResponse(Response):
    def __init__(self, text, score,
                 in_reply_to_id: Optional[int]=None,
                 sensitive: bool=False,
                 visibility: Optional[str]=None,
                 spoiler_text: Optional[str]=None,
                 *args, **kwargs
                 ):
        super(MastodonResponse, self).__init__(text, score, *args, **kwargs)
        self.in_reply_to_id = in_reply_to_id
        self.sensitive = sensitive
        self.visibility = visibility
        self.spoiler_text = spoiler_text

    def post(self, api: MastodonAPI) -> str:
        return api.status_post(
            self.text, in_reply_to_id=self.in_reply_to_id, sensitive=self.sensitive,
            visibility=self.visibility, spoiler_text=self.spoiler_text)


class Mastodon(collections.abc.Iterable):
    def __init__(
            self,
            logger: Logger,
            client_id: str,
            client_secret: str,
            access_token: str,
            api_base_url: str
    ):
        self.logger = logger
        self.api = MastodonAPI(
            client_id,
            client_secret,
            access_token,
            api_base_url
        )

    def __iter__(self) -> Iterator:
        class Listener(collections.abc.Iterable, StreamListener):
            def __init__(self):
                self.queue = Queue()

            def __iter__(self) -> Iterator:
                while True:
                    yield self.queue.get()

            def on_notification(self, notification) -> None:
                if notification['type'] == 'mention':
                    self.queue.put(notification['status'])

        listener = Listener()
        self.api.stream_user(listener, run_async=True)
        return iter(listener)

    def post(self, response: MastodonResponse) -> bool:
        self.logger.info("Trying to toot: " + response.text)
        if len(response.text) > _TOOT_LIMIT:
            self.logger.error('Length of given status has exceeded the limit: %d' % len(response.text))
            return False
        try:
            result = response.post(self.api)
            self.logger.info('Updated: ' + str(result))
        except MastodonError:
            self.logger.error('An API error has occured.')
            return False
        return True
