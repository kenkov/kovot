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
from kovot import Message
from kovot import Speaker
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
from kovot.stream import StdIO

stdio = StdIO()
bot.run(stream=stdio)
# 標準入力から発話を入れると、そのまま応答として標準出力に表示される
```
