# Kovot

Python 製のチャットボットフレームワークです。
チャットボットの研究開発時の利用を想定しており、カスタム性に優れアイディアの素早い実装を可能にします。

## インストール

Kovot は Python 3.7 で動作確認しています。

GitHub 上でリリースしている最新バージョンをインストールしてください。

```sh
$ pip install git+https://github.com/kenkov/kovot@0.1.1
```

## 使い方

Kovot は大きく3つのクラスからできています。

1. Bot
1. Mod
1. Stream

`Bot` は、Kovotのエントリポイントとなるクラスです。
`Bot.talk` メソッドに発話を `Message` オブジェクトとして入力すると、
応答として `Response` オブジェクトが返ります。

`Mod` は、応答を生成するクラスです。
`Bot` 内部では、`Message` オブジェクトを `Mod.get_responses` メソッドに渡すことで
`Response` を生成します。
Kovotでのチャットボット作成は `Mod` クラスを実装することになります。

最後に `Stream` は、入出力の対象を表すクラスです。
例えば `StdIO` は標準入力から発話を受け取り、標準出力に応答を出力します。
`Stream` として Twitter や Slack を使うことで、簡単にそれらの上で動作する
チャットボットを作成できます。

### 発話と応答

対話の基本要素は **発話** です。
Kovot では発話を `Message` オブジェクトで表現します。
`Message` オブジェクトは、発話文字列を表す `text` を引数に生成します。

```py
from kovot.message import Message
msg = Message(text="これが発話です。")
```

オプション引数として話者を表す `Speaker` オブジェクトを指定する `speaker` を引数に指定できます。

```py
from kovot.speaker import Speaker
msg = Message(text="話者を指定した発話です",
              speaker=Speaker(name="話者名"))
```

対話システムでは、発話に対して **応答** を返します。
Kovot では、応答を `Response` オブジェクトで表します。
`Response` オブジェクトは、応答文を表す `text` と、応答の適切さを表すスコアである
`score` を引数に指定して生成します。

```py
from kovot.response import Response
res = Response(text="応答です", score=1.0)
```

`Resposne` オブジェクト生成には、 `Message` オブジェクトと同様の `speaker` 引数に加え、
次の引数をオプションで指定できます。

- `message` は、応答先の `Message` オブジェクトを指定します。
- `source` は、応答を生成した `Mod` 名を文字列を指定します。

```py
res = Response(text="オプション引数ありの応答です",
               score=1.0,
               message=msg,
               source="source名")
```

### Mod の実装

`Mod` の実装には、`get_responses` メソッドを持つクラスを作成します。
`get_responses` メソッドは

- `Bot` オブジェクトと、ユーザの発話である `Message` オブジェクトを引数に取り、
- 応答である `Response` オブジェクトのリストを返します。

`Bot` オブジェクトは、チャットボットに関する情報を含んでおり、
チャットボットの名前を取得して応答に含めるような使い方ができます。

例えば、オウム返しをする `Mod` は次のように実装できます。

```py
from kovot.response import Response

class EchoMod:
    def get_responses(self, bot, message):
        """
        Args:
            bot (Bot): このメソッドを呼ぶ Bot オブジェクトを指定します。
            message (Message): ユーザ発話を表す Message オブジェクトを指定します。
        """
        res = Response(score=1.0,
                       text=message.text,
                       message=message)
        return [res]
```

`Mod` を作成したら、それを指定して `Bot` オブジェクトを作成することで対話が可能となります。
`Bot` オブジェクトは、 `mods` 引数に `Mod` オブジェクトのリストを指定して生成します。

```py
from kovot.bot import Bot
bot = Bot(mods=[EchoMod()])
```

`mods` に複数の `Mod` オブジェクトを指定した場合、
`Bot` オブジェクトは全ての `Mod` から応答を生成し、
スコアが最も大きい応答を最終的な応答として選択します。

`Bot.talk` メソッドに発話を `Message` として入力すると、
応答が `Response` オブジェクトとして帰ってきます。

```py
bot.talk(message=Message(text="ユーザの発話"))
# 次の Response オブジェクトが帰ってくる
# Response(text=ユーザの発話, score=1.0)
```

### Stream

`Stream` オブジェクトを使うことで、 `Bot` の入出力を `Twitter` や `Slack` といった
入出力を伴うサービスと関連づけることができます。

`Stream` オブジェクトには、

- ユーザの発話 `Message` オブジェクトを返すイテレータと
- システムの応答 `Response` オブジェクトをサービスに送る `post` メソッドを実装します。

例えば、
標準入力から `Message` を受け取り、標準出力から `Response` を表示する
`Stream` クラスは次のように実装します。

```py
from kovot.message import Message
from kovot.speaker import Speaker
import sys

class StdIO:
    def __iter__(self):
        return self

    def __next__(self):
        """ユーザからの発話を `Message` として返すイテレータを定義

        Args:
        Returns:
            Message: ユーザの発話を表す Message オブジェクト
        """
        ipt = sys.stdin.readline().strip("\n")
        return Message(text=ipt,
                       speaker=Speaker(name="You"))

    def post(self, response) -> bool:
        """Response オブジェクトを引数に取り、標準出力に表示する。

        Args:
            response (Response): システムの応答を表す Reseponse オブジェクト

        Returns:
            None
        """
        print("{}".format(response.text))
```

`Steram` オブジェクトは、 `Bot.run` メソッドに引数として渡して実行します。

```py
from kovot.stream.stdio import StdIO

stdio = StdIO()
bot.run(stream=stdio)
# 標準入力から発話を入れると、そのまま応答として標準出力に表示される
```

### 全てをまとめた実装例

ここで説明した全ての項目をまとめた実装例を示します。

```py
from kovot.response import Response
from kovot.bot import Bot
from kovot.stream.stdio import StdIO


class EchoMod:
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

kovot.run(stream=stdin_stream)
```
