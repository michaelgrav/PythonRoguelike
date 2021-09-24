from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    """Takes “x” and “y” variables, though these represent a spot on the map. We first
    check that the x and y coordinates are within the map, and are currently visible to the player. If they are,
    then we create a string of the entity names at that spot, separated by a comma. We then return that string,
    adding capitalize to make sure the first letter in the string is capitalized. """
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


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


def render_names_at_mouse_location(
        console: Console, x: int, y: int, engine: Engine
) -> None:
    """Takes the console, x and y coordinates (the location to draw the names),
    and the engine. From the engine, it grabs the mouse’s current x and y positions, and passes them to
    get_names_at_location, which we can assume for the moment will return the list of entity names we want. Once we
    have these entity names as a string, we can print that string to the given x and y location on the screen,
    with console.print. """
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)