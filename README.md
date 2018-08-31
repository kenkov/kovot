# Kovot

Python 製のチャットボットフレームワークです。
チャットボットの研究開発時の利用を想定しており、カスタム性に優れアイディアの素早い実装を可能にします。

## インストール

Kovot は Python 3.7 で動作確認しています。

GitHub 上でリリースしている最新バージョンをインストールしてください。

```sh
$ pip install git+https://github.com/kenkov/kovot@0.1.0
```

## 例

```python
from kovot.mod import Mod
from kovot.response import Response
from kovot.bot import Bot
from kovot.stream.stdio import StdIO


class EchoMod(Mod):
    """おうむ返しする Kovot mod"""
    def get_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text,
                       message=message,
                       source=self.__class__.__name__)
        return [res]


mods = [EchoMod()]
kovot = Bot(mods=mods)
stdin_stream = StdIO()

kovot.run(stdin_stream)
```
