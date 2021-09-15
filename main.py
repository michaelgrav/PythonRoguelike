import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # instance of our EventHandler class
    event_handler = EventHandler()

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
            # Prints our character to the screen
            root_console.print(x=player_x, y=player_y, string="@")

            # Updates the screen
            context.present(root_console)

            # so we dont have the @ smear across the screen
            root_console.clear()

            # Closes the windows if the x button is pressed
            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit


if __name__ == "__main__":
    main()
