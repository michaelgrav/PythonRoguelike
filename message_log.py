from typing import Iterable, List, Reversible, Tuple
import textwrap

import tcod

import color


# Used to save and display messages in our log
class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text  # The actual message text.
        self.fg = fg  # The “foreground” color of the message
        self.count = 1  # This is used to display something like “The Orc attacks (x3).” Rather than crowding our
        # message log with the same message over and over, we can “stack” the messages by increasing a message’s
        # count. This only happens when the same message appears several times in a row.

    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []  # Keeps a list of the Messages received

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        """Add a message to this log
        `text` is the message text, `fg` is the text color
        If `stack` is True then the message cna stack with a previous message
        of the same text"""
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: tcod.Console, x: int, y: int, width: int, height: int,
    ) -> None:
        """
        Render this log over the given area
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`,
        """
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapper text message"""
        for line in string.splitlines():  # Handle newlines in messages
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
            cls,
            console: tcod.Console,
            x: int,
            y: int,
            width: int,
            height: int,
            messages: Reversible[Message],
    ) -> None:
        """
        Render the messages provided
        The `messages` are rendered starting at the last message and working backwards
        """
        y_offset = height - 1

        for message in reversed(messages):
            print(message.full_text)
            for line in reversed(list(cls.wrap(message.full_text, width))):  # This is throwing an error
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # No more space to print messages
