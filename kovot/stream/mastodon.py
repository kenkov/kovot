#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
from html.parser import HTMLParser
from mastodon import StreamListener, MastodonError, Mastodon as MastodonAPI
from collections import OrderedDict
from queue import Queue
from kovot import Message, Response, Speaker
from logging import Logger
from typing import Iterator, List, Tuple
__all__ = ['Mastodon']

TOOT_LIMIT: int = 500
CACHE_SIZE: int = 16


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
            api_base_url: str,
            reply_everyone: bool = False
    ):
        self.logger = logger
        self.api = MastodonAPI(
            client_id,
            client_secret,
            access_token,
            api_base_url
        )
        self.myself = self.api.account_verify_credentials()
        self.reply_everyone = reply_everyone
        self._cached = dict()

    def __iter__(self) -> Iterator:
        listener = _TootListener()
        self.api.stream_user(listener, run_async=True)
        self._cached = listener.cache
        return iter(listener)

    def post(self, response: Response) -> bool:
        self.logger.info("Trying to toot: " + response.text)
        if response.message is not None and response.message.id_ in self._cached:
            in_reply_to = self._cached[response.message.id_]
            if self.reply_everyone:
                for user in reversed(in_reply_to['mentions']):
                    if user['id'] != self.myself['id']:
                        response.text = '@%s %s' % (user['acct'], response.text)
            response.text = '@%s %s' % (in_reply_to['account']['acct'], response.text)
        if len(response.text) > TOOT_LIMIT:
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


class _CleansingParser(HTMLParser):
    """
    This class provides a function which removes HTML tags appearing in toots.
    """

    def __init__(self, *args, **kwargs):
        super(_CleansingParser, self).__init__(*args, **kwargs)
        self.sb: List[str] = []
        self._skip: bool = False

    def __str__(self) -> str:
        return ''.join(self.sb)

    def _append(self, text: str) -> None:
        if self._skip:
            return
        self.sb.append(text)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        self._strip = False
        attr = {name: value for name, value in attrs}
        classes = attr['class'].split() if 'class' in attr else []
        if tag == 'br':
            self._append('\n')
        if tag == 'a' and 'mention' in classes:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if self._skip and tag == 'a':
            self._skip = False
            self._strip = True

    def handle_data(self, data: str) -> None:
        if self._strip:
            data = data.lstrip()
        self._strip = False
        self._append(data)


class _TootListener(collections.abc.Iterable, StreamListener):
    """
    A listener collecting only toots related to the connected account, that is, mentions sent to the account.
    This listener **cannot** generate multiple iterators due to some implemental issue for duplicating them.

    Attributes
    ----------
    queue: queue.Queue
        A queue for processing collected toots in order.
    cache: collections.OrderedDict
        This attribute caches recent raw results given by Mastodon API.
    """

    def __init__(self):
        self.queue = Queue()
        self.cache = OrderedDict()

    def __iter__(self) -> Iterator[Message]:
        while True:
            raw = self.queue.get()
            self.cache[raw['id']] = raw
            while len(self.cache) > CACHE_SIZE:
                self.cache.popitem(last=False)
            content = self._cleanse_html(raw['content'])
            speaker = Speaker(raw['account']['display_name'])
            yield Message(content, id_=raw['id'], speaker=speaker)

    def on_notification(self, notification: dict) -> None:
        if notification['type'] == 'mention':
            self.queue.put(notification['status'])

    @staticmethod
    def _cleanse_html(html: str) -> str:
        parser = _CleansingParser(convert_charrefs=True)
        parser.feed(html)
        return str(parser)
