from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console


def render_bar(
        console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    """Drawing two bars, one on top of the other. The first one will be the background color, which is the health
    bar, will be a red color. The second goes on top, and is green. The one on top will gradually decrease as the
    player drops hit points, as its width is determined by the bar_width variable, which is itself determined by the
    current_value over the maximum_value. """
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )
