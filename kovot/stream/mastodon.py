#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
from mastodon import StreamListener, MastodonError, Mastodon as MastodonAPI
from queue import Queue
from kovot import Message, Response, Speaker
from logging import Logger
from typing import Iterator, Optional
__all__ = ['Mastodon']

_TOOT_LIMIT = 500


class Mastodon(collections.abc.Iterable):
    """
    An implementation of Stream for communicating by Mastodon.

    Attributes
    ----------
    logger: logging.logger
        A logger instance dealing with messages sent by this instance.
    api: mastodon.Mastodon
        A Mastodon instance wrapping APIs of the connected Mastodon instance.
    """

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
        listener = _TootListener()
        self.api.stream_user(listener, run_async=True)
        return iter(listener)

    def post(self, response: Response) -> bool:
        self.logger.info("Trying to toot: " + response.text)
        if len(response.text) > _TOOT_LIMIT:
            self.logger.error('Length of given status has exceeded the limit: %d' % len(response.text))
            return False
        try:
            result = self.api.status_post(response.text, in_reply_to_id=response.message.id_)
            self.logger.info('Updated: ' + str(result))
        except MastodonError:
            self.logger.error('An API error has occured.')
            return False
        return True


class _TootListener(collections.abc.Iterable, StreamListener):
    """
    A listener collecting only toots related to the connected account, that is, mentions sent to the account.
    This listener **cannot** generate multiple iterators due to some implemental issue for duplicating them.

    Attributes
    ----------
    queue: queue.Queue
        A queue for processing collected toots in order.
    """

    def __init__(self):
        self.queue = Queue()

    def __iter__(self) -> Iterator[Message]:
        while True:
            raw = self.queue.get()
            speaker = Speaker(raw['account']['display_name'])
            yield Message(raw['content'], id_=raw['id'], speaker=speaker)

    def on_notification(self, notification: dict) -> None:
        if notification['type'] == 'mention':
            self.queue.put(notification['status'])
