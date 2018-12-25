### Mod

To implement your `Mod` class, you create a class which has a `generate_responses` method.

`generate_responses` method takes `Speaker` and `Message` objects as arguments.
The `Speaker` object has information about your bot and can be passed via `bot` argument of `Kovot` initializer.
The `Message` object is a user utterance.

`generater_responses` method method a List of `Response` objects.

For example, `EchoMod` can be implemented as follows;

```py
from kovot import Response

class EchoMod:
    def generate_responses(self, bot, message):
        """
        Args:
            bot (Speaker): bot information
            message (Message): user utterance
        """
        res = Response(score=1.0,
                       text=message.text,
                       message=message)
        return [res]
```

After implementing your `Mod`, then generate `Bot` object to talk with it.
`Bot` initializer takes a List of `Mod` objects as a `mods` argument.

```py
from kovot import Bot
bot = Bot(mods=[EchoMod()])
```

When you specify several `Mod` objects to `mods`, 
`Bot` object generate all the responses from each `Mod`,
then select one which has the largest score of `Response`.

To talk with the `Bot` object, pass `Message` object to the `Bot.talk` method. The it returns `Response` as a system response.

```py
bot.talk(message=Message(text="This is an utterance."))
# It returns the response below.
# Response(text="This is an utterance.", score=1.0)
```
