# Kovot

Kovot is a chatbot framework written in Python.
It aims to implement prototypes rapidly when researching or develogping chatbots.

Kovot is a simple framework, so you can easily customize it for realizing your idea about chatbots.
Like below, Kovot consists of `Mod` - a base component to generate responses to a user utterance.
You mainly implement `Mod` when building your chatbot in Kovot.

```py
from kovot import Response
from kovot import Bot
from kovot.stream import StdIO


class EchoMod:
    """Echo bot"""
    def generate_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text,
                       message=message,
                       source=self.__class__.__name__)
        return [res]


mods = [EchoMod()]
kovot = Bot(mods=mods)
stdin_stream = StdIO()

kovot.run(stream=stdin_stream)
```

## Install

Install Python 3.7 first, then install the latest version released on GitHub;

```
$ pip install git+https://github.com/kenkov/kovot@0.2.1
```

## Usage

- [Overview](docs/overview.md)
- [Message and Response](docs/message_response.md)
- [Mod](docs/mod.md)
- [Stream](docs/stream.md)
