import copy

import tcod

from engine import Engine
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    # Max rooms a floor can have
    max_rooms = 30

    max_monsters_per_room = 2

    # Loads the file set
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # instance of our EventHandler class
    event_handler = EventHandler()

    player = copy.deepcopy(entity_factories.player)

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        player=player
    )

    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    # Creates the screen
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Michael's roguelike",
            vsync=True,
    ) as context:
        # Creates our console which we draw to
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # Game loop
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
