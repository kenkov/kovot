#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
from html.parser import HTMLParser
from mastodon import StreamListener, MastodonError, Mastodon as MastodonAPI
from queue import Queue
from kovot import Message, Response, Speaker
from logging import Logger
from typing import Iterator, List
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
            if response.message is None:
                result = self.api.status_post(response.text)
            else:
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
            content = self._cleanse_html(raw['content'])
            speaker = Speaker(raw['account']['display_name'])
            yield Message(content, id_=raw['id'], speaker=speaker)

    def on_notification(self, notification: dict) -> None:
        if notification['type'] == 'mention':
            self.queue.put(notification['status'])

    @staticmethod
    def _cleanse_html(html: str) -> str:
        class Parser(HTMLParser):
            def __init__(self, *args, **kwargs):
                super(Parser, self).__init__(*args, **kwargs)
                self.sb: List[str] = []

            def __str__(self) -> str:
                return ''.join(self.sb)

            def handle_data(self, data: str) -> None:
                self.sb.append(data)

        parser = Parser(convert_charrefs=True)
        parser.feed(html)
        return str(parser)
