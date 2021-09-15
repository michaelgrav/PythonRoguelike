import tcod


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

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
            root_console.print(x=1, y=1, string="@")

            # Updates the screen
            context.present(root_console)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()
