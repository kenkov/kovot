### Message and Response

対話の基本要素は **発話** です。
Kovot では発話を `Message` オブジェクトで表現します。
`Message` オブジェクトは、発話文字列を表す `text` を引数に生成します。

```py
from kovot import Message
msg = Message(text="これが発話です。")
```

オプション引数として話者を表す `Speaker` オブジェクトを指定する `speaker` を引数に指定できます。

```py
from kovot import Speaker
msg = Message(text="話者を指定した発話です",
              speaker=Speaker(name="話者名"))
```

対話システムでは、発話に対して **応答** を返します。
Kovot では、応答を `Response` オブジェクトで表します。
`Response` オブジェクトは、応答文を表す `text` と、応答の適切さを表すスコアである
`score` を引数に指定して生成します。

```py
from kovot import Response
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
