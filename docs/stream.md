### Stream

Using `Stream`, you can connect the input and output of `Bot` with services like `Twitter` or `Slack` .

`Stream` class should implements

- iterator which returns `Message` objects as user utterances,
- `post` method to post a system utterance to a service

For example, `StdIO` stream which takes an input utterance from stdin and output a response to stdout can be implemented as follows;

```py
from kovot import Message
from kovot import Speaker
import sys

class StdIO:
    def __iter__(self):
        return self

    def __next__(self):
        """Iterator method to return user utterances
        as `Message` objects
        """
        ipt = sys.stdin.readline().strip("\n")
        return Message(text=ipt,
                       speaker=Speaker(name="You"))

    def post(self, response) -> bool:
        """This method takes a `Response` object as an argument,
        and output it to stdout.
        """
        print("{}".format(response.text))
```

To work with a stream, execute `Bot.run` method passing `Stream` object as a `stream` argument

```py
from kovot.stream import StdIO

stdio = StdIO()
bot.run(stream=stdio)
# Input user utterance from stdin, then output it to stdout
```
