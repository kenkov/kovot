### Mod

`Mod` の実装には、`generate_responses` メソッドを持つクラスを作成します。
`generate_responses` メソッドは

- `Bot` オブジェクトと、ユーザの発話である `Message` オブジェクトを引数に取り、
- 応答である `Response` オブジェクトのリストを返します。

`Bot` オブジェクトは、チャットボットに関する情報を含んでおり、
チャットボットの名前を取得して応答に含めるような使い方ができます。

例えば、オウム返しをする `Mod` は次のように実装できます。

```py
from kovot import Response

class EchoMod:
    def generate_responses(self, bot, message):
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
from kovot import Bot
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
